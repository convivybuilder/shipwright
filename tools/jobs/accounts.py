"""The account a system-scope job runs as, as the directory service reports it.

A system-scope job may name an `account`. The supervisor then starts it as
that account rather than as root, and its placeholders resolve against that
account's home. The home and the primary group are read from the directory
service at render time, so no home path is written into shipping code and a
declaration means the same thing on a machine whose service accounts live
somewhere else.

THE LOOKUP IS `pwd` AND `grp`, WHICH ASK THE SAME SERVICE `dscl` AND `getent`
DO. On macOS `getpwnam` is answered by opendirectoryd, the service `dscl .`
reads; on Linux it goes through NSS, which is what `getent passwd` prints.
Calling the library rather than parsing either command's output gives one
code path for both platforms.

A TEST NEVER CALLS THE REAL SERVICE. Every function that needs an account
takes a `directory` callable, and a test passes one that answers from a
table. The default is `lookup`.
"""

from __future__ import annotations

import grp
import pwd
from collections.abc import Callable
from dataclasses import dataclass

from .declaration import _check_no_backslash, _check_no_control_characters


@dataclass(frozen=True)
class Account:
    name: str
    home: str
    group: str


Directory = Callable[[str], Account | None]


class AccountMissing(ValueError):
    """A job names an account this machine does not have."""


def lookup(name: str) -> Account | None:
    """The account as the directory service has it, or None."""
    try:
        entry = pwd.getpwnam(name)
    except KeyError:
        return None
    try:
        group = grp.getgrgid(entry.pw_gid).gr_name
    except KeyError:
        # A primary group id with no group record. Rendering the number would
        # work for systemd and not for launchd's GroupName, so the account is
        # treated as not provisioned.
        return None
    return Account(name=name, home=entry.pw_dir, group=group)


def require(name: str, source: str, directory: Directory = lookup) -> Account:
    """The account, or a refusal that says how to create it.

    The group name is written into `Group=` without passing through `Job`,
    whose fences every other rendered string meets, so the directory's answer
    is fenced here the same way. The home meets them anyway once the
    placeholders resolve, and is checked here so the refusal names its source.
    """
    account = directory(name)
    if account is None:
        raise AccountMissing(
            f"{source}: the job runs as account {name!r}, which this machine's "
            f"directory service does not have. Run provision-accounts to create "
            f"it, then install again."
        )
    for field_name, value in (("group", account.group), ("home", account.home)):
        what = f"the directory service's {field_name} for account {name!r}"
        _check_no_control_characters(source, what, value)
        _check_no_backslash(source, what, value)
    return account
