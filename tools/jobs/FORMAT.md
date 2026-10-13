# The Builder backend job declaration format

**This describes the format as designed.** The renderers in this directory produce launchd property
lists and systemd units from it today, and the round-trip tests measure it against an existing
deployment's backend jobs. `bin/install-jobs` reads a directory of these and installs them, and
`bin/stand-up-backend` runs it as the supervision step.

A backend job is declared once, in a TOML file, and the installer renders it as a launchd property
list on macOS or a systemd service and timer on Linux. The alternative is a unit written beside
every property list, which would be two versions of the schedule within a month.

## Why TOML

The installer parses declarations on a machine where nothing has been installed yet. `tomllib` has
been in the Python standard library since 3.11, which the installer provisions anyway, so reading a
declaration costs no dependency. PyYAML would be a bootstrap dependency for the one file that has to
be read before dependencies exist.

**This puts the parser downstream of the Python 3.11 provisioning step, and that was measured rather
than assumed.** Ubuntu 22.04 ships Python 3.10, which has no `tomllib`: on a stock 22.04 container
both test suites fail at import with `ModuleNotFoundError: No module named 'tomllib'`, and both pass
once 3.11 is installed. So whatever reads a declaration runs under the provisioned interpreter, and
an installer stage that ran under `/usr/bin/python3` on 22.04 could not read one at all.

## A declaration

```toml
name = "knowledge-watcher"
description = "Reindexes the Reference Room when a document changes on disk."
label = "com.convivy.knowledge-watcher"
command = ["{python}", "{deploy}/agent-platform-shared/bin/knowledge-watcher"]
platforms = ["macos", "linux"]
scope = "user"
enabled-by-default = true
working-directory = "{root}/knowledge"

[log]
stdout = "{state}/knowledge-watcher.log"
stderr = "{state}/knowledge-watcher.log"

[environment]
PATH = "{bin}:/usr/bin:/bin"

[schedule]
at-load = true

[restart]
policy = "always"
delay-seconds = 10
```

### Fields

| field | meaning |
|---|---|
| `name` | short name, unique within a repository's job directory |
| `description` | what the job does, in a sentence; an operator reads this when deciding whether to enable it |
| `command` | argv as a list, never a shell line |
| `label` | the supervisor's identifier; defaults to `name` |
| `platforms` | `["macos", "linux"]` by default; a job listing one platform renders only there |
| `scope` | `user` or `system`; decides LaunchAgents against LaunchDaemons, and a user unit against a system one |
| `enabled-by-default` | whether a fresh install starts this job |
| `working-directory` | optional |
| `[log]` | `stdout` and `stderr` paths; both optional. On a two-account install a system-scope job that runs as an account ignores them and logs to `/opt/builder/var/log/<label>.out` and `<label>.err` |
| `[environment]` | string to string |
| `[schedule]` | `at-load`, `every-seconds`, and `[[schedule.calendar]]` entries |
| `[restart]` | `policy` of `always`, `on-failure` or `never`, and `delay-seconds` |
| `directories` | optional list of directories the installer creates, at mode 700, before the job first starts |
| `prepare` | optional list of commands, each argv as a list or a table `{ run = [...], creates = "path" }`, that the installer runs in order on every real install |
| `stop-timeout-seconds` | optional; how long the supervisor waits after asking the job to stop before it kills it |
| `programs` | optional list of command names the installer finds on its own PATH; see "Placeholders" |
| `[macos]` | optional, for a job whose `platforms` is exactly `["macos"]`: `abandon-process-group` |
| `account` | optional, for a system-scope job: the account it runs as instead of root; see "account" |

### directories and prepare

Some jobs need state that exists before they first start, and only the job's own declaration
knows where it goes. The Library's is a database that has to be created and migrated, then given its
vector tables, at the path its `LIBRARY_DB` names.

`install-jobs` handles both on every real install, before it writes any unit, so a failure leaves
the machine as it was. It creates each directory without following a symlink, at mode 700, the way it
creates log directories. It then runs each `prepare` command in the job's `working-directory`, with
exactly the job's `[environment]` and nothing inherited from the installer, so a step sees what the
service will see. A command that fails stops the install, which exits 2 and names it. Each command
therefore has to be safe to run again, because a re-install runs it again. `--dry-run` prints what it
would create and run.

A step that must run only once names the path it makes, and is skipped while that path exists:

```toml
prepare = [
    ["{deploy}/tool/.venv/bin/python", "migrate.py"],
    { run = ["{deploy}/tool/.venv/bin/python", "mint.py", "--out", "{home}/.tool/token"], creates = "{home}/.tool/token" },
]
```

The installer checks `creates` before each run, reading a relative path from the job's
`working-directory`, and prints the skip. It checks only that the path exists, so the step itself still
has to refuse to damage anything it finds half-made. The Library's credential mints are the case this
exists for: an install may generate a new local credential and never overwrite one.

Both are for user-scope jobs, and for system-scope jobs that name an `account`. A system-scope job with
no account is installed as root, so its steps would run as root on every install; the parser refuses
that. A job that names an account has its directories handed to the account and its steps run as that
account, so a database or credential a step creates belongs to the account and not to root. `prepare`
needs a `working-directory`. A step with no working directory would run wherever the installer was
invoked from.

### stop-timeout-seconds

A job that drains work when told to stop needs the supervisor to wait for it. launchd renders this
as `ExitTimeOut`, with a capital O; without it launchd uses a system-defined default, which
`launchctl print` reads as 5 seconds on a current Mac. systemd renders it as `TimeoutStopSec=`, and
defaults to 90. launchd ignores a misspelled `ExitTimeout` without a word, which is
why the renderer's test checks the exact key. The Library sets 60, above its own 50-second drain.

### [macos]

```toml
platforms = ["macos"]

[macos]
abandon-process-group = true
```

`abandon-process-group` renders as launchd's `AbandonProcessGroup`. launchd kills what is left in a
job's process group when the job exits, which is right for almost every job and wrong for one whose
command starts a server and exits, such as the tmux keeper. The table is refused on a job that also
runs on Linux, because no systemd unit renders it and the job would behave differently on the two
platforms with nothing in the declaration to show it.

### account

```toml
scope = "system"
account = "agents"
```

A system-scope job runs as root unless it names an account. With one, launchd renders `UserName`,
`GroupName` (the account's primary group), `Umask` 027 and `HOME` in `EnvironmentVariables`, and
systemd renders `User=`, `Group=` and `UMask=0027`; systemd sets `HOME` itself from `User=`. The job
still installs to `/Library/LaunchDaemons` or `/etc/systemd/system`, so root installs it and the account
cannot rewrite it.

`{home}`, `{deploy}`, `{state}` and `{bin}` resolve against the named account's home, read from the
directory service at render time (`getpwnam`, which `dscl .` and `getent passwd` also read), so no home
path appears in a declaration or in the installer. `{root}` and `{python}` carry over from the install:
`--root` names the Builder root, and a run as root never asks `builder-root`, so a root install of a job
using `{root}` needs `--root`. A render for an account the directory service does not have stops and
says to run `provision-accounts`.

`account` on a user-scope job is refused, since that job already runs as the account that installed it.
A system-scope job without one renders as before and runs as root. A system-scope job with one runs its
`directories` and `prepare` steps as that account, under root's install. `jobs-lint import` reads `UserName`
from a property list as `account` on a system-scope job.

A run as root leaves out a user-scope job that names no account. The two-account shape runs `install-jobs`
as root with `--home` set to the agents account's home, so such a job would be written there. `install-jobs`
names each job it leaves out and installs nothing for it. `--single-account` installs it for the operator.

### Calendar times

```toml
[[schedule.calendar]]
weekday = "sunday"
hour = 3
minute = 0
```

A field left out means every value of it, so `minute = 2` alone fires at two minutes past every hour.
Several `[[schedule.calendar]]` entries give a job several firing times.

**Weekdays and months are names and never numbers.** launchd numbers Sunday 0 and also accepts 7,
cron agrees, systemd uses names, and Python's `date.weekday()` numbers Monday 0. A weekly job on
Sunday is common, so a renderer reading the number through the wrong convention would move a
weekly job by a day with nothing to report it.

**The format is not cron, for one specific reason.** In cron, when day-of-month and day-of-week are
both restricted the job runs when *either* matches; launchd ANDs every field it is given. A format
that looked like cron would carry that disagreement into the renderers, where it would show up as a
job firing on days nobody asked for. Setting both `day` and `weekday` is refused rather than resolved.

## Placeholders

A job imported from one machine names its home directory or `/opt/homebrew` in its argv,
environment or log paths, often many times over. That is the relocatability release gate
showing up inside the supervision layer. A declaration writes a placeholder and the installer
resolves it:

`{home}` `{root}` `{deploy}` `{state}` `{bin}` `{python}`

`jobs-lint check` reports a path that names one machine: a home directory under `/Users` or `/home`,
and Homebrew at either prefix, `/opt/homebrew` on Apple Silicon and `/usr/local/Cellar` or
`/usr/local/opt` on Intel. Bare `/usr/local/bin` and `/usr/local/sbin` are not reported, because they
are ordinary Linux locations where a job may legitimately run a system program.

**An unknown placeholder stops the install and names the typo.** Rendered literally, `{depoly}`
produces a job whose argv points at a path that cannot exist, and a job that cannot exec looks from
the outside exactly like a job that ran and did nothing, and can fail that way for weeks unnoticed.

The set is closed. Every entry is a directory whose location genuinely differs between a macOS and a
Linux install; anything else a job needs goes in `[environment]`, where a reader can see the value.

**A job may add one kind of placeholder of its own, a program it names in `programs`.**

```toml
command = ["{tmux}", "new-session", "-d", "-s", "keeper"]
programs = ["tmux"]
```

The installer looks each one up on its own PATH and writes the absolute path into the unit. That is
the only place it can be found: Homebrew installs to a different prefix on Apple Silicon and on Intel,
the lint refuses both, and launchd starts a job with a PATH that holds neither. The operator's shell,
which runs the installer, does. A program that is not found stops the install before anything is
written, and the install prints each path it resolved. `{tmux}` is known only in a declaration that
lists `tmux`. A name must be a bare command in the placeholder's own shape, so a path cannot pass for
one, and it may not reuse a built-in placeholder's name. `programs` is for user-scope jobs only,
because a system-scope job runs as root and a program found on PATH could be one another account
placed.

## What each renderer does about the two supervisors disagreeing

Each of these is a place where a faithful-looking translation would change when a job runs.

- **An interval is measured from a different moment.** launchd's `StartInterval` counts from the last
  time the job was started; systemd's `OnUnitInactiveSec` counts from the last time it finished,
  which turns a 15-minute interval into a 17-minute one for a job that takes two minutes. The
  renderer emits `OnUnitActiveSec`, which counts from the last start.
- **A missed firing is not missed the same way.** `launchd.plist(5)`: "Unlike cron which skips job
  invocations when the computer is asleep, launchd will start the job the next time the computer
  wakes up." systemd drops it unless the timer says `Persistent=true`, so every calendar timer sets
  that. Without it, a backend on a machine that sleeps would silently skip the nightly jobs.
- **Running at load is not a schedule.** launchd's `RunAtLoad` on a job that also has an interval
  means "and also once, now". The timer equivalent is `OnActiveSec=0`.
- **Output goes to the journal by default.** `append:` keeps the declaration's log paths, so a runbook
  that says to read a file keeps working on both platforms.
- **A service with a timer gets no `[Install]` section.** The timer pulls it in; a service also
  `WantedBy` a target would run once at every boot on top of its schedule.

## What a declaration is not allowed to contain, and why

A declaration becomes an executable supervisor unit, and for a `system`-scope job that unit runs as
root. So the parser is the fence, in one place, rather than each renderer being trusted to escape
correctly.

- **No control character** in a command part, the working directory, a log path, the label, the
  description, or an environment key or value. A systemd unit is line-oriented, so a newline inside a
  value ends the directive and systemd parses what follows as a new one. Measured: a working
  directory of `/tmp\nZZUnknownProbeKey=1` renders a unit whose injected line `systemd-analyze
  verify` reports as `Unknown key name 'ZZUnknownProbeKey'`. Without the fence a declaration could add
  `ExecStartPost=` or `User=`.
- **No backslash** in the working directory, a log path, or the description. systemd writes those
  unquoted and reads a trailing backslash as a line continuation, which silently swallows the next
  directive. Measured: the probe key above goes unreported when the preceding value ends in a
  backslash, and is reported when it does not. The swallowed line could be the `Restart=` that
  supervises a service. **Line continuation is a property of systemd's parser over every directive**,
  not of a fixed list of fields — `Description=` was left out of this fence when the other three were
  added, on the mistaken basis that the list was complete, and a test now pins the blank line that
  currently sits after `Description=` so a refactor cannot quietly re-open it either.
- **An environment key must be a variable name**, `[A-Za-z_][A-Za-z0-9_]*`. systemd does not quote the
  key side of `Environment="KEY=VALUE"`, and a key that is not a variable name goes wrong silently in
  two ways, both measured: a key containing a space draws `Invalid environment assignment, ignoring`
  and the variable is dropped, so the job runs without something it declared; and a key containing
  `=` is accepted and sets a *different* variable (`A=B` with value `v` sets `A` to `B=v`). A key
  containing a quote would break out of the assignment entirely. The value side needs no such rule:
  systemd treats the whole quoted string as one assignment, confirmed by checking that
  `Environment="A=1 B"` draws no complaint about a stray `B`.
- **A label matches `[A-Za-z0-9][A-Za-z0-9._-]*`**, because it becomes a filename in LaunchAgents,
  LaunchDaemons or a systemd unit directory. A label of `../../etc/cron.d/evil` would otherwise
  resolve outside the supervisor's directory, written by root for a system-scope job.
- **Literal percent signs are escaped for systemd, and left alone for launchd.** systemd expands
  `%h`, `%H` and friends in `Description=`, `ExecStart=`, `Environment=`, `WorkingDirectory=` and the
  log paths; launchd has no specifiers. So a description reading "disk usage exceeds 90%" would mean
  different things on the two platforms. Measured: `%z`, which is not a valid specifier, draws
  `Failed to resolve unit specifiers ... Invalid slot` and is fatal in the working directory.

## Two things the declaration carries that exist only as loose lists today

**Which jobs are system-domain.** Kept as a hardcoded list of the property lists that install to
`/Library/LaunchDaemons`, it has nothing to cross-check it against, so one added without editing
that list lands in LaunchAgents as an inert copy. `scope` is a field on the job and cannot fall
out of step with it.

**Which jobs a fresh install should start.** Copying a property list into LaunchAgents does not run
it; only `launchctl bootstrap` does. A hardcoded list of jobs to activate falls behind, and a job
added after it was last edited installs inert with nothing reporting it. `enabled-by-default` is
read from the same file the job is.

## How this was checked

`tools/test_jobs.py` is the format and renderer suite, stdlib only. `tools/test_jobs_systemd.py`
hands the generated units to systemd itself and runs on Linux.

- **Every existing property list round-trips.** Each is imported, written as TOML, read back and
  rendered, and the result must match what it started as. Where the property lists are present the
  suite fails if too few are found, so a missing checkout cannot pass by collecting nothing, and it
  says in its output which corpus it read and how many. Where they are absent, as in CI, it runs the
  committed fixtures alone, which cover every shape in the corpus.

  **Counts are not repeated in this document.** They went stale twice during the review of this
  change, once in the same commit that added the fixture making them wrong. The suites print theirs.
- **Both suites pass on Ubuntu 22.04 with systemd 249 and Python 3.11**, which is the platform the
  Linux half is for rather than a convenient neighbour, and again on the CI runner's systemd 255.
  Every fixture's units pass `systemd-analyze verify`, and all eight launchd weekday numbers,
  including the 7 that also means Sunday, resolve to the day they name according to
  `systemd-analyze calendar`.
- **The launchd half is checked the same way**, against `plutil`, which is the parser macOS itself
  uses. Until that was added it was the weaker half: the property lists were only ever compared with
  property lists this renderer had already read. Builder's backend runs on macOS and Linux, which
  requires a repository with a platform branch to test on both platforms in CI, so the suites run
  on `macos-latest` as well as `ubuntu-latest`.
- **Both harnesses prove they can fail before they report a pass.** The round-trip check is run
  against a property list carrying an unsupported key and must refuse it. The unit verifier filters
  this machine's own noise out of its output, so it is first run against three planted units, an
  unknown key, an unparseable calendar and a bad service type, and the suite fails if the filter
  calls any of them clean. `systemd-analyze calendar` is separately handed a nonsense expression and
  must reject it.
- **Every distinct calendar expression in the corpus was accepted by systemd 249**, normalizing
  to itself.
- **The percent escaping is checked against systemd with a control.** A declaration full of literal
  percents must render units systemd accepts, and the same unit with the escaping undone must fail,
  so the test cannot pass whether or not the escaping works.

The importer refuses any launchd key outside the set it understands. A dropped `KeepAlive` would turn
a supervised service into a one-shot that dies for good on its first crash, and the declaration would
give a reader no sign anything was lost.

## What ships, and what has not been done

**`jobs/` holds Builder's own backend declarations**, the ones an adopter's backend needs.
`bin/install-jobs` defaults `--jobs` to that directory, so a clean checkout installs them with no
argument. Six are `enabled-by-default`: the Library, Orient, the two
knowledge jobs that keep the Reference Room current, the scheduled backup, and on macOS the tmux
keeper, which lets crews started over SSH use the desktop login's Keychain. The rest install without starting, because a
reporting job on a fresh machine is noise rather than a backend that runs.

**These were imported from an existing deployment's launchd jobs and then changed in three ways**,
none of which a round-trip against the original would preserve, so the round-trip check is not
what guards them:

- **Paths became placeholders.** Log and state paths that named one machine's directories now
  sit under `{state}`, which the installer resolves to `~/.local/state`.
- **Every label ships as `com.convivy.*`.** A label carrying the name of whoever first wrote the
  job means nothing on an adopter's machine.

  **Installing these where the originals run is not a no-op.** A declaration whose label matches
  an original overwrites that property list; a renamed one installs beside it.

  **That also puts a limit on the lost-key comparison below.** It reads the original property
  lists, so once an install has overwritten them it compares each declaration against its own
  output and cannot fail. It checks the conversion until the conversion is installed, and is not a
  standing guard.
- **`PATH` lost `/opt/homebrew`**, which does not exist on Linux at all.

`tools/test_install_jobs.py`'s "the shipped declarations" section is what checks them: that each
parses, names no machine-specific path, carries a written description rather than the importer's
placeholder, renders non-empty units on both platforms, and leaves no placeholder unsubstituted.

**Converting any other jobs is the work of whoever owns them**, against this format.
`tools/jobs-lint check` is what an owner runs to see whether a conversion is complete; it reports
a declaration that will not parse separately from one that parses but names one machine's
filesystem, because those are fixed differently.

**The LLM gateway and the run-register API are declared too**, now that `bin/install-backend`
places the code they run. Neither starts on a fresh install: the gateway refuses to start until the
operator has written its secrets file, and the run register is a reporting service.
