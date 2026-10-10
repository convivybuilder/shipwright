"""Render a job declaration as systemd units.

systemd is the supervisor on Ubuntu 22.04, a platform the backend is committed
to run on alongside macOS. A scheduled job becomes two units, a `.service`
saying what to run and a `.timer` saying when; a long-running job becomes a
`.service` alone.

WHERE THE TWO SUPERVISORS DISAGREE, AND WHAT THIS RENDERER DOES ABOUT IT.
Each of these is a place where a faithful-looking translation changes when a
job runs, so each is handled explicitly rather than left to a default:

- **An interval is measured from different moments.** launchd's StartInterval
  counts from the last time the job was STARTED; systemd's OnUnitInactiveSec
  counts from the last time it FINISHED, which for a job that takes two
  minutes turns a 15-minute interval into a 17-minute one. `OnUnitActiveSec`
  counts from the last start, so that is what this renderer emits.

- **A missed firing is not missed the same way.** launchd runs a calendar job
  when the machine wakes if it was asleep at the firing time. systemd drops
  it unless the timer says `Persistent=true`, so every calendar timer here
  sets it. Without that line a laptop-hosted backend would silently skip the
  nightly jobs it was asleep for, and nothing would report a run that never
  happened.

- **Running at load is not a schedule.** launchd's RunAtLoad on a job that
  also has an interval means "and also once, now". The timer equivalent is
  `OnActiveSec=0`, which fires once when the timer itself starts.

- **Output goes to a file only if it is asked for.** systemd sends a service's
  output to the journal by default, where the existing log paths would not
  exist. `append:` keeps the declaration's paths, so a runbook that says to
  read a log file keeps working on both platforms.
"""

from __future__ import annotations

from . import accounts
from .declaration import CalendarTime, Job

_SYSTEMD_WEEKDAY = {
    "sunday": "Sun",
    "monday": "Mon",
    "tuesday": "Tue",
    "wednesday": "Wed",
    "thursday": "Thu",
    "friday": "Fri",
    "saturday": "Sat",
}

_SYSTEMD_MONTH = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}


def _specifiers(value: str) -> str:
    """Escape systemd's `%` specifiers so a value means what it says.

    systemd expands `%h`, `%H`, `%i` and friends in most directives, where
    launchd treats `%` as an ordinary character. So a description reading
    "alerts when disk usage exceeds 90%" or a path containing a percent would
    mean one thing on macOS and another on Linux. `%%` is systemd's escape for
    a literal percent.

    Measured rather than read: a unit carrying `%z`, which is not a valid
    specifier, draws `Failed to resolve unit specifiers ... Invalid slot` from
    `systemd-analyze verify` in `Description=`, `Environment=` and
    `WorkingDirectory=`, and in the working directory it is fatal — the unit
    will not start. Doubling the percent silences all three.
    """
    return value.replace("%", "%%")


def _quote(value: str) -> str:
    """systemd unit-file escaping for a value that may contain spaces.

    Control characters are refused by the declaration parser rather than
    escaped here, because the same fence has to hold for the launchd renderer.
    See `_check_no_control_characters` in `declaration.py`. The newline escape
    below is a second fence rather than the first one: this function is the
    systemd-escaping primitive, so it should not depend on a caller elsewhere
    having already checked.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", "\\n").replace("\r", "\\r")
    return _specifiers(escaped)


def on_calendar(time: CalendarTime) -> str:
    """One OnCalendar= expression.

    The shape is `DOW YYYY-MM-DD HH:MM:SS`, and `*` is systemd's spelling of
    the same wildcard launchd expresses by leaving a field out. Seconds are
    always `00` because launchd has no seconds field, so a declaration can
    never mean anything else.
    """
    dow = _SYSTEMD_WEEKDAY[time.weekday] + " " if time.weekday else ""
    month = _SYSTEMD_MONTH[time.month] if time.month else "*"
    day = f"{time.day:02d}" if time.day is not None else "*"
    hour = f"{time.hour:02d}" if time.hour is not None else "*"
    minute = f"{time.minute:02d}" if time.minute is not None else "*"
    return f"{dow}*-{month}-{day} {hour}:{minute}:00"


def _service_body(job: Job, directory: accounts.Directory) -> list[str]:
    lines = [
        "[Unit]",
        f"Description={_specifiers(job.description.strip().splitlines()[0])}",
        "",
        "[Service]",
    ]
    if job.account is not None:
        account = accounts.require(job.account, job.source, directory)
        # systemd sets HOME from the account's passwd entry when User= is
        # given, so only launchd's renderer writes it. The umask matches
        # launchd's Umask, so the two platforms create files alike.
        lines.append(f"User={_specifiers(account.name)}")
        lines.append(f"Group={_specifiers(account.group)}")
        lines.append("UMask=0027")
    is_long_running = job.restart.policy == "always" and not (
        job.schedule.every_seconds or job.schedule.calendar
    )
    lines.append("Type=simple" if is_long_running else "Type=oneshot")
    lines.append(
        "ExecStart=" + " ".join(f'"{_quote(part)}"' for part in job.command)
    )
    if job.working_directory:
        lines.append(f"WorkingDirectory={_specifiers(job.working_directory)}")
    for key in sorted(job.environment):
        lines.append(f'Environment="{key}={_quote(job.environment[key])}"')
    if job.stdout:
        lines.append(f"StandardOutput=append:{_specifiers(job.stdout)}")
    if job.stderr:
        lines.append(f"StandardError=append:{_specifiers(job.stderr)}")

    if job.restart.policy == "always":
        lines.append("Restart=always")
    elif job.restart.policy == "on-failure":
        lines.append("Restart=on-failure")
    if job.restart.delay_seconds is not None:
        lines.append(f"RestartSec={job.restart.delay_seconds}")
    if job.stop_timeout_seconds is not None:
        lines.append(f"TimeoutStopSec={job.stop_timeout_seconds}")

    return lines


def render_service(job: Job, directory: accounts.Directory = accounts.lookup) -> str:
    """The `.service` unit.

    A job with a timer is installed with no `[Install]` section on purpose:
    the timer is what pulls it in, and a service that was also `WantedBy` a
    target would run once at every boot in addition to its schedule.
    """
    if not job.runs_on("linux"):
        raise ValueError(
            f"{job.name} does not list linux in platforms, so it has no systemd unit"
        )
    lines = _service_body(job, directory)
    if not needs_timer(job):
        lines += ["", "[Install]", f"WantedBy={_wanted_by(job)}"]
    return "\n".join(lines) + "\n"


def needs_timer(job: Job) -> bool:
    return bool(job.schedule.every_seconds or job.schedule.calendar)


def _wanted_by(job: Job) -> str:
    return "multi-user.target" if job.scope == "system" else "default.target"


def render_timer(job: Job) -> str | None:
    """The `.timer` unit, or None for a job that has no schedule."""
    if not needs_timer(job):
        return None
    lines = [
        "[Unit]",
        f"Description=Timer for {_specifiers(job.description.strip().splitlines()[0])}",
        "",
        "[Timer]",
    ]
    if job.schedule.every_seconds is not None:
        # From the last START, matching launchd's StartInterval. See the module
        # docstring for why OnUnitInactiveSec would drift.
        lines.append(f"OnUnitActiveSec={job.schedule.every_seconds}")
        if job.schedule.at_load:
            lines.append("OnActiveSec=0")
        else:
            # Without this the first firing waits for one full interval after
            # the timer starts, which for the hourly jobs means an hour of
            # nothing after a reboot.
            lines.append(f"OnActiveSec={job.schedule.every_seconds}")
    for time in job.schedule.calendar:
        lines.append(f"OnCalendar={on_calendar(time)}")
    if job.schedule.calendar:
        lines.append("Persistent=true")
        if job.schedule.at_load:
            lines.append("OnActiveSec=0")
    lines += ["", "[Install]", "WantedBy=timers.target"]
    return "\n".join(lines) + "\n"


def unit_directory(job: Job, home: str) -> str:
    """Where this job's units belong on a Linux machine."""
    if job.scope == "system":
        return "/etc/systemd/system"
    return f"{home}/.config/systemd/user"


def render(job: Job, directory: accounts.Directory = accounts.lookup) -> dict[str, str]:
    """Every unit file for this job, keyed by filename."""
    units = {f"{job.label}.service": render_service(job, directory)}
    timer = render_timer(job)
    if timer is not None:
        units[f"{job.label}.timer"] = timer
    return units
