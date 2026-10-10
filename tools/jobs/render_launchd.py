"""Render a job declaration as a launchd property list.

launchd is macOS's supervisor. A property list produced here is what
`launchctl bootstrap` loads, and it goes to `~/Library/LaunchAgents` for a
`user`-scope job or `/Library/LaunchDaemons` for a `system`-scope one.

The scope decides the destination, and that is the point of carrying it in
the declaration. Kept anywhere else, as a hardcoded list of system-domain
property lists, it has nothing to cross-check it against, so a system daemon
added without editing that list lands in LaunchAgents as an inert copy. A
field on the job cannot fall out of step with the job.
"""

from __future__ import annotations

import plistlib

from . import accounts
from .declaration import MONTHS, WEEKDAYS, CalendarTime, Job

# launchd numbers Sunday 0. The declaration writes the name, so this table is
# the only place the number appears, and it is read in one direction only.
_LAUNCHD_WEEKDAY = {name: number for number, name in enumerate(WEEKDAYS)}
_LAUNCHD_MONTH = {name: number for number, name in enumerate(MONTHS, start=1)}


def _calendar_entry(time: CalendarTime) -> dict[str, int]:
    """One StartCalendarInterval dictionary.

    A field the declaration leaves out is left out here too, which is how
    launchd spells "every value of this field".
    """
    entry: dict[str, int] = {}
    if time.minute is not None:
        entry["Minute"] = time.minute
    if time.hour is not None:
        entry["Hour"] = time.hour
    if time.day is not None:
        entry["Day"] = time.day
    if time.month is not None:
        entry["Month"] = _LAUNCHD_MONTH[time.month]
    if time.weekday is not None:
        entry["Weekday"] = _LAUNCHD_WEEKDAY[time.weekday]
    return entry


# 027 octal: the account's group may read what the job writes, and nobody else
# may. launchd takes the mode as an integer.
ACCOUNT_UMASK = 0o027


def to_plist_dict(job: Job, directory: accounts.Directory = accounts.lookup) -> dict:
    """The property list as a dictionary, for rendering or for comparison.

    A job with an `account` reads that account from `directory` and refuses
    if it is missing.
    """
    if not job.runs_on("macos"):
        raise ValueError(
            f"{job.name} does not list macos in platforms, so it has no launchd job"
        )

    plist: dict = {
        "Label": job.label,
        "ProgramArguments": list(job.command),
    }
    environment = dict(job.environment)
    if job.account is not None:
        account = accounts.require(job.account, job.source, directory)
        plist["UserName"] = account.name
        plist["GroupName"] = account.group
        plist["Umask"] = ACCOUNT_UMASK
        # Set here so a job that reads `~` finds the account's home whatever
        # launchd chooses for a daemon's environment.
        environment["HOME"] = account.home
    if job.working_directory is not None:
        plist["WorkingDirectory"] = job.working_directory
    if environment:
        plist["EnvironmentVariables"] = environment
    if job.stdout is not None:
        plist["StandardOutPath"] = job.stdout
    if job.stderr is not None:
        plist["StandardErrorPath"] = job.stderr

    plist["RunAtLoad"] = job.schedule.at_load

    if job.schedule.every_seconds is not None:
        plist["StartInterval"] = job.schedule.every_seconds

    if job.schedule.calendar:
        entries = [_calendar_entry(t) for t in job.schedule.calendar]
        # launchd accepts one dictionary or an array of them. Existing
        # property lists use both forms, so the renderer writes the array only
        # when there is more than one time; a single-entry array and a bare
        # dictionary behave identically, and matching the existing shape keeps
        # the migration diff to the fields that actually changed.
        plist["StartCalendarInterval"] = entries[0] if len(entries) == 1 else entries

    if job.restart.policy == "always":
        plist["KeepAlive"] = True
    elif job.restart.policy == "on-failure":
        # launchd's dictionary form. `SuccessfulExit false` means "restart it
        # unless it exited 0", which is what on-failure says.
        plist["KeepAlive"] = {"SuccessfulExit": False}

    if job.restart.delay_seconds is not None:
        plist["ThrottleInterval"] = job.restart.delay_seconds

    # CAPITAL O. launchd ignores `ExitTimeout` without a word, so a misspelling
    # here would render a key that reads as set and never takes effect.
    if job.stop_timeout_seconds is not None:
        plist["ExitTimeOut"] = job.stop_timeout_seconds

    if job.abandon_process_group:
        plist["AbandonProcessGroup"] = True

    return plist


def render(job: Job, directory: accounts.Directory = accounts.lookup) -> bytes:
    return plistlib.dumps(to_plist_dict(job, directory), sort_keys=True)


def install_path(job: Job, home: str) -> str:
    """Where this job's property list belongs on a macOS machine."""
    if job.scope == "system":
        return f"/Library/LaunchDaemons/{job.label}.plist"
    return f"{home}/Library/LaunchAgents/{job.label}.plist"
