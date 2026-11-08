# Installing Builder

_Last checked against Builder 0.7.0, on 2026-11-02._

These pages install Builder's current release; the first public release was 0.6.0, and [the release
notes](release-notes.md) say what each release changed. Builder ships from five public
repositories, each cloned at its `stable` branch: `shipwright`, `agent-platform`, `library`,
`convivy-orient` and `convivy-deck`. A sixth, `write-better`, ships no release of its own; each
release's signed manifest names the commit it is installed at. [Before you start](#before-you-start)
shows how to clone all six.

Every command and message on these pages was run and seen on a test machine, except where a page
says it was not. On Debian, that machine had nothing of Builder's on it beforehand, and a newcomer
given only these pages used it to go from that empty machine to a crew whose session built a working
tool.

The [install checklist](install-checklist.md) lists every step on these pages as a single page of
checkboxes, if you would rather tick each one off than read the pages in order.

## The one command

On the machine that will run the sessions, run:

```
curl -fsSL https://convivybuilder.org/install.sh | sh
```

It checks for `git`, Python 3.11, Claude Code and, on a Mac, `tmux`, and installs what it can before
naming what is still missing. On Linux, with an account that can use `sudo`, it installs `git`,
Python 3.11, `curl` and `ca-certificates` with `apt-get`, asking for your password once. On a Mac
with Homebrew already there, it installs `git`, Python 3.11 and `tmux` with `brew install`, as your
own account, never as an administrator. On a Mac with no Homebrew but an administrator account at
the keyboard, it runs Homebrew's own installer first, which also brings Apple's Command Line Tools,
then finishes with `brew install`; without a terminal for that installer to ask its password and
confirmation at, it leaves this to you and says so. Claude Code installs the same way on either
platform, with `claude.ai`'s own script, never through `sudo`. Two things still need a person
whatever the platform: an account with no administrator rights and no Homebrew has no route the
install can take, and signing in to Claude Code by running `claude` once stays something only you
can do. The install's closing lines ask for that sign-in when they installed Claude Code itself.

Once it has installed what it can, it names anything still missing along with how to get it. It
then clones the six repositories below into `~/src` and runs the backend's installers in order:
`provision-backend`, `install-payload` and `stand-up-backend`. Everything past the prerequisite step
runs as your own account; on a Mac nothing ever asks for an administrator's password. Running it
again finishes or repairs an install, and changes nothing that is already there.

Before any installer runs, the install checks that the release is one Convivy signed. It fetches the
release's signed manifest and checks the signature against the release keys this copy trusts: those
built into the one-line install script, or, for the Homebrew copy, those shipped beside it from the
same archive. It then checks the commit of each of the six repositories and the sha256 of the
release archive against what the manifest names, and it runs no installer unless every check
passes. No option, environment variable or prompt skips the check. The Homebrew copy pinned to
0.7.0 predates the check, so after a Homebrew install of 0.7.0, check its clones with `--verify`. The install also clones
`write-better` at the commit the manifest names, rather than at its `main`, so a later change to
`write-better` does not stop an older release installing.

A copy of the installer run from a git checkout refuses with `could not check`, because the trusted
keys in a checkout cannot vouch for the checkout they sit in. Use the one-line install from the
site instead, or check clones you made by hand with the site's script:
`curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --verify vX.Y.Z`, naming the release
you want checked.

A failed check ends the install before any installer runs, leaving the machine as it was. The
message says which check failed, and the exit status says what kind. **1** means the release is not
one Convivy signed: the signature did not verify, or a repository or archive on disk is not what the
manifest names. Do not run Builder from those clones. **3** means the check could not run at all:
the manifest could not be fetched, `ssh-keygen` is missing, or a repository is absent. Fix that and
run the command again.

As its last step, it creates the GitHub App your agents will act through and pauses: open the
address it prints in a browser and click **Create GitHub App**, and the install finishes once
GitHub redirects back. Over SSH, where that redirect cannot reach this machine, paste the whole
address the browser was left at (`http://127.0.0.1:<port>/callback?code=...&state=...`) at the
terminal instead. Add `--no-github-app` to skip this and create the App later by hand; [Connecting
GitHub](connecting-github.md) covers both the install's own step and the manual command, and the
rest of what connects the App to your repositories.

To install the three-account shape instead of the default single account, add `--shape three`. It
needs administrator rights and one of the server platforms [Supported setups](supported-setups.md)
lists (Debian 12, Ubuntu 22.04 or macOS 26); the install checks both before changing anything and
names what is missing. It then creates the `agents` and `reviewers` accounts, the root-owned
privileged half, and the backend, each as the account that step needs, and running it again
finishes or repairs the install exactly as the single-account shape does. This shape has not been
rehearsed end to end on a real machine yet; [What works and what does not yet](install-status.md)
says so.

The `agents` account must not be able to read your home. If your home is readable by other
accounts, as it can be on a stock Debian 12, the install refuses and says so. Close it first:

```
chmod 750 ~
```

```
curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --shape three
```

On your laptop, to install Deck instead, add `--role laptop`:

```
curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --role laptop
```

The laptop needs `git`, Python 3.11 and `swift`; it needs neither Claude Code nor `tmux`. The install
installs `git` and Python 3.11 the same way it does on a server Mac — Homebrew when it is there,
Homebrew's own installer first when it is not and an administrator is at the keyboard — and `swift`
along with it, since the Command Line Tools bring both. If `swift` is still missing afterward,
install Apple's Command Line Tools yourself (`xcode-select --install`).

Once Deck is built and placed, the laptop install also sets up the ssh config Deck's crew sidebar
reads, using a tool from the `agent-platform` tree it fetched alongside Deck's own checkout. That
tool needs three things already set up on this laptop: this laptop's own operator config
naming the server's address on your private network, an ssh host alias for the server, and a
mounted share of the account that runs your crews. When any of the three is missing, Deck is
installed anyway and the install says which is missing; fixing it and running the laptop install
again is safe.

On a Mac with Homebrew, you can install the same installer through Homebrew instead, and then run
it. This has not been rehearsed: the formula is published and pins the release archive by its
sha256, but nobody has yet run `brew install` on a clean Mac.

```
brew install convivybuilder/tap/builder
builder-install
```

On your laptop, run `builder-install --role laptop` instead. Homebrew installs only the installer,
pinned to the current release, along with Python 3.11 and `tmux`; `brew upgrade` moves it
to each new release.

The rest of this page, and the pages under [Which install is yours](#which-install-is-yours), show
the manual route: the same steps, one at a time, for anyone who wants to see or do each one
themselves, or whose machine the one command refuses on. The manual route runs each installer
directly and does not perform the release check, so check its clones with `--verify` if you want
that assurance. [What works and what does not yet](install-status.md) says how far the one command
itself has been rehearsed.

## A server, and a laptop to work from

Builder works best on two machines with different jobs.

- **A server runs the sessions.** It is a machine that stays on and stays awake: a Linux machine, a
  virtual machine in the cloud, or a Mac left plugged in somewhere. Builder's backend, its crews and
  every session they start live there. These pages install Builder on it.
- **Your laptop is where you work from.** You run Deck there, the Mac app that shows each crew and
  lets you talk to its sessions, and Deck reaches the server over SSH. The laptop runs no sessions
  of its own, so you can close it, take it with you, or switch it off.

The two machines are joined by a private network such as Tailscale, so the server needs no port
open to the internet. [How many machines Builder runs on](where-everything-runs.md) says more
about each machine's part.

**Builder is set up this way because long-lived sessions build complex projects better.** A crew's
session keeps its conversation, what it has read and what it has decided, for as long as it runs. A
large project takes many hours of agent work spread over days: designing, writing code, reviewing it
and fixing what the review finds. On a server, a session keeps that work going overnight and while
your laptop is shut, and it is still there, with everything it knew, when you open Deck again. A
session on a laptop stops whenever the laptop sleeps.

This release needs both machines. [What you need](what-you-need.md) lists them, and the account
each one needs.

[After the install](after-installing.md#meet-the-steward) gives the steps that add your server to
Deck on the laptop. They have not been rehearsed end to end yet; [What works and what does not
yet](install-status.md) says so.

## Which install is yours

Every reader starts with [Before you start](#before-you-start), below. Then follow the one page that
fits the machine that will run the sessions, and the account on it:

- **[Installing on Linux, with administrator access](install-linux.md)**, for Debian or Ubuntu when your account can install software
  for the whole machine, which on Linux means it can use `sudo`. Run `sudo -v` to find out; [Words
  these pages use](#words-these-pages-use) explains it.
- **[Installing on Linux, without administrator access](install-linux-without-sudo.md)**, for a Linux account that cannot install
  software for the whole machine, where someone else administers it.
- **[Installing on a Mac](install-mac.md)**, for any Mac, whether you administer it yourself or
  someone else does.

All three end at [After the install](after-installing.md), which shows what the install put where
and takes you to the steward and your first crew. [When something goes
wrong](#when-something-goes-wrong), at the end of this page, lists what to do when a step refuses.

## Words these pages use

The pages use two sets of words. The first set belongs to any computer.

- **A terminal** is a window where you type commands and read the answers. On a Mac it is the
  Terminal app, in Applications › Utilities. **A shell** is the program inside it that reads what
  you type. **A login shell** is a shell started by logging in, which is when it reads your
  account's settings. Logging out and back in gives you one.
- **`~`** stands for your account's home folder, so `~/src` is a folder named `src` inside it.
- **`PATH`** is the list of folders the shell searches for a command. A program is "on your `PATH`"
  when you can run it by typing its name.
- **An administrator** is an account allowed to change the whole machine, for example by
  installing programs every account can use. On Linux the all-powerful account is called **root**.
- **`sudo`** is the command an administrator types in front of another command to run that one
  command as root. `sudo apt-get install tmux`, for example, installs `tmux` for the whole machine.
  The first time in a while, `sudo` asks for your own account's password, and it works only if the
  machine's administrator has allowed your account to use it. To find out whether yours can, run
  `sudo -v`: if it asks for your password and then prints nothing, your account can use `sudo`; if
  it says your account `may not run sudo` or `is not in the sudoers file`, it cannot. A command run
  with `sudo` can change anything on the machine, which is why these pages use it once at most.
- **Git** is the tool that records every change to a folder of files. **A repository** is a folder
  it keeps that way, **to clone** one is to copy it onto your machine, **a commit** is one recorded
  change, and **`main`** is the repository's current version. **`stable`** is a branch that always
  points at the latest tagged release, so cloning it skips `main`'s unreleased edge.
- **A service** or **job** is a program that runs in the background without a window.
- **A credential** or **token** is a secret that proves to one program that another may use it.
- **tmux** is a background program that keeps terminal sessions running after you close the window.
- **SSH** is a standard way to open a terminal on another machine.

The second set is Builder's own.

- **Claude Code** is the program that lets you talk with Claude, an AI model, in a terminal. **A
  session** is one such conversation.
- **The steward** is the first session you meet. It asks what you want to build and sets up a crew.
- **A crew** is one project and everything working on it, and **a bead** is a crew's short
  description of where its project is going.
- **The Library** is where Builder keeps everything a project knows. **The Reference Room** is the
  part of it that holds what a project holds to be true, which many systems call a knowledge base.
  **Your knowledge repository** is the git repository that holds the Reference Room's documents.
- **Your install repository** is a git repository the install makes at `install` inside your Builder
  root, holding configuration that is not a secret and is not part of any one release — the registry
  of your crews and the projects they work on is its first file.
- **The work queue** is the list of pieces of work, which the Library serves.
- **Orient** is Builder's view of the whole system, and **Deck** is the Mac application you work
  from.

## Before you start

You need three things in place before the first install command.

- **A machine and account** that fit one of the three install pages above. Every route needs `git`
  and `python3`. On Linux without `sudo`, or on a Mac, the administrator's part of your install page
  provides them, so do that part first.
- **Claude Code, installed and signed in** on that account. Run `claude` once and follow its
  sign-in. On a Mac, and on Linux without `sudo`, your install page installs it in the owner's part.
- **The six repositories, cloned side by side in one folder**, as the steps below show.

### Cloning the six repositories

All six repositories are public, in the `convivybuilder` organisation on GitHub:

```
https://github.com/convivybuilder/shipwright
https://github.com/convivybuilder/agent-platform
https://github.com/convivybuilder/library
https://github.com/convivybuilder/convivy-orient
https://github.com/convivybuilder/convivy-deck
https://github.com/convivybuilder/write-better
```

`convivy-deck` builds Deck, the Mac app. Skip it if you are installing only the backend on Linux.

Clone only from addresses you trust. On Linux with `sudo`, the first install command runs this code
as root, and code run as root can change anything on the machine. On the other routes it runs as
your account and reaches everything your account holds.

1. **Open a terminal** on the machine Builder will run on, as the account Builder will run in. A new
   terminal starts in your home folder.
2. **Check that git is there.** Run `git --version`. It prints a line such as `git version 2.39.5`.
   If it says `command not found`, git is missing: install it with `sudo apt-get install git` on
   Linux with `sudo`, or ask the machine's administrator, whose part of your install page installs
   it.
3. **Make the folder the repositories will sit in, and move into it.** These pages use `~/src`:

   ```
   mkdir -p ~/src
   cd ~/src
   ```

4. **Clone the five released repositories at their `stable` branch**, which checks out the latest
   release. Run the five lines one at a time. Each prints `Cloning into '<name>'...` and takes a few
   seconds:

   ```
   git clone --branch stable https://github.com/convivybuilder/shipwright
   git clone --branch stable https://github.com/convivybuilder/agent-platform
   git clone --branch stable https://github.com/convivybuilder/library
   git clone --branch stable https://github.com/convivybuilder/convivy-orient
   git clone --branch stable https://github.com/convivybuilder/convivy-deck
   ```

5. **Clone `write-better`**, which ships no release and has no `stable` branch:

   ```
   git clone https://github.com/convivybuilder/write-better
   ```

6. **Check the result.** Run `ls ~/src`. It lists the six folders:

   ```
   agent-platform  convivy-deck  convivy-orient  library  shipwright  write-better
   ```

7. **Go back to your home folder** with `cd`, since the install commands are written to run from
   there.

If a clone stops with `Repository not found` or `Could not resolve host`, check the address for a
typing mistake and that the machine can reach github.com, then run that one line again. If it stops
with `destination path '<name>' already exists`, that repository is already cloned and you can go
on to the next line.

Now follow your install page from [Which install is yours](#which-install-is-yours).

## When something goes wrong

Each installer refuses rather than doing half a job, and says what it refused. A refusal leaves what
was already installed as it was, and you can run the step again once the cause is fixed. Each
heading is the message or symptom you will see, so find yours and read only that part.

### `provision-backend` says `apt-get update failed` and `sudo: a password is required`

The command ran without `sudo` somewhere `sudo` could not ask for a password. On the first install,
before any crew exists, run it with `sudo` in front, as [Installing on Linux, with administrator access](install-linux.md#run-the-install) does. After that, never
run it as root: install the package it names with `sudo apt-get install <package>`, then run
`provision-backend --no-install` without `sudo` to check that nothing else is missing.

### `install-backend: no checkout for library under ~/src`

One of the five repositories is missing from the folder beside `shipwright`. The message names it.
Clone it there and run `stand-up-backend` again. The install looks for all five in the folder that
holds `shipwright`.

### `link-commands: 1 destination(s) hold something this did not put there`

A file already exists in `~/.local/bin` under the name of one of Builder's commands, and the install
will not replace a file it did not make. The message names the file. Move it somewhere else, then
run `stand-up-backend` again. The message names a second cause as well: the files can be the
install's own earlier links, if its deploy folder is now named by a different path. The targets the
message lists say which, and moving them aside fixes that case too.

### `link-commands: ~/.local/bin is NOT on PATH`

The commands are linked but your shell does not look in that folder. Log out and back in first: on
Debian and Ubuntu, a login shell adds `~/.local/bin` once the folder exists. If `command -v co` still
prints nothing, add this line to `~/.profile`, or on a Mac to `~/.zprofile`:

```
export PATH="$HOME/.local/bin:$PATH"
```

The install also adds a line to `~/.bashrc` (bash) or `~/.zshenv` (zsh) so a command run over ssh,
which never reads `~/.profile` or `~/.zprofile`, finds `~/.local/bin` too.

### A skill is missing from a session

Two commands link skills. List what each one linked:

```
sh ~/src/shipwright/bin/install-payload --status
python3 ~/src/shipwright/bin/link-commands --status
```

Between them they should show nine: `install-payload` links `new-crew`, `new-subcrew`,
`take-upstream`, `write-bead`, `rollover`, `handoff-pickup` and `handoff-leave`, and `link-commands`
links `write-better` and `talk-better`. The first command's
`live paths` list shows every skill in `~/.claude/skills`, whichever command linked it. If one is
missing, run the command that links it again without `--status`, which puts it back, then start a
new session: a session already running keeps the skills it started with.

### `install-payload: refusing to install a payload with symlinks in it`

The `payload/` folder of your `shipwright` clone's `main` holds a symbolic link, a file that points
at another file. The whole payload is copied into the install, and a link there would serve
whatever it points at on this machine as if Builder had shipped it, so the install refuses and keeps
the version already installed. The lines before the message list each link. Replace each one with
the file it points at, commit, and run `install-payload` again.

### The install says jobs `were started and are not running`

The message names each job and its log. To see a service's state and its recent output on Linux:

```
# single-account install
systemctl --user status com.convivy.library.service
tail ~/.local/state/library.log

# three-account install
systemctl status com.convivy.library.service
tail /opt/builder/var/log/com.convivy.library.out
```

On a three-account install the log belongs to `agents` and its group, which the install adds your account
to. A terminal session you opened before the install does not have that group yet, so `tail` there
answers `Permission denied`; log out and back in, or open a new login session, and it reads the log.

The install checks each job once, straight after starting it, so a job that runs for a moment before
stopping can be missed there. `systemctl --user list-units 'com.convivy*'` shows every job's state
at any time on a single-account install, and `systemctl list-units 'com.convivy*'` on a three-account
one. On a Mac, `launchctl print gui/$(id -u)/com.convivy.library` shows a job's `state`, `pid`,
`last exit code` and log path on a single-account install, and `launchctl print
system/com.convivy.library` on a three-account one. Orient's log can start with `preflight FAILED,
build.load_docs() cannot reach the Library` from its first seconds, while the Library was still
starting. A later `preflight ok` means it recovered.

### The install stops at `mint_credential.py`, saying `already has a credential`

One of the seven credential files in `~/.orient-control`, or the Bosun's in `~/.local/state/library`, is gone, and the Library still has the
credential it matched. The install will not replace a
credential, so it stops and changes nothing. If you have the file, put it back. If not, replace the
credential. The commands below restart Orient with `systemctl --user`, so they are for a single-account install
on Linux; on a three-account install the files are in the `agents` account's home and Orient runs at
system scope. Replace `library-token` with its grant, since a replacement without `--grants` would
lose it:

```
cd ~/.local/deploy/library
LIBRARY_API_TOKENS=~/.local/state/library/api-tokens.json .venv/bin/python mint_credential.py --file agents --name orient --grants registry.read --out ~/.orient-control/library-token --replace
systemctl --user restart com.convivy.orient.service
```

For `library-client-token`, use `LIBRARY_CLIENT_TOKENS=~/.local/state/library/client-tokens.json`,
`--file clients`, `--name orient` and `--out ~/.orient-control/library-client-token`. For
`ops-mcp-token`, keep `--file agents` and use `--name ops-mcp --out
~/.orient-control/ops-mcp-token`. Replace `agent-platform-token` with its grant, since a replacement
without `--grants` would lose it, and with no restart:

```
cd ~/.local/deploy/library
LIBRARY_API_TOKENS=~/.local/state/library/api-tokens.json .venv/bin/python mint_credential.py --file agents --name agent-platform --grants review_record.create --out ~/.orient-control/agent-platform-token --replace
```

Replace `agent-platform-registry-reader-token` the same way, with its own grant and no restart:

```
cd ~/.local/deploy/library
LIBRARY_API_TOKENS=~/.local/state/library/api-tokens.json .venv/bin/python mint_credential.py --file agents --name agent-platform-registry-reader --grants registry.read --out ~/.orient-control/agent-platform-registry-reader-token --replace
```

Replace `agent-platform-registry-writer-token` the same way. It takes `--kind registrar` in place of a grant, and needs no restart:

```
cd ~/.local/deploy/library
LIBRARY_API_TOKENS=~/.local/state/library/api-tokens.json .venv/bin/python mint_credential.py --file agents --name agent-platform-registry-writer --kind registrar --out ~/.orient-control/agent-platform-registry-writer-token --replace
```

For `deck-library-token`, use the same `LIBRARY_CLIENT_TOKENS`, `--file clients`, `--name deck` and
`--out ~/.orient-control/deck-library-token`, with no restart. An install from before 0.7.0 that
holds a `deck` credential and no file stops here when it moves to 0.7.0, and its message prints this
command.

The eighth credential, the Bosun's, lives at `~/.local/state/library/bosun-client-token`; replace
it with
`--file clients --name bosun --holds-reserved= --out ~/.local/state/library/bosun-client-token`
and the same `LIBRARY_CLIENT_TOKENS`, with no restart. `--holds-reserved=` is left empty on purpose,
as the install leaves it: the Bosun acts for no person, so it holds none of the capabilities
reserved for one, such as approving. When the command finishes, the old token no longer works.

If the command is interrupted, the old token can be left in a backup beside the credential file,
such as `~/.orient-control/ops-mcp-token.mint-backup`, and it still works. The next run refuses with
`a stale backup already exists`. Move the backup aside, for example by adding the date to its name,
and run the command again. Delete it only once the new credential works, since it may hold the only
copy of a working token.

**A crew's own `ops-<crew>-token` or `ops-co-<crew>-token` refuses the same way, with the store
already holding a credential of that name and no file to show for it.** Run `mint-crew-ops-credentials`
again rather than minting by hand: it reports every pair this way and prints the exact `--replace`
command for each one it cannot complete, naming the crew, the file and the grant.

### `claude mcp list` shows `kb` and `ops` as connected, and their tools fail

`Connected` means only that the two tool servers started. These are the programs that give
Claude Code its `kb` tools, for the Reference Room, and its `ops` tools, for the work queue. The
`ops` tools need a per-crew file, which `co` and `agentctl` each point at a different name for the
same crew — `ops-co-<crew>-token` in `~/.orient-control` for a crew's own session,
`ops-<crew>-token` there for a run dispatched into it. If the `ops` tools refuse to connect, run
`mint-crew-ops-credentials` to mint whichever of the two is missing; it changes nothing that is
already there.

## Where to go next

- **[After the install](after-installing.md)** shows what the install put where and takes you to the steward.
- **[Getting started](getting-started.md)** describes a first week with the steward.
- **[How Builder works](how-builder-works.md)** explains the parts the install put in place.
- **[The glossary](glossary.md)** explains each word Builder uses.

Last, read [What works and what does not yet](install-status.md), which lists what Builder has been
seen doing on each test machine, and what it cannot do yet.
