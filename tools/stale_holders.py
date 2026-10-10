"""Which running processes still hold the version an install just replaced.

**A DEPLOYED FILE EXISTS IN THREE PLACES**: the working tree, the deploy area,
and whatever a resident process bound when it started. An install can make the
first two agree and still leave a daemon serving last week's code, and every
check short of the running process comes back green. The case that prompted
this was a long-running watcher whose working directory and loaded native
libraries were all in a deploy area an update had moved aside and deleted
underneath it. Nothing reported it.

So an installer calls `holders()` after it has moved the new area into place
and before it deletes the old one, and prints what comes back. It reports and
never restarts: restarting somebody's live processes is not reversible work,
so it is the operator's decision.

**TWO SIGNALS, BECAUSE EACH IS BLIND WHERE THE OTHER SEES.**

- **`lsof`, for anything under the parked copy.** After the rename, a process's
  working directory and memory-mapped files report the parked path. That catches
  a daemon whose working directory is its area, and anything that loaded a
  native extension from the area's virtualenv. It does not catch a pure-Python
  process, because Python closes each source file once it has imported it.
- **The command line, for a process started before the swap.** A process whose
  command line runs a program inside the area, and which started no later than
  the swap, has loaded the code the swap replaced. The program is argv[0], an
  interpreter's script, or the command a shell's `-c` string runs, after any
  `env`, `timeout`, `nice`, `nohup`, `exec`, `sudo`, `caffeinate` or
  `NAME=value` in front. Each is compared both as written and with symlinks
  resolved, since `{bin}/example-server` is a link into the area and the
  area's own `.venv/bin/python` is a link out of it. A path that is only an
  argument to the program is text, not code. That catches the pure-Python
  process `lsof` cannot see. A process started in the same second as the swap
  is reported, because a false "still running the old version" costs a restart
  nobody needed, and a false silence is the failure this exists for.

**"COULD NOT CHECK" IS ITS OWN ANSWER, NEVER "NOTHING".** When `lsof` or `ps`
is missing or fails, the result says which check did not run. An installer that
printed "nothing holds the previous version" because it could not look would be
a check whose passing and failing states read the same.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Holder:
    pid: int
    command: str
    started: str  # as `ps` printed it, for a person to read
    why: str  # which signal found it


@dataclass
class Report:
    holders: list[Holder] = field(default_factory=list)
    not_checked: list[str] = field(default_factory=list)

    def lines(self, what: str) -> list[str]:
        """What an installer prints about one area, one line each."""
        out = [
            f"  {what}: pid {h.pid} {h.command} (started {h.started}) is still "
            f"running the previous version, found by {h.why}"
            for h in self.holders
        ]
        for missing in self.not_checked:
            out.append(f"  {what}: {missing}, so a process still running the "
                       f"previous version may not be listed")
        if not self.holders and not self.not_checked:
            out.append(f"  {what}: nothing is running the previous version")
        return out


def _under(path: str, top: str) -> bool:
    return path == top or path.startswith(top.rstrip("/") + "/")


def _lsof_pids(parked: Path) -> tuple[dict[int, str], str | None]:
    """Pid to command for every process with a file or directory under `parked`.

    Returns the error text instead when `lsof` could not be run, so the caller
    can say the check did not happen rather than report a clean result.
    """
    # RESOLVED, because `lsof` reports the kernel's path and the caller's may
    # run through a symlink. On macOS `/var` and `/tmp` are links into
    # `/private`, and an installer given `/var/folders/...` compared against
    # `lsof`'s `/private/var/folders/...` and found nothing, silently.
    top = os.path.realpath(parked)
    try:
        done = subprocess.run(
            ["lsof", "-nP", "-w", "-F", "pcn"],
            capture_output=True, text=True, check=False, timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {}, f"lsof could not be run ({exc.__class__.__name__})"
    # `lsof` exits 1 when some files could not be read, which on a busy machine
    # is ordinary; an empty stdout is what means it read nothing at all.
    if not done.stdout:
        return {}, f"lsof produced no output (exit {done.returncode})"
    found: dict[int, str] = {}
    pid, command = None, ""
    for line in done.stdout.splitlines():
        tag, value = line[:1], line[1:]
        if tag == "p":
            pid, command = int(value), ""
        elif tag == "c":
            command = value
        elif tag == "n" and pid is not None and _under(value, top):
            found[pid] = command
    return found, None


def _ps_rows() -> tuple[list[tuple[int, float, str, str]], str | None]:
    """(pid, start as epoch seconds, start as printed, args) for every process."""
    try:
        done = subprocess.run(
            ["ps", "-Ao", "pid=,lstart=,args="],
            capture_output=True, text=True, check=False, timeout=60,
            # The C locale fixes `lstart`'s day and month names, which the
            # parser below reads in English.
            env={**os.environ, "LC_ALL": "C"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], f"ps could not be run ({exc.__class__.__name__})"
    if done.returncode != 0 or not done.stdout:
        return [], f"ps failed (exit {done.returncode})"
    rows = []
    for line in done.stdout.splitlines():
        # `lstart` is always five fields in the C locale: `Tue Sep 22 18:01:48 2026`.
        parts = line.split(None, 6)
        if len(parts) < 7:
            continue
        pid_text, started_text, args = parts[0], " ".join(parts[1:6]), parts[6]
        try:
            started = time.mktime(time.strptime(started_text, "%a %b %d %H:%M:%S %Y"))
        except ValueError:
            continue
        rows.append((int(pid_text), started, started_text, args))
    return rows, None


# An interpreter runs the program named by its first argument that is not an
# option. Anything after that is the program's own arguments, and a path there
# is text: an argument can name a file in the area without running it.
# Case-insensitive, because Homebrew's framework Python re-execs as `Python`.
_INTERPRETER = re.compile(
    r"(python[0-9.]*t?|pypy[0-9.]*|sh|bash|dash|zsh|ksh|node|perl|ruby|java)",
    re.IGNORECASE)


def _family(name: str) -> str:
    name = name.lower()
    if name.startswith(("python", "pypy")):
        return "python"
    if name in {"sh", "bash", "dash", "zsh", "ksh"}:
        return "shell"
    return name


# Per family, because one option means different things to different
# interpreters: `-e` is inline code to node and errexit to a shell, and `-C`
# takes a value for node and none for bash.
# Options that take the next word as their value, so it is not the program.
_OPTION_WITH_VALUE = {
    "python": {"-W", "-X", "--check-hash-based-pycs"},
    "shell": {"-o", "+o", "-O", "+O"},
    "node": {"--env-file", "--inspect-port", "--title", "-C", "--conditions",
             "--disable-warning"},
    "java": {"-cp", "-classpath", "--class-path", "-p", "--module-path"},
    "perl": set(),
    "ruby": {"-C"},
}
# Options whose value is code the interpreter loads before the program: a
# module, or a directory it loads modules from.
_LOADS_CODE = {
    "node": {"-r", "--require", "--import", "--loader", "--experimental-loader"},
    "perl": {"-I"},
    "ruby": {"-r", "-I"},
}
# Options after which the interpreter runs a module or inline code, so no
# program file follows.
_INLINE = {
    "python": {"-m"},
    "node": {"-e", "--eval", "-p", "--print"},
    "perl": {"-e", "-E"},
    "ruby": {"-e"},
}
# Options whose value is the program itself.
_PROGRAM_OPTION = {"java": {"-jar"}}
# A combined short-option word holding `c`, such as `-lc`, `-ec` or `-uc`,
# for the families where `c` means the command follows.
_COMBINED_C = re.compile(r"-[A-Za-z]*c[A-Za-z]*")
# Words that run the command after them, each with the options of its own that
# take a value, and how many words of its own precede the command. The list is
# closed: a launcher not named here hides the command it runs from this signal.
_WRAPPERS = {
    "env": ({"-u", "-C", "-P", "-S"}, 0),
    "nohup": (set(), 0),
    "exec": ({"-a"}, 0),
    "nice": ({"-n"}, 0),
    "timeout": ({"-s", "-k"}, 1),
    "sudo": ({"-u", "-g", "-C", "-h", "-p", "-U", "-D", "-R", "-T"}, 0),
    "caffeinate": ({"-t", "-w"}, 0),
}
# Words that end one shell command, so the word after them starts the next.
_SEPARATORS = {";", "&&", "||", "|", "&"}
# `NAME=value` in front of a command sets its environment.
_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


def _unwrap(tokens: list[str]) -> list[str]:
    """Drop `env VAR=x`, `timeout 30`, `nice -n 5`, `NAME=value` and the like
    from the front."""
    while tokens:
        if _ASSIGNMENT.match(tokens[0]):
            tokens = tokens[1:]
            continue
        wrapper = _WRAPPERS.get(os.path.basename(tokens[0]))
        if wrapper is None:
            return tokens
        with_value, operands = wrapper
        tokens = tokens[1:]
        while tokens and (tokens[0].startswith("-") or _ASSIGNMENT.match(tokens[0])):
            if tokens[0] in with_value:
                tokens = tokens[1:]
            tokens = tokens[1:]
        tokens = tokens[operands:]
    return tokens


def _shell_commands(tokens: list[str]) -> list[list[str]]:
    """Split a `-c` string, as `ps` printed it, into its commands."""
    commands, current = [], []
    for token in tokens:
        if token in _SEPARATORS:
            commands.append(current)
            current = []
            continue
        ends = token.endswith(";")
        # A subshell's parentheses are not part of the program's path.
        token = token.rstrip(";").lstrip("(").rstrip(")")
        if token:
            current.append(token)
        if ends:
            commands.append(current)
            current = []
    commands.append(current)
    return [c for c in commands if c]


def _programs(args: str) -> list[str]:
    """Every path a command line runs as code.

    That is argv[0], an interpreter's script and any code it loads by option,
    and, for a shell's `-c` string, the program each command in it runs. `ps`
    gives the arguments as one string with the quoting gone, so a path holding
    a space is split here as it was before, and the `-c` string runs to the end
    of the line; the lsof signal still sees such a process.
    """
    return _programs_of(args.split())


def _as_path(value: str) -> str:
    """A `file:///x` URL, which node's `--import` accepts, as the path `/x`."""
    return value[len("file://"):] if value.startswith("file:///") else value


def _attached_code(family: str, token: str) -> str | None:
    """The code a code-loading option names in the same word: `--require=<path>`,
    or ruby's `-r<path>`."""
    for option in _LOADS_CODE.get(family, ()):
        if option.startswith("--") and token.startswith(option + "="):
            return token[len(option) + 1:]
        if not option.startswith("--") and token.startswith(option) and len(token) > len(option):
            return token[len(option):].lstrip("=")
    return None


def _programs_of(tokens: list[str]) -> list[str]:
    tokens = _unwrap(tokens)
    if not tokens:
        return []
    found = [tokens[0]]
    name = os.path.basename(tokens[0])
    if not _INTERPRETER.fullmatch(name):
        return found
    family = _family(name)
    rest = tokens[1:]
    i = 0
    while i < len(rest):
        token = rest[i]
        if token in _PROGRAM_OPTION.get(family, ()):
            return found + rest[i + 1:i + 2]
        if token in _LOADS_CODE.get(family, ()):
            found += [_as_path(v) for v in rest[i + 1:i + 2]]
            i += 2
            continue
        attached = _attached_code(family, token)
        if attached:
            found.append(_as_path(attached))
            i += 1
            continue
        if token in _OPTION_WITH_VALUE.get(family, ()):
            i += 2
            continue
        if token in _INLINE.get(family, ()):
            return found
        if family in {"shell", "python"} and (
                token == "-c" or _COMBINED_C.fullmatch(token)):
            if family == "python":
                return found  # inline code, not a program file
            for command in _shell_commands(rest[i + 1:]):
                found.extend(_programs_of(command))
            return found
        if token.startswith(("-", "+")) and token not in {"-", "+"}:
            i += 1
            continue
        # The first word that is not an option is the program, though only an
        # absolute path can be compared with the area.
        return found + [token]
    return found


def holders(parked: Path | None, area: Path, swapped_at: float) -> Report:
    """Every process still running what was at `area` before `swapped_at`.

    `parked` is where the previous version sits after the swap (None when there
    was no previous version, in which case nothing can hold one).
    """
    report = Report()
    if parked is None:
        return report
    me = os.getpid()
    seen: dict[int, Holder] = {}
    starts: dict[int, str] = {}

    rows, ps_error = _ps_rows()
    if ps_error:
        report.not_checked.append(ps_error)
    area_real = os.path.realpath(area)
    named: dict[int, str] = {}
    for pid, _, started_text, args in rows:
        starts[pid] = started_text
        # Last first, so an in-area venv running an in-area script is named
        # by the script rather than by `python`.
        for program in reversed(_programs(args)):
            # The path as written as well as resolved: `{bin}/example-server`
            # is a link into the area, while an area's own `.venv/bin/python`
            # is a link out of it, to the interpreter that built the venv.
            if program.startswith("/") and (
                    _under(os.path.realpath(program), area_real)
                    or _under(os.path.normpath(program), area_real)
                    or _under(os.path.normpath(program), str(area))):
                # Named by the path in the area rather than by `lsof`'s
                # command, which is the interpreter for a Python program and
                # tells a person nothing about what to restart.
                named[pid] = os.path.basename(program)
                break

    lsof_found, lsof_error = _lsof_pids(parked)
    if lsof_error:
        report.not_checked.append(lsof_error)
    for pid, command in lsof_found.items():
        if pid != me:
            seen[pid] = Holder(pid, named.get(pid) or command or "?",
                               starts.get(pid, "at an unknown time"),
                               "a file or directory it has open in the previous version")

    for pid, started, started_text, _ in rows:
        if pid == me or pid in seen or started > swapped_at or pid not in named:
            continue
        seen[pid] = Holder(
            pid, named[pid], started_text,
            "its command line, which names this area and started before the swap",
        )

    report.holders = sorted(seen.values(), key=lambda h: h.pid)
    return report


def main(argv: list[str]) -> int:
    """`stale_holders.py <parked> <area> <swapped-at epoch> <label>`, for a shell
    installer. Prints the report and always exits 0: it informs an install that
    has already succeeded and must not turn that into a failure."""
    if len(argv) != 4:
        print("usage: stale_holders.py <parked> <area> <swapped-at> <label>")
        return 0
    parked, area, swapped_at, label = argv
    for line in holders(Path(parked), Path(area), float(swapped_at)).lines(label):
        print(line)
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv[1:]))
