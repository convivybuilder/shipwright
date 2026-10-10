"""Turn an existing launchd property list into a job declaration.

This is the migration tool for existing launchd jobs, and it is also the
harness that tests whether the format can express them: a property list
imported and rendered back must match what it started as, and the round-trip
check in `tools/test_jobs.py` asserts exactly that.

EVERY KEY IS EITHER UNDERSTOOD OR REFUSED. An importer that skipped a key it
did not recognise would emit a declaration that looks complete and renders a
job missing whatever that key did — a `KeepAlive` dropped this way turns a
supervised service into a one-shot that dies for good on its first crash, and
the declaration would give a reader no sign anything was lost. So the known
set is listed here and anything outside it stops the import with the key
named.
"""

from __future__ import annotations

import plistlib
from pathlib import Path

from .declaration import MONTHS, WEEKDAYS, CalendarTime, Job, Restart, Schedule

KNOWN_KEYS = {
    "Label",
    "ProgramArguments",
    "WorkingDirectory",
    "EnvironmentVariables",
    "StandardOutPath",
    "StandardErrorPath",
    "RunAtLoad",
    "StartInterval",
    "StartCalendarInterval",
    "KeepAlive",
    "ThrottleInterval",
    "ExitTimeOut",
    "AbandonProcessGroup",
    "UserName",
}

_WEEKDAY_NAME = dict(enumerate(WEEKDAYS))
_MONTH_NAME = {number: name for number, name in enumerate(MONTHS, start=1)}


class ImportError_(ValueError):
    pass


def _calendar_time(entry: dict, source: str) -> CalendarTime:
    unknown = set(entry) - {"Minute", "Hour", "Day", "Month", "Weekday"}
    if unknown:
        raise ImportError_(
            f"{source}: StartCalendarInterval has unsupported field(s) "
            f"{', '.join(sorted(unknown))}"
        )
    weekday = entry.get("Weekday")
    if weekday is not None:
        # launchd accepts 7 for Sunday as well as 0, and both mean the same day.
        if weekday == 7:
            weekday = 0
        if weekday not in _WEEKDAY_NAME:
            raise ImportError_(f"{source}: Weekday {weekday} is out of range")
    month = entry.get("Month")
    if month is not None and month not in _MONTH_NAME:
        raise ImportError_(f"{source}: Month {month} is out of range")
    return CalendarTime(
        minute=entry.get("Minute"),
        hour=entry.get("Hour"),
        day=entry.get("Day"),
        month=_MONTH_NAME[month] if month is not None else None,
        weekday=_WEEKDAY_NAME[weekday] if weekday is not None else None,
    )


def from_plist_dict(
    plist: dict,
    *,
    source: str,
    description: str,
    platforms: tuple[str, ...] = ("macos", "linux"),
    scope: str = "user",
    enabled_by_default: bool = False,
    name: str | None = None,
) -> Job:
    unknown = set(plist) - KNOWN_KEYS
    if unknown:
        raise ImportError_(
            f"{source}: unsupported launchd key(s) {', '.join(sorted(unknown))}. "
            f"Add it to the declaration format and both renderers, or decide the "
            f"job does not need it — do not drop it silently."
        )

    label = plist.get("Label")
    if not isinstance(label, str) or not label:
        raise ImportError_(f"{source}: missing or empty Label")
    command = plist.get("ProgramArguments")
    if not isinstance(command, list) or not command:
        raise ImportError_(f"{source}: missing or empty ProgramArguments")

    keep_alive = plist.get("KeepAlive")
    if keep_alive is None:
        policy = "never"
    elif keep_alive is True:
        policy = "always"
    elif keep_alive is False:
        policy = "never"
    elif isinstance(keep_alive, dict) and keep_alive == {"SuccessfulExit": False}:
        policy = "on-failure"
    elif isinstance(keep_alive, dict) and keep_alive == {"SuccessfulExit": True}:
        # `SuccessfulExit: true` means launchd restarts the job ONLY after a
        # clean exit, which is the opposite of on-failure and has no slot in
        # RESTART_POLICIES. Reading it as "never" would be the exact silent
        # drop this module exists to prevent: the job would stop being
        # restarted and the declaration would look complete.
        raise ImportError_(
            f"{source}: KeepAlive {{SuccessfulExit: true}} means the job is restarted "
            f"only after it exits 0, which the declaration format cannot express. "
            f"Add a restart policy for it, or decide the job does not need it — do "
            f"not import it as a job that never restarts."
        )
    else:
        raise ImportError_(
            f"{source}: KeepAlive form {keep_alive!r} has no equivalent in the "
            f"declaration format yet"
        )

    throttle = plist.get("ThrottleInterval")
    if throttle is not None and policy == "never":
        raise ImportError_(
            f"{source}: ThrottleInterval is set but KeepAlive is not, so the value "
            f"describes a restart that never happens"
        )

    calendar_raw = plist.get("StartCalendarInterval")
    if calendar_raw is None:
        calendar: tuple[CalendarTime, ...] = ()
    elif isinstance(calendar_raw, dict):
        calendar = (_calendar_time(calendar_raw, source),)
    elif isinstance(calendar_raw, list):
        calendar = tuple(_calendar_time(e, source) for e in calendar_raw)
    else:
        raise ImportError_(
            f"{source}: StartCalendarInterval must be a dictionary or a list of them"
        )

    # UserName is a LaunchDaemon key: launchd ignores it in a LaunchAgent, which
    # already runs as its user. So a property list that carries it is a
    # system-scope job running as that account.
    account = plist.get("UserName")
    if account is not None:
        if not isinstance(account, str) or not account:
            raise ImportError_(f"{source}: UserName must be a non-empty string")
        scope = "system"

    return Job(
        name=name or label.split(".")[-1],
        description=description,
        command=tuple(str(part) for part in command),
        label=label,
        platforms=platforms,
        scope=scope,
        enabled_by_default=enabled_by_default,
        working_directory=plist.get("WorkingDirectory"),
        environment=dict(plist.get("EnvironmentVariables") or {}),
        stdout=plist.get("StandardOutPath"),
        stderr=plist.get("StandardErrorPath"),
        schedule=Schedule(
            at_load=bool(plist.get("RunAtLoad", False)),
            every_seconds=plist.get("StartInterval"),
            calendar=calendar,
        ),
        restart=Restart(policy=policy, delay_seconds=throttle),
        stop_timeout_seconds=plist.get("ExitTimeOut"),
        abandon_process_group=bool(plist.get("AbandonProcessGroup", False)),
        account=account,
        source=source,
    )


def from_file(path: str | Path, **kwargs) -> Job:
    path = Path(path)
    kwargs.setdefault("description", f"Imported from {path.name}; describe this job.")
    with open(path, "rb") as handle:
        plist = plistlib.load(handle)
    return from_plist_dict(plist, source=str(path), **kwargs)


def _toml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def to_toml(job: Job) -> str:
    """The declaration, as the TOML a human will read and edit afterwards."""
    lines = [
        f"name = {_toml_string(job.name)}",
        f"description = {_toml_string(job.description)}",
        f"label = {_toml_string(job.label)}",
        "command = [",
    ]
    lines += [f"  {_toml_string(part)}," for part in job.command]
    lines.append("]")
    lines.append(f"platforms = [{', '.join(_toml_string(p) for p in job.platforms)}]")
    if job.scope != "user":
        lines.append(f"scope = {_toml_string(job.scope)}")
    if job.account is not None:
        lines.append(f"account = {_toml_string(job.account)}")
    lines.append(f"enabled-by-default = {str(job.enabled_by_default).lower()}")
    if job.working_directory:
        lines.append(f"working-directory = {_toml_string(job.working_directory)}")
    if job.stop_timeout_seconds is not None:
        lines.append(f"stop-timeout-seconds = {job.stop_timeout_seconds}")

    if job.stdout or job.stderr:
        lines += ["", "[log]"]
        if job.stdout:
            lines.append(f"stdout = {_toml_string(job.stdout)}")
        if job.stderr:
            lines.append(f"stderr = {_toml_string(job.stderr)}")

    if job.environment:
        lines += ["", "[environment]"]
        for key in sorted(job.environment):
            lines.append(f"{key} = {_toml_string(job.environment[key])}")

    schedule_lines = []
    if job.schedule.at_load:
        schedule_lines.append("at-load = true")
    if job.schedule.every_seconds is not None:
        schedule_lines.append(f"every-seconds = {job.schedule.every_seconds}")
    if schedule_lines:
        lines += ["", "[schedule]"] + schedule_lines
    for time in job.schedule.calendar:
        lines += ["", "[[schedule.calendar]]"]
        if time.weekday:
            lines.append(f"weekday = {_toml_string(time.weekday)}")
        if time.month:
            lines.append(f"month = {_toml_string(time.month)}")
        if time.day is not None:
            lines.append(f"day = {time.day}")
        if time.hour is not None:
            lines.append(f"hour = {time.hour}")
        if time.minute is not None:
            lines.append(f"minute = {time.minute}")

    if job.restart.policy != "never":
        lines += ["", "[restart]", f"policy = {_toml_string(job.restart.policy)}"]
        if job.restart.delay_seconds is not None:
            lines.append(f"delay-seconds = {job.restart.delay_seconds}")

    if job.abandon_process_group:
        lines += ["", "[macos]", "abandon-process-group = true"]

    return "\n".join(lines) + "\n"
