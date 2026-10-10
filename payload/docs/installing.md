# Installing Builder today

This page describes installing Builder 0.6.0, the first public release. Builder ships from five
public repositories, each cloned at its `stable` branch: `shipwright`, `agent-platform`, `library`,
`convivy-orient` and `convivy-deck`. A sixth, `write-better`, ships no release and is cloned at its
own `main`. [Before you start](#before-you-start) gives each address.

This page was written before 0.6.0's first install on a machine outside this project: an install on
an employer's Mac, done after a security review of these public repositories. That install is the
release's end-to-end test, and this page is corrected once it has run. Until then, every claim below
names the rehearsal that showed it, or says that none has shown it yet.

Every command and message on this page was run and seen on a test machine, except where the page says
it was not. On Debian, that machine had nothing of Builder's on it beforehand, and a newcomer given
only this page used it to go from that empty machine to a crew whose session built a working tool.
Where a part does not work yet, the page says so.

**It has been tested on Debian 12.** The package step has also been tested on Ubuntu 22.04. The
install as one account without administrator rights,
[below](#installing-without-administrator-rights), has also been run on macOS 26.4, on a Mac its
administrator had prepared; the install with administrator rights has not been run on a clean Mac.
The page describes Linux, and that section says where a Mac differs.

This is a long page because it covers three different machines and says what to do when a step
fails. You will read only part of it. The next section tells you which part, and the one after it
explains the words the page uses.

## Which parts of this page to read

Every reader starts with [Before you start](#before-you-start). After that, the route depends on
your machine.

- **On Debian or Ubuntu, with an account that has administrator rights**, read
  [Install](#install).
- **On Debian, with an account that has no administrator rights**, read [Installing without
  administrator rights](#installing-without-administrator-rights).
- **On a Mac**, read [Preparing a Mac](#preparing-a-mac) if you administer the Mac yourself, and
  then [Installing without administrator rights](#installing-without-administrator-rights).

All three routes meet again at [What the install put where](#what-the-install-put-where), and go on
to meeting the steward and creating your first crew. The last section, [When something goes
wrong](#when-something-goes-wrong), is there to look things up in when a step refuses.

## Words this page uses

The page uses two sets of words. The first set belongs to any computer.

- **A terminal** is a window where you type commands and read the answers. **A shell** is the
  program inside it that reads what you type. **A login shell** is a shell started by logging in,
  which is when it reads your account's settings. Logging out and back in gives you one.
- **`~`** stands for your account's home folder, so `~/src` is a folder named `src` inside it.
- **`PATH`** is the list of folders the shell searches for a command. A program is "on your `PATH`"
  when you can run it by typing its name.
- **An administrator** is an account allowed to change the whole machine. On Linux the all-powerful
  account is called **root**, and **`sudo`** is the command that runs one command as root.
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
- **The work queue** is the list of pieces of work, which the Library serves.
- **Orient** is Builder's view of the whole system, and **Deck** is the Mac application you work
  from.

## What works, and what does not yet

**Working on Debian, seen in the Linux container rehearsals** (an account with no `sudo`, run
2026-09-25 and again 2026-10-02/03): `install-payload` and `stand-up-backend --shape single
--seed-registry --activate` complete.

- A crew's session can read and write its own folder, run programs and commit to git: the steward
  created a crew whose session, started by `co`, built and committed a program that runs.
- The Library, Orient, the knowledge watcher and the run register all run as systemd user services.
- No step asked for GitHub when the install had none configured.
- A missing program stops the install, names it, and installs nothing.
- Without lingering enabled, jobs stop at logout, and the install says so.

**Working on a Mac, seen in the Mac rehearsal** (a standard account with no administrator password,
macOS 26.4, run 2026-10-02/03): `install-payload` and `stand-up-backend --shape single
--seed-registry --activate` complete in a login shell.

- The services run once the account has a desktop session, opened through Screen Sharing.
- After a restart, the services return once the account logs in again, by the steps under [After the
  Mac restarts](#after-the-mac-restarts).
- A signed-in Claude session starts inside the tmux server that keeps it running, and that sign-in
  survived a restart.

Not yet seen on a Mac: the steward creating a crew whose session writes code, and Deck notifying that
the account is logged out. (Deck's Hosts window showed the account logged out, but posted no
notification of it.)

**Working with GitHub, seen in the GitHub App rehearsal** (a Debian container, a scratch repository,
run 2026-10-09): `connect-github` created the remote through the GitHub App you create for your
install, and pull requests, pushes and comments appeared under that App.

- A session over an hour old still pushed and called GitHub.
- A direct push to `main` was refused.
- In Enforced mode, an agent's pull request stayed blocked until the operator approved it, the App
  could not approve its own, and a push cleared an existing approval.
- An SSH remote was rewritten to the App, and one the App could not rewrite was refused and named.
- `github-gate --check` reported pass or fail, naming each field it checked.

This release fixes two defects that rehearsal found: GitHub's host keys are now pinned, and the check
now works when run with the App's own token. Not yet seen: Deck on a second Mac, reaching the first over SSH, with
a session started there.

**Not working yet, on any machine:**

- **A crew the steward creates cannot yet file work items.** It has no row in the projects registry.
- **Orient's pages.** Orient answers every page with `403 Forbidden`, a web server's way of
  refusing, until the way it identifies a person is built.
- **The merge check.** A merge is the acceptance of a proposed change into a project. A merge you
  start from Deck or Orient asks the Library first, and the Library approves every one, its log
  saying `merge admission STUBBED (always approves)`, so it does not yet stop a merge that nobody
  reviewed. An agent's merge takes a separate path, through `agentctl kb merge` or `agentctl docs
  merge`, and each of those refuses anything your agent policy does not permit.
- **An updater.** To move to a later release, pull `stable` in each clone, as [Install](#install)
  describes; no command does that for you.
- **A way to check that a release is genuine.** The `v0.6.0` tag and the `stable` branch are not
  signed, so a clone is only as trustworthy as your connection to GitHub and the `convivybuilder`
  organisation's control of its repositories.
- **The two-account install.** 0.6.0 installs only the single-account shape this page describes.
- **Pairing Deck with the Mac from this page.** The steps that add the Mac in Deck are not on this
  page yet.

## Before you start

You need three things in place before the first command.

- **A Debian or Ubuntu machine and an account on it that can use `sudo`.** It needs `git` and
  `python3`; the install adds everything else. For an account without `sudo`, or on a Mac, follow
  [Installing without administrator rights](#installing-without-administrator-rights) instead. That
  path still needs `git` and `python3`; the `sudo` requirement and the root warning below do not
  apply there.
- **Claude Code, installed and signed in** on that account. Run `claude` once and follow its sign-in.
  On a Mac without administrator rights, the account's owner installs it later, in that path's own
  section.
- **The six repositories, cloned side by side in one folder**: `shipwright`, `agent-platform`,
  `library`, `convivy-orient`, `convivy-deck` and `write-better`. All six are public, in the
  `convivybuilder` organisation on GitHub. `convivy-deck` builds Deck, the Mac app; skip it if you
  are installing only the backend on Linux.

  ```
  https://github.com/convivybuilder/shipwright
  https://github.com/convivybuilder/agent-platform
  https://github.com/convivybuilder/library
  https://github.com/convivybuilder/convivy-orient
  https://github.com/convivybuilder/convivy-deck
  https://github.com/convivybuilder/write-better
  ```

  Clone only from addresses you trust: the first install command runs this code as root (on the path
  without administrator rights, it runs as your account and reaches what your account holds). Code
  run as root can change anything on the machine. Clone each of the five released repositories with
  `git clone --branch stable <its address>`, which checks out the latest release instead of `main`'s
  unreleased edge. `write-better` ships no release and has no `stable` branch; clone it with
  `git clone <its address>` instead. This page uses `~/src`, and when you are done the six sit like this:

  ```
  ~/src/shipwright
  ~/src/agent-platform
  ~/src/library
  ~/src/convivy-orient
  ~/src/convivy-deck
  ~/src/write-better
  ```

## Preparing a Mac

This section is for a Mac you administer yourself. It changes three settings so that agents can
keep working with nobody at the keyboard. Each setting gives up some of the Mac's protection, so
read the warning before the steps.

The install has not yet been run on a clean Mac. If Builder will run on one, do these three things
as soon as the Mac is set up, before you clone the repositories. Then, on any Mac, skip the next
section and follow [Installing without administrator
rights](#installing-without-administrator-rights), doing both the administrator's part and the
owner's if you administer the Mac yourself. If someone else administers it, skip this section too;
that path says which of these steps still apply.

**Do this only on a Mac that stays somewhere you control.** With the screen lock off, anyone at its
keyboard reaches your account: a crew's session that runs commands without asking, and the tokens the
install creates. A Mac signed out of iCloud also cannot be located or erased with Find My, and one that logs in by
itself has FileVault off, so its disk is readable by whoever takes it. FileVault is the macOS
feature that encrypts the disk. A desktop
machine in your own space suits these settings; a laptop that travels does not.

1. **Keep the Mac out of iCloud.** When an agent's command touches iCloud, macOS puts a dialog on
   the Mac's own screen, and the work stops until someone answers it through Screen Sharing or at a
   monitor plugged into the Mac. When the setup assistant asks you to sign in with an Apple
   Account, choose **Set Up Later**. If the Mac is already signed in, sign it out:
    1. Open **System Settings** and click your name at the top of the sidebar.
    2. Click **Sign Out** at the bottom of that page, and follow the prompts.
2. **Turn off the screen lock.** Tests that open windows draw them on the Mac's screen, and while
   the screen is locked those tests fail although nothing in the code changed. Change one setting:
    1. Open **System Settings** and click **Lock Screen** in the sidebar.
    2. Set **Require password after screen saver begins or display is turned off** to **Never**.
       macOS asks for your password to confirm.

    To check it, run `sysadminctl -screenLock status` in Terminal. It prints a line that ends in
    `screenLock is off`. Check again after a macOS update. The display can still sleep.

3. **Keep someone logged in at the desktop.** Claude Code keeps its login in the macOS Keychain,
   the Mac's store of saved passwords, which a session started over SSH cannot read, and Deck
   starts crews over SSH. The install adds a
   job that starts a tmux server from the desktop login, and crews started inside it can read the
   Keychain. That job runs only while someone is logged in at the desktop, so after a restart, crews
   come up logged out until someone logs in, in person or through Screen Sharing. To have the Mac
   log in by itself:
    1. Open **System Settings**, click **Users & Groups**, and set **Automatically log in as** to
       your account.

    macOS offers automatic login only while FileVault is off, so this step also leaves the disk
    unencrypted. If you keep FileVault on, log in after each restart instead.

## Install

This section is for a Debian or Ubuntu account that can use `sudo`. On a Mac, or for an account
without `sudo`, follow [Installing without administrator
rights](#installing-without-administrator-rights) instead.

Run these three commands in order, from your home directory, which is where a new terminal window
starts. Type each line, press Return, and wait for it to finish before typing the next. The list
under the commands says what each one does.

```
sudo python3 ~/src/shipwright/bin/provision-backend
sh ~/src/shipwright/bin/install-payload
python3 ~/src/shipwright/bin/stand-up-backend --shape single --seed-registry --activate
```

Then log out and back in, or open a new login shell, so the commands the install linked are on your
`PATH`. Check with:

```
command -v co agentctl
```

which prints two paths under `~/.local/bin`. Those two lines are how you know the install worked:
`co` and `agentctl` are two of Builder's commands, and the shell has found both.

**What each command does:**

1. `provision-backend` installs the system packages Builder needs: `zsh`, `lsof`, `tmux`, `curl`,
   Python 3.11, Python's venv support, and `getfacl` from the `acl` package. It checks each one by
   running it, and changes nothing that is already present.
2. `install-payload` puts the steward, its skills and your knowledge repository in place. On a
   first install, it names the folder where you meet the steward as it places the steward there.
3. `stand-up-backend --shape single --seed-registry --activate` installs Builder as your own account,
   which is the only shape built so far. `--seed-registry` starts your projects registry, the list of your
   projects, from Builder's seed, because the source repositories carry the registry of the crews that build Builder, which
   is not yours. It places Builder's backend, links its commands and the two writing
   skills, registers the tools a session uses to reach the Library, and installs and starts the
   background services. Before the Library first starts, it creates the Library's database and two
   credentials Orient uses to reach the Library. It prints what each step did and ends with `every
   step reported success (5 of 5 ran)`.

**Run the first command as root only this once, before any crew exists.** A crew's session runs as
your account and can edit the files in `~/src`, so a later `sudo` run of that code would run
whatever a session changed as root. After the first install, install a package a newer release needs
with `sudo apt-get install` yourself, and run `provision-backend` without `sudo` and with
`--no-install`, which checks each package and names what is missing without installing anything.

The other two commands are safe to run again. A second run changes only what is missing or out of
date, and it never replaces a credential: it prints `skipped … since … exists` for each one already
there.

**To move to a later release, pull `stable` in each of the five released clones first**, with
`git -C ~/src/shipwright pull --ff-only origin stable` and the same for `agent-platform`, `library`,
`convivy-orient` and `convivy-deck`; pull `write-better`'s own `main` instead, since it has no
`stable` branch. Then run the two commands above again. Running `install-payload` from a newer
release also brings the starter set in your knowledge
repository up to that release, when the repository's remote is a folder on this machine, as the one
the install made is. A knowledge repository whose remote is hosted, on GitHub or elsewhere, is left
alone, and the install says so. The update leaves any document you changed as you have it and hands
Builder's version to the steward. [Customizing
Builder](customizing.md#when-you-install-a-newer-release) says what it does to each document. To see
what an update would change before it changes anything, run `install-payload` with `--dry-run`
first.

### What the installers print that this page does not ask you to do

The installers print more steps than this page gives. You can leave every one of them alone. None
of them is needed to meet the steward and build a first crew, which is what this page takes you
through:

- **A credentials file for the LLM gateway**, `~/.config/convivy/llm-gateway.env`. The gateway is
  a local service that lets agents use models from providers other than Anthropic. It is off by
  default, and nothing on this page uses it.
- **Checks such as `bin/register-mcp --check` and `bin/provision-backend --check`**, and a pointer to
  `bin/install-jobs --help`. `stand-up-backend` has already run the steps these check, and printed
  what each one did.
- **`claude mcp get ops`**, which asks whether the work-queue tools can reach what they need.
- **A note that Ubuntu 22.04's `python3` is version 3.10.** It does not apply on Debian 12, where
  `python3` is 3.11. This page has been tested on Ubuntu 22.04 only as far as the package step.

## Installing without administrator rights

Builder also installs into one ordinary account that cannot use `sudo`, such as an account on a work
machine, or a second person's account on a Mac someone else administers. Everything runs as that
account. These steps were run on Debian 12, in a container, by an account that could not use `sudo`
(`sudo -l -U <the account>` answered `is not allowed to run sudo`), and on macOS 26.4 by a standard
account on a Mac whose administrator is someone else, except where a step says it was not run or
was run on only one of the two.

Two people take part on this path, the machine's administrator and the owner of the account Builder
will run in. If you are both, do both parts. The path has four parts, in this order:

1. The administrator installs a few programs and, on a Mac, decides who can reach the account over
   the network.
2. The account's owner installs Claude Code and, on a Mac, logs in at the desktop and installs
   Python.
3. The owner runs the three install commands.
4. On a Mac, the owner logs in again after each restart.

A container, mentioned in the tests above, is an isolated Linux system running inside another
machine. Tailscale is a private network across your own devices, Remote Login is the Mac setting
that allows logins over SSH, and Screen Sharing is the Mac feature that shows a Mac's desktop on
another computer.

### What the machine's administrator does once

The account cannot install system packages, so someone who administers the machine installs them
first, from the list below. `provision-backend --no-install`, run later by the account, names
anything still missing; treat its output as something to read, and install only what this list
names, and never run a command it prints, since the account can change the program that prints it.
Besides installing packages, the administrator may take two further root steps, each named in the
list: `loginctl enable-linger <the account>` on Linux, and, on a Mac reached through the Tailscale
app, Tailscale's system daemon. Check the account name before running the first.

- **On Debian 12**, the administrator installs the packages as root with `apt-get update` and then
  `apt-get install git zsh lsof tmux curl python3-venv acl`; the Debian test machine had `git`
  already and installed the rest with that `apt-get install` command. `provision-backend` names the
  venv package as `python3.11-venv`, which Debian 12's `python3-venv` depends on and installs; on
  the test machine, `apt-cache depends python3-venv` listed it. On this path, never run the
  account's copy of Builder as root: the account can change those files, so running them as root
  would hand it root. So that the account's services keep running after it logs out, the
  administrator also runs `loginctl enable-linger <the account>` as root, with the account name
  checked. That command was not run in the Debian test. Ubuntu has not been tested on this path.
  The rest of the administrator's part is for a Mac; on Debian, the account's owner goes on to the
  first paragraph of the next section.
- **On a Mac**, the administrator installs Apple's Command Line Tools, which provide `git` and
  `python3`, and Homebrew's `tmux`. On a test Mac both were already there, and in the account's
  login shell `tmux` resolved through `/opt/homebrew/bin`, which the login shell adds to every
  account's path from `/etc/paths.d/homebrew`, a file Homebrew's installer writes.

  **First, protect the account's password.** The Sharing step below opens the account to password
  logins over the network. Remote Login and
  Screen Sharing accept the account's password from any computer that can reach the Mac, and a
  standard account cannot change sshd's password setting. An administrator could make the account
  key-only, but this path has not been tested that way, so this page relies on that password.
  Whoever has it can log in as the account, run its crews and read the credentials the install
  writes. So first:

  - Make the password a passphrase of four or more words drawn by a generator from a list of 7,776
    words, such as [the EFF's long word list](https://www.eff.org/dice), which gives about 52 bits,
    and use it nowhere else.
  - Before you narrow anything in the next step, from a device on the Tailscale network that will
    be outside the allowed set, run `ping -c 3 <the Mac's Tailscale address>` and see replies. That
    shows the device has a route to the Mac, so a probe below that fails is not failing for want of
    one.
  - Put the Mac where only your devices and the owner's can reach it. On a Tailscale network,
    change the access rules, which by default admit every device on the network, to admit only
    those devices. Tailscale's rules do not cover the Mac's local network, where Remote Login and
    Screen Sharing also answer, so the local network has to be one only those devices join as
    well; a work network shared with other people does not qualify.

  **Before you turn on any sharing service, check three routes in from the internet.** None of these
  checks needs a service running, and a router forward would expose the login the moment it is on.

  - **The router forwards nothing to the Mac.** In the settings of the router, and of any modem in
    front of it, no port forward and no DMZ host points at the Mac, and UPnP, NAT-PMP and PCP are
    off, so no program can open a forward by itself. A port forward and a DMZ host are router
    settings that pass connections from the internet to one machine, and the other three are
    features that let a program create a forward.
  - **The Mac has only private IPv4 addresses.** In Terminal on the Mac,
    `ifconfig | grep -E '^[a-z]|inet '`, which prints each interface's name above its addresses,
    lists only private IPv4 addresses (starting `10.`, `127.`, `169.254.`, `172.16.` to `172.31.`,
    or `192.168.`, plus a `100.64.` to `100.127.` address under a `utun` interface only, since
    internet providers use that range too). An interface is one of the Mac's network connections.
  - **The Mac has no public IPv6 address.** `ifconfig | grep inet6` lists no address that starts
    with `2` or `3`, the prefixes of a public IPv6 address.

  **Then turn on the two sharing services.** In System Settings › General › Sharing, allow the
  account in **Remote Login**, so Deck can reach it over ssh, and in **Screen Sharing**, so its
  owner can log in from their own computer. Under **Allow access for**, choose **Only these users**
  and add the account. In Screen Sharing's options, leave **VNC viewers may control screen with
  password** off, so the only way in is the account's own login.

  **Now check who can reach those two services over Tailscale**, without typing the password
  anywhere. The check uses `nc -z`, which tries to open a connection to one numbered port and
  reports whether it could, sending nothing. Port 22 is Remote Login and port 5900 is Screen
  Sharing. The outside device is the one that answered `ping` earlier. Work through these steps in
  order:

  1. On the outside device, run `tailscale status` and check that it shows itself connected.
  2. From one of your own devices, run `nc -z <the Mac's address> 22` and the same with `5900`.
     Both should report success.
  3. From the outside device, run the same two commands against the Mac's Tailscale address. Both
     should fail.
  4. From your own device, run the two commands again. Both should succeed.
  5. On the outside device, run `tailscale status` again and check that it still shows itself
     connected.

  Only when steps 1, 2, 4 and 5 all pass does the failure in step 3 come from the rules. If any of
  them fails, the Mac or the device was off the network, so wait until all of them pass and start
  again from step 1.

  If either command in step 3 succeeds:

  1. Turn off Remote Login and Screen Sharing, and give the account a new passphrase.
  2. Fix the rules.
  3. Turn the two services back on and start again from step 1 of the five checks above, since a probe with them off
     fails whatever the rules say.
  4. If one still connects, turn them off again.

  The install has not run yet at this point, so there are no credentials to replace.

  **Then check who is on the local network.** Remote Login and Screen Sharing answer any device on
  the Mac's local network, and nothing in this setup filters by address, so check who is on it
  instead: on the Mac, `arp -a` lists only your
  devices, the owner's and the router. It lists only devices that have talked to the Mac recently,
  so also read the router's list of connected devices. If either shows a device you do not
  recognize, turn off Remote Login and Screen Sharing until it is off the network, and check again
  whenever someone new joins.

  **Check what else is listening.** The probe covers the Tailscale network only, and the three
  checks before the services went on covered the common routes in from the internet, not every
  one. One more check states what you should find.

  - **Nothing else is listening that nobody needs.** Since only ports 22 and 5900 were probed, the
    administrator lists what the Mac listens on with `sudo lsof -nP -iTCP -sTCP:LISTEN` and
    `sudo lsof -nP -iUDP`, turns off any sharing service in System Settings › General › Sharing
    that the account does not need, and stops any other listener bound to every interface (shown
    as `*:`) that nobody needs. A listener is a program waiting for connections.

  That describes the Mac at setup; a program a crew starts later can open a listener, or a tunnel
  out to the internet, of its own.

  **Not all of these checks have been run.** The inside probe ran against a test Mac: from a device
  on its Tailscale network, `nc -z` to ports
  22 and 5900 both printed `succeeded`. The `ping` control, the outside probe, the membership check
  and these direct checks have not been run yet. They are written for the Mac. On Debian, `ss -ltnu`
  lists what the machine listens on, and the same rule applies to any listener on every interface
  (shown as `*:` or `0.0.0.0:`); that has not been run on this path, which was tested only in a
  container.
- **If you reach the Mac through the Tailscale app,** replace the app with Tailscale's `tailscaled`
  system daemon, one of the variants in [Tailscale's guide to its macOS
  versions](https://tailscale.com/kb/1065/macos-variants). On a test Mac, the daemon came up at
  boot, before anyone logged in. That guide says the daemon "is only recommended for unattended
  installs managed by experienced macOS system administrators", so weigh it against the problem it
  fixes. When the owner's Screen Sharing login took a test Mac's screen, the Tailscale app in the
  administrator's session dropped the Mac off the Tailscale network. The daemon kept that Mac
  reachable through a restart.

### What the account's owner does on a Mac

How much of this section you need depends on your machine.

- **On Debian,** install Claude Code as your account with the first `curl` line below, open a new
  shell, run `claude` to sign in, and then go on to Install, the next heading; skip the rest of
  this section. That step was run on the Mac only.
- **If you administer this Mac yourself and it logs your account in automatically,** as
  [Preparing a Mac](#preparing-a-mac) sets up, skip the Screen Sharing login and the screen-lock
  and iCloud paragraphs below, which are for a second account on a Mac someone else logs in to,
  and start at the Terminal step; that combination has not been run.
- **On a Mac someone else administers,** follow the whole section.

**Know what others can reach before you set up.** The administrator can read every file in your
account, including the credentials the install writes, and by resetting your password can log in as
you and run your crews. A Mac that logs another account in by itself has FileVault off, so anyone
who takes the Mac can read its disk. The same holds for an account on any machine someone else
administers. Decide whether that suits your work before you install.

**Log in at the desktop through Screen Sharing.** A Mac starts an account's background services
only while that account is logged in at the desktop. On a Mac where another account logs in
automatically, log in through Screen Sharing from your own computer: connect to the Mac, sign in with your account, click **Log In** when asked whether to
share the display or log in. When your desktop appears, lock the screen, so your desktop is never
left open on the Mac's own display: inside the Screen Sharing window, choose **Lock Screen** from
the Apple menu, or press Control-Command-Q, and wait until the window shows the login screen. Then
close the window without logging out. Your session keeps running alongside the other account's after
the window closes, and on a test Mac Builder's services kept running while the session was locked.

**Keep the screen lock on and iCloud off.** Leave your account's screen lock on, as macOS sets it. To check, run `sysadminctl -screenLock
status` in Terminal; while the lock is on it prints `screenLock delay is` and a number of seconds.
If your account is signed in to iCloud, sign it out, for the reason the first step of [Preparing a
Mac](#preparing-a-mac) gives. Skip that section's other two steps: they are for a Mac its owner
administers, and your Screen Sharing login takes the place of its automatic one.

**Install Claude Code and your own Python.** In that desktop session, open Terminal and give your
account what it needs that the administrator's programs cannot provide. The first line below
installs Claude Code. The second installs `uv`, a tool that installs Python. The third puts
`~/.local/bin`, the folder both install into, on your `PATH`. Run these once; the last line adds a
line to `~/.zprofile` each time it runs. The first two run each vendor's published installer as your
account, trusting the vendor's HTTPS site, as their own instructions do:

```
curl -fsSL https://claude.ai/install.sh | bash
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
```

Open a new Terminal window, so `~/.local/bin` is on your `PATH`, and run:

```
uv python install 3.11
claude
```

In that second block, the first line installs Python 3.11 for your account. `claude` signs Claude
Code in. Do it here, at the desktop, so the sign-in is kept where crews started inside the tmux
server that the desktop login starts can read it. Your own Python 3.11 is needed because the Library
refuses to run on an interpreter another account owns, and the administrator's Homebrew Python
belongs to them. Your `python3` can stay an older version: `stand-up-backend` finds `python3.11` on
your `PATH` and builds Builder's environments on it. On a test Mac, `python3` was macOS's 3.9, and
every environment was built on the account's own 3.11.

### Install

Run the install as the account, from its home directory, in a login shell, with the five
repositories cloned in `~/src` as [Before you start](#before-you-start) shows. That section's Debian or Ubuntu machine,
`sudo` and root warning are for the install with administrator rights. Here every command runs as
your account, so the code reaches what your account holds, including the credentials the install
writes.

```
python3 ~/src/shipwright/bin/provision-backend --no-install
sh ~/src/shipwright/bin/install-payload
python3 ~/src/shipwright/bin/stand-up-backend --shape single --seed-registry --activate
```

`provision-backend --no-install` never uses `sudo`. It checks every program and, if one is missing,
stops, names it and says how to install it, and installs nothing. On Debian, `stand-up-backend`
reported `registry seeded, not the tree's` as it placed the backend, which means it started your
projects registry from Builder's seed as it should, and ended with `every step
reported success (5 of 5 ran)`. On the Mac it reported the same seeding line.

Then open a new login shell, so the commands the install linked are on your `PATH`, and check with
`command -v co agentctl`, which prints two paths under `~/.local/bin`. Those two paths are how you
know the install worked.

**On Linux,** if `stand-up-backend` says `lingering could not be enabled`, Builder's services stop
when you log out and start again at your next login. To keep them going, whoever administers the
machine runs `loginctl enable-linger <the account>`, the line in the administrator's Debian step
above, with the account name checked, and never a command copied from the message, which your
account's copy of Builder prints.

**On a Mac,** the services start at the desktop login, so run the install while your Screen Sharing
session is logged in. If you run it with no desktop session, it reports `work left in: supervise`,
because macOS refuses to start an account's services then. They start at your next desktop login.

### After the Mac restarts

A Mac logs in only one account by itself after it restarts, so your account comes back logged out
and your crews stay down until you log in again. Deck's Hosts window shows the account as logged
out then. To check from your own computer, run this line, which asks the Mac whether
your account has a desktop login and prints the answer:

```
ssh <your account>@<the Mac's address> 'launchctl print gui/$(id -u) >/dev/null 2>&1 && echo "logged in" || echo "logged out"'
```

On a test Mac it printed `logged in` while the account was logged in. After a restart, before the
account logged back in, `launchctl print gui/$(id -u)` exited 125 there. By the shell's rules that
exit takes the `||` branch, which prints `logged out`; that output itself was not seen.

To log back in, connect to the Mac with Screen Sharing as before, click **Log In** when asked
whether to share the display or log in, wait until your desktop appears, lock the screen as before,
and then close the window without logging out.

**Never log out to give the screen back:** your account's services run only while it is logged in
at the desktop, and on a test Mac, with the account logged out after a restart, none of them ran.
After that one login, Builder's services and the tmux server the desktop login starts came back by
themselves, and a Claude session started inside that server, which is where Deck starts crews, came
up signed in.

## What the install put where

This table is for reference, and you do not need to learn it. It tells you where to look when you
want to read, edit or back up something Builder made.

| path | what it is |
|---|---|
| `~/builder` | everything Builder owns: one folder per crew |
| `~/builder/steward/CLAUDE.md` | the steward's charter, which is its instructions and yours to edit |
| `~/builder/knowledge` | your knowledge repository, which holds the Reference Room, starting with Builder's starter set: four agents, their instructions, a default profile and the agent policy |
| `~/.claude/CLAUDE.md` | the machine-wide instructions every session reads at start, placed only when you have none, since an existing one is never replaced |
| `~/.claude/skills` | the skills: `new-crew`, `new-subcrew`, `take-upstream` and `write-bead`, and the writing passes `write-better` and `talk-better` |
| `~/.claude/settings.json` | your Claude Code settings, to which the install adds one hook that tells a starting session when the backup is stale, and changes nothing else |
| `~/.local/deploy` | the installed copy of each repository, which is what runs |
| `~/.local/bin` | eleven commands, including `co`, which starts a crew's session, and `builder-backup` |
| `~/.local/state/builder-backup` | your backups: the latest, the one before it, and every blob either has held |
| `~/.config/systemd/user` on Linux, `~/Library/LaunchAgents` on a Mac | the background services |
| `~/.local/state` | the services' logs |
| `~/.local/state/library` | the Library's database, and the two files listing the credentials it accepts |
| `~/.orient-control` | Orient's database, its two Library credentials, `library-token` and `library-client-token`, the work-queue tools' credential, `ops-mcp-token`, and the credential reviewers post their records with, `agent-platform-token` |

The four credential files are secrets, as are `api-tokens.json`, `client-tokens.json` and
`bosun-client-token` in `~/.local/state/library`. Only your account and anyone with administrator
rights on the machine can read them; on a test Mac each was mode 600, a permission setting that
keeps other ordinary accounts out, in a folder other ordinary accounts cannot open. Check yours with
`ls -l ~/.orient-control ~/.local/state/library`: each credential file should read `-rw-------`.
Each of the four tokens in `~/.orient-control` is one the install generated on this machine, and the
Library accepts it because the install also recorded it in `~/.local/state/library`. Nothing copied
a credential from anywhere else.

To check that the Library accepts each one, run the four lines below. Each reads one credential
file and asks the Library, at an address on this machine, whose credential it is:

```
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/library-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/library-client-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/ops-mcp-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/agent-platform-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
```

The token goes to `curl` on its input rather than as an argument, so it never appears in the
process list another account on the machine can read.

They answer with `"actor":"orient","kind":"agent"`, `"actor":"orient","kind":"approved_client"`,
`"actor":"ops-mcp","kind":"agent"` and `"actor":"agent-platform","kind":"agent"`, each followed by
what that credential may do. The last one's list includes `review_record.create`. An answer of `no
resolvable identity` means the Library does not know that token; [a missing credential
file](#the-install-stops-at-mint_credentialpy-saying-already-has-a-credential) below shows how to
replace one.

**Your clones in `~/src` are separate from what runs.** The install copies each repository from its
`main` branch into `~/.local/deploy`, so you can edit or switch branches in `~/src` without changing
what is running. Updating the starter set from a newer release is described [above](#install).
Updating the rest of what runs, the backend and its services, has not been tested yet, so this page
does not describe it.

To see what is installed, and whether it is current:

```
python3 ~/src/shipwright/bin/stand-up-backend --shape single --status
```

## Meet the steward

With the install finished, you can start your first conversation. The first line below moves into
the steward's folder, and the second starts Claude there:

```
cd ~/builder/steward
claude
```

The steward is the first session you meet. Tell it what you want to build, in plain language. It asks what it needs to
know and then creates a crew for the project.

## Your first crew

When the steward creates a crew, three things appear:

- a folder, `~/builder/<crew>`, where the crew's work lives, set up with the starter agents;
- a `tmux` session with the crew's name, where the crew's own Claude session runs as its crew
  orchestrator, started by `co`;
- a file under `~/.config/convivy/deck/crews.d/` that Deck reads. Deck is a Mac app, so on a Linux
  machine the file waits for a Mac to read it.

To watch or talk to the crew, attach to its session, putting the crew's name in place of `<crew>`:

```
tmux attach -t <crew>
```

You will see the crew's conversation with Claude, and you can type into it. To step away, press
`Ctrl-b` then `d`, which leaves the session running.

**A new crew's session waits for you before it starts.** Claude Code asks whether to trust the
crew's folder, once for each crew. On your first crew it also asks whether to accept
bypass-permissions mode, once for the account, because `co` starts every crew in that mode, where a
session runs commands without asking you first. These are yours to answer, and the steward leaves
them to you: attach to the crew's session and answer there.

The steward may tell you the crew's registration is incomplete. That check still looks for settings
Builder no longer uses, and its fix is under way; the crew's session works regardless.

## Backups

You do not have to set backups up. Every six hours, starting when it first runs, the install backs
up the Library's database, which holds the work queue, the Library's cold store,
`~/.local/state/library/cold.db`, where a job moves older signals every six hours, Orient's
database, `~/.orient-control/control.db`, the Library's blobs, which are the files it keeps outside
its database, and your knowledge repository. It does not back up your crews' folders under
`~/builder/<crew>`, your projects registry or Deck's list of crews, so keep a copy of those
yourself, for example by pushing each crew's work to its own remote. Each backup is checked before
it counts. Each copied database has to pass SQLite's integrity check and hold the same number of
rows as the database it came from, before Orient's push subscriptions are removed from its copy, and
the copy of the knowledge repository has to pass `git bundle verify`. Credentials and TLS keys, the
keys that secure the backend's encrypted connections, are left out, because a new install makes its
own. So are Orient's web-push subscriptions, one for each browser you let Orient notify, because
none would work after a restore: a new install makes its own notification key.

The backups stay on this machine, in `~/.local/state/builder-backup`. Your machine's own backups,
such as a VM snapshot, are what carry them off it.

To take one now, before a reboot for instance:

```
builder-backup
```

It prints what it copied and ends with `bundle verified`. To see when the last one succeeded:

```
builder-backup --status
```

That prints `ok` with the time, or `STALE` when no backup has succeeded in the last 24 hours, and
then exits 1. When a run fails, `--status` also prints the reason.

You will hear about a stale backup without asking. Each Claude Code session runs the same check as
it starts or resumes, through a hook the install added to `~/.claude/settings.json`, and says
nothing while the backup is fresh. When it is stale, the session shows the `STALE` line and tells
you about it before anything else.

### Restoring onto a new install

Use these steps when a machine is lost or replaced and you want the Library and your Reference Room
back on a new one. Your crews' folders and your projects registry come back from wherever you kept
them. In outline, you stop Builder's services, put the backed-up databases and knowledge repository
in place, force-push the restored knowledge repository to its remote, and run the install again.

**Run this only on a new install.** It replaces the new machine's database and knowledge repository
with the backup's, and anything written on that machine since its install is gone. The force push
also replaces `main` on the knowledge repository's remote, so if that remote is hosted, for example
on GitHub, anything pushed there since the backup is gone too.
`git -C ~/builder/knowledge remote -v` shows which remote that is. On a fresh install it is
`~/builder/.remotes/knowledge.git`, and if it names anything else, stop and decide whether you mean
to replace that remote's `main` before you run the push.

These steps have been run on Linux only; on a Mac the services are launchd jobs, and `systemctl`
does not exist. Install Builder on the new machine as this page describes, then copy the backup's
`latest` folder to it, here as `~/restore`. Copy the backup's `blobs` folder too: it sits beside
`latest` in `~/.local/state/builder-backup`, not inside it, and holds the files the Library's
records point at. Then:

```
systemctl --user stop com.convivy.library.service com.convivy.orient.service com.convivy.knowledge-watcher.service
systemctl --user stop com.convivy.library.cold-tier.timer com.convivy.knowledge-autopull.timer com.convivy.builder-backup.timer
install -m 600 ~/restore/library.db ~/.local/state/library/library.db
rm -f ~/.local/state/library/library.db-wal ~/.local/state/library/library.db-shm
install -m 600 ~/restore/cold.db ~/.local/state/library/cold.db
rm -f ~/.local/state/library/cold.db-wal ~/.local/state/library/cold.db-shm
install -m 600 ~/restore/orient-control.db ~/.orient-control/control.db
rm -f ~/.orient-control/control.db-wal ~/.orient-control/control.db-shm
git -C ~/builder/knowledge fetch ~/restore/knowledge.bundle main:refs/remotes/backup/main
git -C ~/builder/knowledge reset --hard backup/main
git -C ~/builder/knowledge push --force origin main
python3 ~/src/shipwright/bin/stand-up-backend --shape single --seed-registry --activate
agentctl kb sync
```

The second line stops the three timed jobs that would otherwise open the database, pull into the
knowledge repository or start a backup partway through the restore. `stand-up-backend` starts them
again.

The `install -m 600` form of the `library.db` line, and the lines that restore `cold.db` and
Orient's `control.db`, have not yet been run on the test machine. `install -m 600` copies each
database readable by your account alone, which `cp` does not guarantee for a file it creates.

Copy the contents of the backup's `blobs` folder into `~/.local/state/library/blobs/` before the
`stand-up-backend` line. Without them, the restored Library's records point at files that are not
there. Put your saved projects registry back at
`~/.local/deploy/agent-platform/config/projects.json` before that line too: the install keeps the
registry it finds there, and without one it starts again from Builder's seed, which lists none of
your crews.

The restore brings back the knowledge repository's `main` branch, which is what the Reference Room
serves. `stand-up-backend` brings the restored database up to the installed Library's version and
starts the services again. `agentctl kb sync` ends with `up to date at <commit>`, naming the last commit in the
backup. On the test machine, a document and two work items created before the backup, with a comment
on one, read back the same after the restore through a session's `kb_get` and `issue_get`.

## When something goes wrong

Each installer refuses rather than doing half a job, and says what it refused. A refusal leaves what
was already installed as it was, and you can run the step again once the cause is fixed. Each
heading is the message or symptom you will see, so find yours and read only that part.

### `provision-backend` says `apt-get update failed` and `sudo: a password is required`

The command ran without `sudo` somewhere `sudo` could not ask for a password. On the first install,
before any crew exists, run it with `sudo` in front, as the install section does. After that, never
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

### A skill is missing from a session

Two commands link skills. List what each one linked:

```
sh ~/src/shipwright/bin/install-payload --status
python3 ~/src/shipwright/bin/link-commands --status
```

Between them they should show six: `install-payload` links `new-crew`, `new-subcrew`, `take-upstream`
and `write-bead`, and `link-commands` links `write-better` and `talk-better`. The first command's
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
systemctl --user status com.convivy.library.service
tail ~/.local/state/library.log
```

The install checks each job once, straight after starting it, so a job that runs for a moment before
stopping can be missed there. `systemctl --user list-units 'com.convivy*'` shows every job's state
at any time. On a Mac, `launchctl print gui/$(id -u)/com.convivy.library` shows a job's `state`,
`pid`, `last exit code` and log path. Orient's log can start with `preflight FAILED,
build.load_docs() cannot reach the Library` from its first seconds, while the Library was still
starting. A later `preflight ok` means it recovered.

### The install stops at `mint_credential.py`, saying `already has a credential`

One of the four credential files in `~/.orient-control`, or the Bosun's in `~/.local/state/library`, is gone, and the Library still has the
credential it matched. The install will not replace a
credential, so it stops and changes nothing. If you have the file, put it back. If not, replace the
credential. The commands below restart Orient with `systemctl`, so they are for Linux. For
`library-token`:

```
cd ~/.local/deploy/library
LIBRARY_API_TOKENS=~/.local/state/library/api-tokens.json .venv/bin/python mint_credential.py --file agents --name orient --out ~/.orient-control/library-token --replace
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

The fifth credential, the Bosun's, lives at `~/.local/state/library/bosun-client-token`; replace
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

### `claude mcp list` shows `kb` and `ops` as connected, and their tools fail

`Connected` means only that the two tool servers started. These are the programs that give
Claude Code its `kb` tools, for the Reference Room, and its `ops` tools, for the work queue. If the `ops` tools answer `no ops token`,
`~/.orient-control/ops-mcp-token` is missing; [a missing credential
file](#the-install-stops-at-mint_credentialpy-saying-already-has-a-credential) shows how to replace
it.

## Where to go next

- **[Getting started](getting-started.md)** describes a first week with the steward.
- **[How Builder works](how-builder-works.md)** explains the parts this page installed.
- **[The glossary](glossary.md)** explains each word Builder uses.
