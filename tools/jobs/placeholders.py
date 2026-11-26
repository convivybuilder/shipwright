"""Resolve the placeholders in a job declaration against one machine.

A declaration is written once and installed on machines that agree about
nothing but the shape of their filesystem. A job imported from one machine
names its home directory or `/opt/homebrew` in its argv, environment or log
path, which is the relocatability gate Builder's release depends on, showing
up inside the supervision layer. So a declaration writes
`{deploy}/library/.venv/bin/python3` and the installer resolves it.

AN UNKNOWN PLACEHOLDER IS AN ERROR, NOT LITERAL TEXT. `{depoly}` left to
render as itself would produce a job whose argv points at a path that cannot
exist, and a job that cannot exec looks from the outside exactly like a job
that ran and did nothing, and a job can fail that way for weeks unnoticed.
Refusing at render time turns that into an install that stops and names the
typo.

THE PLACEHOLDER SET IS CLOSED ON PURPOSE. Every built-in entry is a directory
whose location genuinely differs between a macOS and a Linux install. Anything
else a job needs belongs in its environment table, where a reader can see the
value.

THE ONE OPENING IS A PROGRAM THE JOB NAMES IN `programs`, and it is still
closed per job: `{tmux}` is known only in a declaration that lists `tmux`.
It exists because the path cannot be written down anywhere else. Homebrew puts
tmux under `/opt/homebrew` on one Mac and `/usr/local` on another, the lint
below refuses both, and launchd starts a job with a PATH that holds neither,
so the job cannot find it by name either. The installer runs from the
operator's shell, whose PATH does hold it, so that is where it is looked up.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, replace

from .declaration import Job

PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")

# Paths that name one machine's layout and cannot be right on another.
#
# Homebrew is matched at BOTH its prefixes, because an Intel Mac installs to
# `/usr/local` rather than `/opt/homebrew`, and a declaration written on one
# would otherwise pass the lint that exists to catch exactly this.
#
# **Only the unambiguous parts of the Intel prefix are matched.** `/usr/local`
# alone, and `/usr/local/bin` and `/usr/local/sbin` with it, are ordinary
# Linux locations for software that has nothing to do with Homebrew, so
# flagging them would make the lint report a portable declaration as broken. `Cellar` and
# `opt` under `/usr/local` are Homebrew's own directories and nothing else's.
HOSTILE_TO_PORTABILITY = re.compile(
    # `/Users/` and `/home/` are matched plainly rather than requiring a
    # following non-brace character. An earlier version required one, which let
    # `/Users/{state}` through: a hardcoded macOS home root followed by a
    # placeholder is exactly the mistake this lint exists to catch, and it read
    # as clean. A placeholder on its own is `{home}` and contains neither root,
    # so matching plainly costs no false positive.
    r"/Users/"  # a macOS home directory
    r"|/home/"  # a Linux home directory
    r"|/opt/homebrew"  # Homebrew on Apple Silicon
    r"|/usr/local/(?:Cellar|opt)/"  # Homebrew on Intel
)

KNOWN = {
    "home": "the account the backend runs as: /Users/<name> or /home/<name>",
    "root": "the Builder root, holding crews, knowledge and checkouts",
    "deploy": "the deploy area jobs run from, never a git working tree",
    "state": "writable state and logs",
    "bin": "the directory Builder's own commands are linked into",
    "python": "the interpreter Builder provisioned, by absolute path",
}


@dataclass(frozen=True)
class Machine:
    home: str
    root: str
    deploy: str
    state: str
    bin: str
    python: str

    def as_map(self) -> dict[str, str]:
        return {name: getattr(self, name) for name in KNOWN}

    @classmethod
    def for_home(
        cls,
        home: str,
        *,
        root: str,
        python: str,
        deploy: str | None = None,
        state: str | None = None,
        bin: str | None = None,
    ) -> Machine:
        """The layout an install gives an account whose home is `home`.

        One definition, used both for the account running the installer and
        for the account a system-scope job names, so the two cannot disagree
        about where an account's deploy area is.
        """
        return cls(
            home=home,
            root=root,
            deploy=deploy or f"{home}/.local/deploy",
            state=state or f"{home}/.local/state",
            bin=bin or f"{home}/.local/bin",
            python=python,
        )

    def for_account(self, home: str) -> Machine:
        """This layout moved to another account's home.

        `root` and `python` carry over. Neither is derived from a home: the
        Builder root is whatever `--root` or `builder-root` named, and the
        interpreter is the one Builder provisioned.
        """
        return Machine.for_home(home, root=self.root, python=self.python)


class PlaceholderError(ValueError):
    pass


def unknown_placeholders(job: Job) -> set[str]:
    """Every placeholder in this job that the installer could not resolve."""
    found: set[str] = set()
    for text in _all_strings(job):
        found.update(PLACEHOLDER.findall(text))
    if job.own_root is not None:
        found.update(PLACEHOLDER.findall(job.own_root))
    return found - set(KNOWN) - set(job.programs)


def uses_placeholder(job: Job, name: str) -> bool:
    """Whether any field this installer renders names `{name}`."""
    return any(f"{{{name}}}" in text for text in _all_strings(job))


def _all_strings(job: Job):
    """Every string `resolve` substitutes placeholders into.

    `own_root` IS DELIBERATELY LEFT OUT. It is resolved once, on its own, by
    `own_root_value`, against every placeholder but `{root}`, the one name it
    exists to replace, so folding it in here would let it be substituted
    through the ordinary path, `{root}` included, which is exactly backward.
    It is also what `uninstall-builder`'s `state_plan` reads this generator
    for to tell which of a job's resolved fields are safe to treat as a
    removable name under `{state}`; that reasoning assumes every string here
    went through the ordinary substitution, which `own_root` never does.

    `account_environment` AND `account_prepare` ARE INCLUDED, unlike
    `own_root`: both resolve against the same full placeholder set their
    plain counterparts do, through the ordinary path, so there is nothing
    backward about reading them here for the lint and unknown-placeholder
    checks. `resolve` merges each into its plain counterpart and clears it,
    so a resolved job's `account_environment` and `account_prepare` are
    always empty and `state_plan`'s reasoning above still holds.
    """
    yield from job.command
    if job.working_directory:
        yield job.working_directory
    if job.stdout:
        yield job.stdout
    if job.stderr:
        yield job.stderr
    yield from job.environment.values()
    yield from job.account_environment.values()
    yield from job.directories
    for step in job.prepare:
        yield from step.argv
        if step.creates:
            yield step.creates
    for step in job.account_prepare:
        yield from step.argv
        if step.creates:
            yield step.creates


def resolve(job: Job, machine: Machine, programs: Mapping[str, str] | None = None) -> Job:
    """This job with every placeholder replaced by this machine's path.

    `programs` maps each name in the job's `programs` to the absolute path the
    installer found for it. The lookup is the caller's, so this stays a pure
    function a test can hand any machine.
    """
    programs = programs or {}
    shadowing = sorted(set(job.programs) & set(KNOWN))
    if shadowing:
        raise PlaceholderError(
            f"{job.source}: programs names {', '.join(shadowing)}, which is already "
            f"a built-in placeholder. The declaration could not say which one "
            f"{'{' + shadowing[0] + '}'} means."
        )
    missing = sorted(name for name in job.programs if name not in programs)
    if missing:
        raise PlaceholderError(
            f"{job.source}: no path was found for program(s) {', '.join(missing)}."
        )
    unknown = unknown_placeholders(job)
    if unknown:
        known = ", ".join(sorted(KNOWN))
        raise PlaceholderError(
            f"{job.source}: unknown placeholder(s) "
            f"{', '.join('{' + name + '}' for name in sorted(unknown))}. "
            f"Known placeholders are {known}. A placeholder left to render as "
            f"itself produces a job that cannot exec, which looks exactly like a "
            f"job that ran and did nothing."
        )
    values = {**machine.as_map(), **{name: programs[name] for name in job.programs}}

    def sub(text: str) -> str:
        return PLACEHOLDER.sub(lambda m: values[m.group(1)], text)

    # account_environment and account_prepare apply only while the job's
    # account is in force (FORMAT.md, "account-environment",
    # "account-prepare"); dropping the account, as `install-jobs.as_invoker`
    # does for `--single-account`, leaves nothing for either to apply to, so
    # both are merged into their plain counterpart here and never on a job
    # whose account has already been dropped.
    environment = dict(job.environment)
    prepare_steps = job.prepare
    if job.account is not None:
        environment.update(job.account_environment)
        prepare_steps = (*job.prepare, *job.account_prepare)

    return replace(
        job,
        command=tuple(sub(part) for part in job.command),
        working_directory=sub(job.working_directory) if job.working_directory else None,
        stdout=sub(job.stdout) if job.stdout else None,
        stderr=sub(job.stderr) if job.stderr else None,
        environment={key: sub(value) for key, value in environment.items()},
        account_environment={},
        directories=tuple(sub(directory) for directory in job.directories),
        prepare=tuple(
            replace(
                step,
                argv=tuple(sub(part) for part in step.argv),
                creates=sub(step.creates) if step.creates else None,
            )
            for step in prepare_steps
        ),
        account_prepare=(),
    )


def own_root_value(job: Job, machine: Machine, programs: Mapping[str, str] | None = None) -> str | None:
    """What `{root}` becomes for this job alone, or `None` when it declares
    no `own-root`.

    Resolved against every placeholder `machine` carries but `{root}` itself;
    `Job.__post_init__` already refuses an `own-root` that names `{root}`,
    since that would need its own answer before it has one. The caller
    substitutes the result for `machine.root` before calling `resolve`, so
    every other field that names `{root}` gets this job's own answer.
    """
    if job.own_root is None:
        return None
    programs = programs or {}
    unknown = set(PLACEHOLDER.findall(job.own_root)) - set(KNOWN) - set(job.programs)
    if unknown:
        known = ", ".join(sorted(KNOWN))
        raise PlaceholderError(
            f"{job.source}: own-root uses unknown placeholder(s) "
            f"{', '.join('{' + name + '}' for name in sorted(unknown))}. "
            f"Known placeholders are {known}."
        )
    values = {**machine.as_map(), **{name: programs[name] for name in job.programs}}
    resolved = PLACEHOLDER.sub(lambda m: values[m.group(1)], job.own_root)
    if not resolved.startswith("/"):
        raise PlaceholderError(
            f"{job.source}: own-root resolves to {resolved!r}, which is not an "
            f"absolute path. Every field that uses {{root}} is written assuming "
            f"it is one."
        )
    return resolved


def unresolved_absolute_paths(job: Job) -> list[str]:
    """Strings that name one machine's layout instead of using a placeholder.

    This is what a lint run over the shipped declarations checks. It looks for
    the two roots that cannot be right on another machine: a home directory
    under `/Users` or `/home`, and Homebrew's prefix, which does not exist on
    Linux at all.
    """
    offenders = []
    for text in _all_strings(job):
        if HOSTILE_TO_PORTABILITY.search(text):
            offenders.append(text)
    if job.own_root is not None and HOSTILE_TO_PORTABILITY.search(job.own_root):
        offenders.append(job.own_root)
    return offenders
