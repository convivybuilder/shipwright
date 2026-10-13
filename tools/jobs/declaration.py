"""Parse and validate a Builder backend job declaration.

A job declaration says what a backend job is, once, in a file the installer
renders as a launchd property list on macOS or a systemd unit on Linux.
`tools/jobs/FORMAT.md` is the format's specification and the reasoning behind
each field; this module is its only parser.

The format is TOML because the installer parses declarations on a machine
where nothing has been installed yet. `tomllib` is in the standard library
from Python 3.11, which the installer provisions anyway, so reading a
declaration costs no dependency. PyYAML would be a bootstrap dependency for
the one file that has to be read before dependencies exist.

WEEKDAYS ARE NAMES AND NEVER NUMBERS, and that is a correctness decision
rather than a readability one. launchd numbers Sunday 0 and also accepts 7;
cron agrees; systemd uses names; Python's `date.weekday()` numbers Monday 0.
A weekly job on Sunday is common, so a renderer that mapped the number
through the wrong convention would move a weekly job by a day and nothing
would report it. A name cannot be misread by either renderer.

CALENDAR FIELDS ARE EXPLICIT AND THE FORMAT IS NOT CRON, for one specific
reason. In cron, when day-of-month and day-of-week are both restricted the
job runs when EITHER matches; launchd ANDs every field it is given. A format
that looked like cron would carry that disagreement into the renderers, where
it would appear as a job firing on days nobody asked for. Naming each field
leaves nothing to a convention.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import tomllib

WEEKDAYS = (
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
)

MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)

PLATFORMS = ("macos", "linux")
SCOPES = ("user", "system")
RESTART_POLICIES = ("always", "on-failure", "never")


class DeclarationError(ValueError):
    """A declaration that cannot be rendered. Carries the file and the field."""

    def __init__(self, source: str, message: str) -> None:
        super().__init__(f"{source}: {message}")
        self.source = source
        self.message = message


@dataclass(frozen=True)
class CalendarTime:
    """One firing time. An absent field means every value of it.

    This is launchd's own model, and it is the reason the format keeps it:
    every launchd calendar schedule is expressible with no translation, so
    the importer that reads the existing property lists is a field rename
    rather than an interpretation.
    """

    minute: int | None = None
    hour: int | None = None
    day: int | None = None
    month: str | None = None
    weekday: str | None = None

    def __post_init__(self) -> None:
        if all(
            getattr(self, f) is None
            for f in ("minute", "hour", "day", "month", "weekday")
        ):
            raise ValueError(
                "a calendar time with no fields fires every minute of every day; "
                "say what you mean with at least one field"
            )
        if self.day is not None and self.weekday is not None:
            # launchd ANDs these, cron ORs them, and a reader cannot tell which
            # was meant. Refusing is better than picking one silently.
            raise ValueError(
                "set day or weekday, not both: launchd runs the job only when both "
                "match while cron runs it when either does, so the declaration "
                "would mean different things to different readers"
            )


@dataclass(frozen=True)
class Schedule:
    """When a job runs. A job may have none of these, and then it runs at load
    and whenever its restart policy brings it back."""

    at_load: bool = False
    every_seconds: int | None = None
    calendar: tuple[CalendarTime, ...] = ()


@dataclass(frozen=True)
class Restart:
    policy: str = "never"
    delay_seconds: int | None = None


@dataclass(frozen=True)
class PrepareStep:
    """One command the installer runs before a job first starts.

    `creates` names a path the step makes. When it already exists the step is
    skipped, which is how a step that must never run twice, such as minting a
    credential, can sit beside steps that run on every install. A relative
    path is read from the job's working directory, where the step runs.
    """

    argv: tuple[str, ...]
    creates: str | None = None


@dataclass(frozen=True)
class Job:
    name: str
    description: str
    command: tuple[str, ...]
    label: str
    platforms: tuple[str, ...] = PLATFORMS
    scope: str = "user"
    enabled_by_default: bool = False
    working_directory: str | None = None
    environment: dict[str, str] = field(default_factory=dict)
    stdout: str | None = None
    stderr: str | None = None
    schedule: Schedule = field(default_factory=Schedule)
    restart: Restart = field(default_factory=Restart)
    # State the job needs before it first starts: directories the installer
    # creates, then commands it runs, in order, on every real install and
    # before anything is activated. See FORMAT.md, "directories and prepare".
    directories: tuple[str, ...] = ()
    prepare: tuple[PrepareStep, ...] = ()
    # How long the supervisor waits after asking the job to stop before it
    # kills it. None leaves the supervisor's default. See FORMAT.md.
    stop_timeout_seconds: int | None = None
    # Commands the installer finds on its own PATH, each written `{name}` in
    # the declaration. See FORMAT.md, "programs".
    programs: tuple[str, ...] = ()
    # launchd's AbandonProcessGroup, for a macOS-only job. See FORMAT.md.
    abandon_process_group: bool = False
    # The account a system-scope job runs as, instead of root. See FORMAT.md,
    # "account".
    account: str | None = None
    source: str = "<memory>"

    def __post_init__(self) -> None:
        """Fence every string that reaches a renderer, on the TYPE.

        THIS IS HERE RATHER THAN IN `parse` BECAUSE `parse` IS NOT THE ONLY WAY
        A JOB IS BUILT. `import_launchd.from_plist_dict` constructs one straight
        from a property list, and `placeholders.resolve` builds one with
        `dataclasses.replace`, and neither went through the parser's checks
        while they lived there. That made the invariant true of jobs that came
        from `parse` rather than of jobs, which is the weaker claim, and the
        suite in `test_jobs_systemd.py` was already rendering imported jobs
        without a parse in between. A frozen dataclass runs this on every
        construction, including `replace`, so there is now one fence and no way
        around it.
        """
        _check_no_control_characters(self.source, "name", self.name)
        _check_no_control_characters(self.source, "description", self.description)
        # `Description=` is written unquoted, like the working directory and the
        # log paths, so a trailing backslash continues the line.
        _check_no_backslash(self.source, "description", self.description)
        _check_label(self.source, self.label)
        for index, part in enumerate(self.command):
            _check_no_control_characters(self.source, f"command[{index}]", part)
        for field_name, value in (
            ("working-directory", self.working_directory),
            ("log.stdout", self.stdout),
            ("log.stderr", self.stderr),
        ):
            if value is not None:
                _check_no_control_characters(self.source, field_name, value)
                _check_no_backslash(self.source, field_name, value)
        for index, directory in enumerate(self.directories):
            _check_no_control_characters(self.source, f"directories[{index}]", directory)
        for index, step in enumerate(self.prepare):
            for position, part in enumerate(step.argv):
                _check_no_control_characters(self.source, f"prepare[{index}][{position}]", part)
            if step.creates is not None:
                _check_no_control_characters(self.source, f"prepare[{index}].creates", step.creates)
        for key, value in self.environment.items():
            _check_no_control_characters(self.source, f"environment key {key!r}", key)
            _check_no_control_characters(self.source, f"environment[{key}]", value)
            _check_environment_key(self.source, key)
        for program in self.programs:
            if not isinstance(program, str) or not PROGRAM.match(program):
                raise DeclarationError(
                    self.source,
                    f"program {program!r} is not a bare command name. It must match "
                    f"{PROGRAM.pattern}, because it is also the placeholder the "
                    f"declaration writes it as, and a path would bypass the lookup "
                    f"this field exists for.",
                )
        # A SYSTEM-SCOPE JOB RUNS AS ROOT, and a program found on the
        # installer's PATH can sit in a directory an ordinary account writes.
        # Nothing needs it, so it is refused rather than gated, the same call
        # `prepare` makes.
        if self.programs and self.scope == "system":
            raise DeclarationError(
                self.source,
                "programs is for user-scope jobs only; a system-scope job runs as "
                "root, and a program found on PATH could be one another account "
                "placed",
            )
        # A user-scope job already runs as the account that installed it, so an
        # account there would read as a setting that took effect and never did.
        if self.account is not None:
            if not isinstance(self.account, str) or not self.account:
                raise DeclarationError(self.source, "account must be a non-empty string")
            if self.scope != "system":
                raise DeclarationError(
                    self.source,
                    "account is for system-scope jobs only; a user-scope job runs "
                    "as the account that installs it, so naming another one would "
                    "never take effect",
                )
            # `User=` and `Group=` are written unquoted, like the working directory.
            _check_no_control_characters(self.source, "account", self.account)
            _check_no_backslash(self.source, "account", self.account)
        # Here with the other fences because `import_launchd` builds a job from
        # a plist's `ExitTimeOut` without going through `parse` (security review).
        stop = self.stop_timeout_seconds
        if stop is not None and (not isinstance(stop, int) or isinstance(stop, bool) or stop < 1):
            raise DeclarationError(
                self.source,
                f"stop-timeout-seconds must be a positive whole number, got {stop!r}",
            )
        # launchd's key with no systemd counterpart this format renders. A job
        # that also runs on Linux would get it on one platform and silently not
        # on the other, so the table is refused there rather than half-applied.
        if self.abandon_process_group and tuple(self.platforms) != ("macos",):
            raise DeclarationError(
                self.source,
                "[macos] is for a job whose platforms is exactly [\"macos\"]; it "
                "sets launchd keys that no systemd unit renders, so on a job that "
                "also runs on Linux it would take effect on one platform only",
            )

    def runs_on(self, platform: str) -> bool:
        return platform in self.platforms


def _require(table: dict, key: str, source: str, kind: type):
    if key not in table:
        raise DeclarationError(source, f"missing required key {key!r}")
    value = table[key]
    if not isinstance(value, kind) or (kind is bool and not isinstance(value, bool)):
        raise DeclarationError(
            source, f"{key!r} must be {kind.__name__}, got {type(value).__name__}"
        )
    return value


def _check_range(source: str, name: str, value, low: int, high: int) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise DeclarationError(source, f"{name} must be a whole number, got {value!r}")
    if not low <= value <= high:
        raise DeclarationError(source, f"{name} must be {low}-{high}, got {value}")
    return value


def _check_no_control_characters(source: str, name: str, value: str) -> str:
    """Refuse a control character in anything that lands in a unit file.

    THIS IS A UNIT-FILE INJECTION FENCE, NOT TIDINESS. A systemd unit is a
    line-oriented text file, so a newline inside a value ends the directive and
    begins a new one, and systemd parses what follows as a real directive. This
    was measured on Ubuntu 22.04 rather than assumed: a declaration with
    `working-directory = "/tmp\\nZZUnknownProbeKey=1"` renders a unit that
    `systemd-analyze verify` reads as two directives, reporting `Unknown key
    name 'ZZUnknownProbeKey'` from the injected line. The same holds for the
    log paths. So a declaration could otherwise add `ExecStartPost=`, or `User=`
    on a system-scope job that runs as root.

    Escaping the newline would not be enough, because the fence has to hold for
    the launchd renderer too, where a newline in an argv entry is preserved as
    data and produces a job whose command cannot be found. Nothing Builder runs
    needs a control character in a path, a command or an environment value, so
    refusing is both safe and simpler than escaping correctly in two formats.
    """
    bad = [
        (index, character)
        for index, character in enumerate(value)
        if ord(character) < 0x20 or ord(character) == 0x7F
    ]
    if bad:
        index, character = bad[0]
        raise DeclarationError(
            source,
            f"{name} contains a control character ({character!r} at position "
            f"{index}). A newline in a value ends the directive in a systemd unit "
            f"file and everything after it is parsed as a new directive, so this "
            f"would let a declaration add unit-file settings it never names.",
        )
    return value


def _check_no_backslash(source: str, name: str, value: str) -> str:
    """Refuse a backslash in a path that systemd writes unquoted.

    `WorkingDirectory=`, `StandardOutput=` and `StandardError=` are written
    without quotes, and systemd treats a trailing backslash as a line
    continuation, so a value ending in one silently swallows the directive on
    the next line. Measured on Ubuntu 22.04: a unit with
    `WorkingDirectory=/tmp/x\\` followed by `ZZProbeKeyAfterBackslash=1` draws
    no complaint about that key, while the identical unit without the
    backslash reports `Unknown key name 'ZZProbeKeyAfterBackslash'`. The
    swallowed line could be a `Restart=` that stops a supervised service being
    supervised.

    A backslash is legal in a POSIX filename and nothing Builder runs uses
    one, so refusing is cheaper than escaping it correctly in a directive
    whose quoting rules differ from the quoted ones.
    """
    if "\\" in value:
        raise DeclarationError(
            source,
            f"{name} contains a backslash. systemd writes this directive unquoted "
            f"and reads a trailing backslash as a line continuation, which silently "
            f"swallows the next directive in the unit file.",
        )
    return value


# A supervisor label becomes a filename in `~/Library/LaunchAgents`,
# `/Library/LaunchDaemons`, `~/.config/systemd/user` or `/etc/systemd/system`.
# Restricting it here is what stops a label being a path: `../../etc/cron.d/evil`
# would otherwise resolve out of the supervisor's directory, and for a
# system-scope job the process writing it is root. Reverse-DNS shape, which is
# what every existing label already uses.
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

# An environment variable name, POSIX shape. The key side of systemd's
# `Environment="KEY=VALUE"` is not quoted, and a key that is not a variable
# name goes wrong silently in two different ways, both measured on Ubuntu
# 22.04: a key containing a space makes systemd report `Invalid environment
# assignment, ignoring` and drop the variable, so the job runs without
# something it declared; and a key containing `=` is accepted, setting a
# DIFFERENT variable to a different value (`A=B` with value `v` sets `A` to
# `B=v`). The value side needs no such rule — systemd treats the whole quoted
# string as one assignment, confirmed by checking that `Environment="A=1 B"`
# draws no complaint about a stray `B`.
ENVIRONMENT_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

# A program name in `programs`. It is the placeholder's name as well, so it
# takes the placeholder shape, which also keeps a slash, and with it a path,
# out.
PROGRAM = re.compile(r"^[a-z][a-z0-9_]*$")


def _check_label(source: str, label: str) -> str:
    if not isinstance(label, str) or not label:
        raise DeclarationError(source, "label must be a non-empty string")
    if not LABEL.match(label):
        raise DeclarationError(
            source,
            f"label {label!r} is not a supervisor label. It becomes a filename in "
            f"LaunchAgents, LaunchDaemons or a systemd unit directory, so it must "
            f"match {LABEL.pattern} — letters, digits, dot, dash and underscore. A "
            f"label containing a path separator or '..' would write the unit "
            f"outside the supervisor's directory, as root for a system-scope job.",
        )
    return label


def _check_environment_key(source: str, key: str) -> str:
    if not ENVIRONMENT_KEY.match(key):
        raise DeclarationError(
            source,
            f"environment key {key!r} is not a variable name. It must match "
            f"{ENVIRONMENT_KEY.pattern}. systemd does not quote the key side of "
            f"Environment=, so a key with a space makes it drop the variable "
            f"silently, a key containing '=' sets a different variable to a "
            f"different value, and a key containing a quote sets a second variable "
            f"the declaration never named.",
        )
    return key


def _check_name(source: str, name: str, value, allowed: tuple[str, ...]) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or value.lower() not in allowed:
        raise DeclarationError(
            source,
            f"{name} must be one of {', '.join(allowed)} (a name, never a number, "
            f"because the number means different days to launchd, cron and systemd), "
            f"got {value!r}",
        )
    return value.lower()


def _calendar_time(entry: dict, source: str) -> CalendarTime:
    unknown = set(entry) - {"minute", "hour", "day", "month", "weekday"}
    if unknown:
        raise DeclarationError(
            source, f"unknown calendar field(s): {', '.join(sorted(unknown))}"
        )
    try:
        return CalendarTime(
            minute=_check_range(source, "calendar.minute", entry.get("minute"), 0, 59),
            hour=_check_range(source, "calendar.hour", entry.get("hour"), 0, 23),
            day=_check_range(source, "calendar.day", entry.get("day"), 1, 31),
            month=_check_name(source, "calendar.month", entry.get("month"), MONTHS),
            weekday=_check_name(
                source, "calendar.weekday", entry.get("weekday"), WEEKDAYS
            ),
        )
    except ValueError as exc:
        if isinstance(exc, DeclarationError):
            raise
        raise DeclarationError(source, str(exc)) from exc


def parse(text: str, source: str = "<memory>") -> Job:
    """Parse one declaration. Raises DeclarationError naming the field."""
    try:
        table = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise DeclarationError(source, f"not valid TOML: {exc}") from exc

    name = _require(table, "name", source, str)
    description = _require(table, "description", source, str)
    if not description.strip():
        raise DeclarationError(
            source,
            "description is empty; it is what an operator reads when deciding "
            "whether to enable the job, so a job without one cannot be reviewed",
        )
    command = _require(table, "command", source, list)
    if not command or not all(isinstance(part, str) for part in command):
        raise DeclarationError(
            source, "command must be a non-empty list of strings (argv, not a shell line)"
        )

    label = table.get("label", name)
    if not isinstance(label, str) or not label:
        raise DeclarationError(source, "label must be a non-empty string")

    platforms = table.get("platforms", list(PLATFORMS))
    if not isinstance(platforms, list) or not platforms:
        raise DeclarationError(source, "platforms must be a non-empty list")
    for entry in platforms:
        if entry not in PLATFORMS:
            raise DeclarationError(
                source, f"unknown platform {entry!r}; known: {', '.join(PLATFORMS)}"
            )

    scope = table.get("scope", "user")
    if scope not in SCOPES:
        raise DeclarationError(
            source, f"scope must be one of {', '.join(SCOPES)}, got {scope!r}"
        )

    enabled = table.get("enabled-by-default", False)
    if not isinstance(enabled, bool):
        raise DeclarationError(source, "enabled-by-default must be true or false")

    environment = table.get("environment", {})
    if not isinstance(environment, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in environment.items()
    ):
        raise DeclarationError(source, "environment must be a table of string to string")

    log = table.get("log", {})
    if not isinstance(log, dict):
        raise DeclarationError(source, "log must be a table")
    unknown_log = set(log) - {"stdout", "stderr"}
    if unknown_log:
        raise DeclarationError(
            source, f"unknown log field(s): {', '.join(sorted(unknown_log))}"
        )

    sched_table = table.get("schedule", {})
    if not isinstance(sched_table, dict):
        raise DeclarationError(source, "schedule must be a table")
    unknown_sched = set(sched_table) - {"at-load", "every-seconds", "calendar"}
    if unknown_sched:
        raise DeclarationError(
            source, f"unknown schedule field(s): {', '.join(sorted(unknown_sched))}"
        )

    every = sched_table.get("every-seconds")
    if every is not None and (
        not isinstance(every, int) or isinstance(every, bool) or every < 1
    ):
        raise DeclarationError(
            source,
            f"schedule.every-seconds must be a positive whole number, got {every!r}",
        )

    calendar_entries = sched_table.get("calendar", [])
    if not isinstance(calendar_entries, list) or not all(
        isinstance(e, dict) for e in calendar_entries
    ):
        raise DeclarationError(
            source, "schedule.calendar must be a list of tables, one per firing time"
        )
    calendar = tuple(_calendar_time(e, source) for e in calendar_entries)

    if every is not None and calendar:
        raise DeclarationError(
            source,
            "set schedule.every-seconds or schedule.calendar, not both: launchd "
            "accepts both keys and fires on each independently, which is never "
            "what a declaration means",
        )

    restart_table = table.get("restart", {})
    if not isinstance(restart_table, dict):
        raise DeclarationError(source, "restart must be a table")
    unknown_restart = set(restart_table) - {"policy", "delay-seconds"}
    if unknown_restart:
        raise DeclarationError(
            source, f"unknown restart field(s): {', '.join(sorted(unknown_restart))}"
        )
    policy = restart_table.get("policy", "never")
    if policy not in RESTART_POLICIES:
        raise DeclarationError(
            source,
            f"restart.policy must be one of {', '.join(RESTART_POLICIES)}, got {policy!r}",
        )
    delay = restart_table.get("delay-seconds")
    if delay is not None and (
        not isinstance(delay, int) or isinstance(delay, bool) or delay < 0
    ):
        raise DeclarationError(
            source, f"restart.delay-seconds must be a whole number, got {delay!r}"
        )
    if delay is not None and policy == "never":
        raise DeclarationError(
            source,
            "restart.delay-seconds has no meaning when restart.policy is never; "
            "a reader would take it as evidence the job restarts",
        )

    schedule = Schedule(
        at_load=bool(sched_table.get("at-load", False)),
        every_seconds=every,
        calendar=calendar,
    )

    if (
        not schedule.at_load
        and schedule.every_seconds is None
        and not schedule.calendar
        and policy == "never"
    ):
        raise DeclarationError(
            source,
            "this job has no schedule, does not run at load and never restarts, "
            "so nothing would ever start it",
        )

    unknown_top = set(table) - {
        "name",
        "description",
        "command",
        "label",
        "platforms",
        "scope",
        "enabled-by-default",
        "working-directory",
        "environment",
        "log",
        "schedule",
        "restart",
        "directories",
        "prepare",
        "stop-timeout-seconds",
        "programs",
        "macos",
        "account",
    }
    if unknown_top:
        raise DeclarationError(
            source,
            f"unknown key(s): {', '.join(sorted(unknown_top))}. A misspelled key "
            f"that was ignored would read as a setting that took effect.",
        )

    working_directory = table.get("working-directory")
    if working_directory is not None and not isinstance(working_directory, str):
        raise DeclarationError(source, "working-directory must be a string")

    stdout = log.get("stdout")
    stderr = log.get("stderr")
    for log_name, log_value in (("log.stdout", stdout), ("log.stderr", stderr)):
        if log_value is not None and not isinstance(log_value, str):
            raise DeclarationError(source, f"{log_name} must be a string")

    directories = table.get("directories", [])
    if not isinstance(directories, list) or not all(
        isinstance(entry, str) and entry for entry in directories
    ):
        raise DeclarationError(source, "directories must be a list of non-empty strings")
    raw_prepare = table.get("prepare", [])
    if not isinstance(raw_prepare, list):
        raise DeclarationError(source, "prepare must be a list of commands")
    prepare = [_parse_prepare_step(entry, index, source) for index, entry in enumerate(raw_prepare)]
    # A PREPARE STEP RUNS SOMEWHERE THE JOB NAMES, AS THE ACCOUNT THAT RUNS THE
    # JOB. Without a working-directory it would run wherever the installer
    # happened to be invoked from. A system-scope job with no `account` is
    # installed as root, so its steps would run as root on every install with
    # no opt-in: nothing needs that, so it is refused rather than gated (security
    # review). One that names an account has its steps run as that account, which
    # is how the Library's database and credentials come to be the account's.
    if (directories or prepare) and scope == "system" and table.get("account") is None:
        raise DeclarationError(
            source,
            "directories and prepare are for user-scope jobs, or for system-scope "
            "jobs that name an account; a system-scope job with no account is "
            "installed as root, and its steps would run as root",
        )
    if prepare and not working_directory:
        raise DeclarationError(
            source,
            "prepare needs a working-directory, so each step runs where the job "
            "says rather than wherever the installer was invoked from",
        )

    # Checked in `Job.__post_init__`, which every construction passes through.
    stop_timeout = table.get("stop-timeout-seconds")

    programs = table.get("programs", [])
    if not isinstance(programs, list) or not all(isinstance(p, str) for p in programs):
        raise DeclarationError(source, "programs must be a list of command names")
    if len(set(programs)) != len(programs):
        raise DeclarationError(source, "programs names a command more than once")

    macos = table.get("macos", {})
    if not isinstance(macos, dict):
        raise DeclarationError(source, "macos must be a table")
    unknown_macos = set(macos) - {"abandon-process-group"}
    if unknown_macos:
        raise DeclarationError(
            source, f"unknown macos field(s): {', '.join(sorted(unknown_macos))}"
        )
    abandon = macos.get("abandon-process-group", False)
    if not isinstance(abandon, bool):
        raise DeclarationError(source, "macos.abandon-process-group must be true or false")
    if macos and tuple(platforms) != ("macos",):
        # Checked here as well as on Job, because a table holding only
        # `abandon-process-group = false` never reaches that check and would
        # otherwise pass on a job that also runs on Linux.
        raise DeclarationError(
            source,
            "[macos] is for a job whose platforms is exactly [\"macos\"]; it sets "
            "launchd keys that no systemd unit renders, so on a job that also "
            "runs on Linux it would take effect on one platform only",
        )

    account = table.get("account")
    if account is not None and not isinstance(account, str):
        raise DeclarationError(source, "account must be a string")

    # NO STRING FENCE RUNS HERE. They live on Job itself, so they hold for every
    # way a Job is built rather than only for this one — see Job.__post_init__,
    # which the constructor below invokes.
    #
    # A copy of the environment-key fence survived here when that move was made,
    # and within one round the two had drifted: this one still raised the
    # message from before the quote case was found, and it fired first, so the
    # real check was never reached for a declaration parsed from a file. That is
    # the failure the move existed to prevent, reproduced by the move itself.
    return Job(
        name=name,
        description=description,
        command=tuple(command),
        label=label,
        platforms=tuple(platforms),
        scope=scope,
        enabled_by_default=enabled,
        working_directory=working_directory,
        environment=dict(environment),
        stdout=stdout,
        stderr=stderr,
        schedule=schedule,
        restart=Restart(policy=policy, delay_seconds=delay),
        directories=tuple(directories),
        prepare=tuple(prepare),
        stop_timeout_seconds=stop_timeout,
        programs=tuple(programs),
        abandon_process_group=abandon,
        account=account,
        source=source,
    )


def _parse_prepare_step(entry, index: int, source: str) -> PrepareStep:
    """A step is argv as a list, or a table `{ run = [...], creates = "path" }`."""
    shape = (
        "each prepare command must be a non-empty list of strings (argv, not a "
        "shell line), or a table { run = [...], creates = \"path\" }"
    )
    creates = None
    argv = entry
    if isinstance(entry, dict):
        unknown = set(entry) - {"run", "creates"}
        if unknown:
            raise DeclarationError(
                source, f"prepare[{index}] has unknown key(s): {', '.join(sorted(unknown))}"
            )
        argv = entry.get("run")
        creates = entry.get("creates")
        if not isinstance(creates, str) or not creates:
            raise DeclarationError(
                source, f"prepare[{index}].creates must be a non-empty string"
            )
    if not isinstance(argv, list) or not argv or not all(isinstance(part, str) for part in argv):
        raise DeclarationError(source, f"prepare[{index}]: {shape}")
    return PrepareStep(argv=tuple(argv), creates=creates)


def load(path: str | Path) -> Job:
    path = Path(path)
    return parse(path.read_text(encoding="utf-8"), source=str(path))


def load_directory(directory: str | Path) -> list[Job]:
    """Every declaration in a directory, sorted by name.

    A duplicate label is refused rather than resolved: two jobs sharing a
    label means one of them silently replaces the other when installed, and
    which one wins depends on the order the directory is read in.
    """
    directory = Path(directory)
    jobs = [load(p) for p in sorted(directory.glob("*.toml"))]
    seen: dict[str, str] = {}
    for job in jobs:
        if job.label in seen:
            raise DeclarationError(
                job.source, f"label {job.label!r} is already used by {seen[job.label]}"
            )
        seen[job.label] = job.source
    return sorted(jobs, key=lambda j: j.name)
