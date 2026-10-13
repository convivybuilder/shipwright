# Installing on a Mac

On a Mac, Builder installs into one ordinary account and needs no administrator rights to run.
Everything runs as that account. These steps were run on macOS 26.4 by a standard account on a Mac
whose administrator is someone else, except where a step says it was not run. The install has not
been run on a clean Mac.

Two people take part, the Mac's administrator and the owner of the account Builder will run in. If
you are both, do both parts. The page has five parts, in this order:

1. [Preparing a Mac](#preparing-a-mac), only if you administer the Mac yourself and Builder will run
   in your own account.
2. [What the Mac's administrator does once](#what-the-macs-administrator-does-once): installs a few
   programs and decides who can reach the account over the network.
3. [What the account's owner does](#what-the-accounts-owner-does): logs in at the desktop and
   installs Claude Code and Python.
4. [Run the install](#run-the-install): the owner runs the three install commands.
5. [After the Mac restarts](#after-the-mac-restarts): the owner logs in again after each restart.

Tailscale is a private network across your own devices, Remote Login is the Mac setting that allows
logins over SSH, and Screen Sharing is the Mac feature that shows a Mac's desktop on another
computer.

## Preparing a Mac

This section is for a Mac you administer yourself. It changes three settings so that agents can
keep working with nobody at the keyboard. Each setting gives up some of the Mac's protection, so
read the warning before the steps. Do these three things as soon as the Mac is set up, before you
clone the repositories. If someone else administers the Mac, skip this section; the owner's part
says which of these steps still apply.

**Do this only on a Mac that stays somewhere you control.** With the screen lock off, anyone at its
keyboard reaches your account: a crew's session that runs commands without asking, and the tokens
the install creates. A Mac signed out of iCloud also cannot be located or erased with Find My, and
one that logs in by itself has FileVault off, so its disk is readable by whoever takes it. FileVault
is the macOS feature that encrypts the disk. A desktop machine in your own space suits these
settings; a laptop that travels does not.

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
   starts crews over SSH. The install adds a job that starts a tmux server from the desktop login,
   and crews started inside it can read the Keychain. That job runs only while someone is logged in
   at the desktop, so after a restart, crews come up logged out until someone logs in, in person or
   through Screen Sharing. To have the Mac log in by itself:
    1. Open **System Settings**, click **Users & Groups**, and set **Automatically log in as** to
       your account.

    macOS offers automatic login only while FileVault is off, so this step also leaves the disk
    unencrypted. If you keep FileVault on, log in after each restart instead.

## What the Mac's administrator does once

**Install two programs.** The administrator installs Apple's Command Line Tools, which provide `git`
and `python3`, and Homebrew's `tmux`. On a test Mac both were already there, and in the account's
login shell `tmux` resolved through `/opt/homebrew/bin`, which the login shell adds to every
account's path from `/etc/paths.d/homebrew`, a file Homebrew's installer writes.

**Never run the account's copy of Builder as an administrator.** The account can change those files,
so running them with administrator rights would hand it those rights. When `provision-backend
--no-install` later names something missing, install only what this section names, and never run a
command it prints, since the account can change the program that prints it.

**Protect the account's password.** The sharing step below opens the account to password logins
over the network. Remote Login and Screen Sharing accept the account's password from any computer
that can reach the Mac, and a standard account cannot change sshd's password setting. An
administrator could make the account key-only, but this path has not been tested that way, so this
page relies on that password. Whoever has it can log in as the account, run its crews and read the
credentials the install writes. So first:

- Make the password a passphrase of four or more words drawn by a generator from a list of 7,776
  words, such as [the EFF's long word list](https://www.eff.org/dice), which gives about 52 bits,
  and use it nowhere else.
- Before you narrow anything in the next step, from a device on the Tailscale network that will be
  outside the allowed set, run `ping -c 3 <the Mac's Tailscale address>` and see replies. That shows
  the device has a route to the Mac, so a probe below that fails is not failing for want of one.
- Put the Mac where only your devices and the owner's can reach it. On a Tailscale network, change
  the access rules, which by default admit every device on the network, to admit only those
  devices. Tailscale's rules do not cover the Mac's local network, where Remote Login and Screen
  Sharing also answer, so the local network has to be one only those devices join as well; a work
  network shared with other people does not qualify.

**Before you turn on any sharing service, check three routes in from the internet.** None of these
checks needs a service running, and a router forward would expose the login the moment it is on.

- **The router forwards nothing to the Mac.** In the settings of the router, and of any modem in
  front of it, no port forward and no DMZ host points at the Mac, and UPnP, NAT-PMP and PCP are off,
  so no program can open a forward by itself. A port forward and a DMZ host are router settings that
  pass connections from the internet to one machine, and the other three are features that let a
  program create a forward.
- **The Mac has only private IPv4 addresses.** In Terminal on the Mac,
  `ifconfig | grep -E '^[a-z]|inet '`, which prints each interface's name above its addresses, lists
  only private IPv4 addresses (starting `10.`, `127.`, `169.254.`, `172.16.` to `172.31.`, or
  `192.168.`, plus a `100.64.` to `100.127.` address under a `utun` interface only, since internet
  providers use that range too). An interface is one of the Mac's network connections.
- **The Mac has no public IPv6 address.** `ifconfig | grep inet6` lists no address that starts with
  `2` or `3`, the prefixes of a public IPv6 address.

**Then turn on the two sharing services.** In System Settings › General › Sharing, allow the account
in **Remote Login**, so Deck can reach it over ssh, and in **Screen Sharing**, so its owner can log
in from their own computer. Under **Allow access for**, choose **Only these users** and add the
account. In Screen Sharing's options, leave **VNC viewers may control screen with password** off, so
the only way in is the account's own login.

**Now check who can reach those two services over Tailscale**, without typing the password anywhere.
The check uses `nc -z`, which tries to open a connection to one numbered port and reports whether it
could, sending nothing. Port 22 is Remote Login and port 5900 is Screen Sharing. The outside device
is the one that answered `ping` earlier. Work through these steps in order:

1. On the outside device, run `tailscale status` and check that it shows itself connected.
2. From one of your own devices, run `nc -z <the Mac's address> 22` and the same with `5900`. Both
   should report success.
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
3. Turn the two services back on and start again from step 1 of the five checks above, since a
   probe with them off fails whatever the rules say.
4. If one still connects, turn them off again.

The install has not run yet at this point, so there are no credentials to replace.

**Then check who is on the local network.** Remote Login and Screen Sharing answer any device on the
Mac's local network, and nothing in this setup filters by address, so check who is on it instead:
on the Mac, `arp -a` lists only your devices, the owner's and the router. It lists only devices that
have talked to the Mac recently, so also read the router's list of connected devices. If either
shows a device you do not recognize, turn off Remote Login and Screen Sharing until it is off the
network, and check again whenever someone new joins.

**Check what else is listening.** The probe covers the Tailscale network only, and the three checks
before the services went on covered the common routes in from the internet, not every one. List
what the Mac listens on with `sudo lsof -nP -iTCP -sTCP:LISTEN` and `sudo lsof -nP -iUDP`, turn off
any sharing service in System Settings › General › Sharing that the account does not need, and stop
any other listener bound to every interface (shown as `*:`) that nobody needs. A listener is a
program waiting for connections. That describes the Mac at setup; a program a crew starts later can
open a listener, or a tunnel out to the internet, of its own.

**Not all of these checks have been run.** The inside probe ran against a test Mac: from a device on
its Tailscale network, `nc -z` to ports 22 and 5900 both printed `succeeded`. The `ping` control, the
outside probe, the membership check and the listener check have not been run yet.

**If you reach the Mac through the Tailscale app,** replace the app with Tailscale's `tailscaled`
system daemon, one of the variants in [Tailscale's guide to its macOS
versions](https://tailscale.com/kb/1065/macos-variants). On a test Mac, the daemon came up at boot,
before anyone logged in. That guide says the daemon "is only recommended for unattended installs
managed by experienced macOS system administrators", so weigh it against the problem it fixes. When
the owner's Screen Sharing login took a test Mac's screen, the Tailscale app in the administrator's
session dropped the Mac off the Tailscale network. The daemon kept that Mac reachable through a
restart.

## What the account's owner does

How much of this section you need depends on your Mac.

- **If you administer this Mac yourself and it logs your account in automatically,** as [Preparing
  a Mac](#preparing-a-mac) sets up, skip the Screen Sharing login and the screen-lock and iCloud
  paragraphs below, which are for a second account on a Mac someone else logs in to, and start at
  the Terminal step. That combination has not been run.
- **On a Mac someone else administers,** follow the whole section.

**Know what others can reach before you set up.** The administrator can read every file in your
account, including the credentials the install writes, and by resetting your password can log in as
you and run your crews. A Mac that logs another account in by itself has FileVault off, so anyone
who takes the Mac can read its disk. Decide whether that suits your work before you install.

**Log in at the desktop through Screen Sharing.** A Mac starts an account's background services only
while that account is logged in at the desktop. On a Mac where another account logs in
automatically, log in through Screen Sharing from your own computer: connect to the Mac, sign in
with your account, and click **Log In** when asked whether to share the display or log in. When your
desktop appears, lock the screen, so your desktop is never left open on the Mac's own display:
inside the Screen Sharing window, choose **Lock Screen** from the Apple menu, or press
Control-Command-Q, and wait until the window shows the login screen. Then close the window without
logging out. Your session keeps running alongside the other account's after the window closes, and
on a test Mac Builder's services kept running while the session was locked.

**Keep the screen lock on and iCloud off.** Leave your account's screen lock on, as macOS sets it. To
check, run `sysadminctl -screenLock status` in Terminal; while the lock is on it prints `screenLock
delay is` and a number of seconds. If your account is signed in to iCloud, sign it out, for the
reason the first step of [Preparing a Mac](#preparing-a-mac) gives. Skip that section's other two
steps: they are for a Mac its owner administers, and your Screen Sharing login takes the place of
its automatic one.

**Install Claude Code and your own Python.** In that desktop session, open Terminal and give your
account what it needs that the administrator's programs cannot provide. The first line below
installs Claude Code. The second installs `uv`, a tool that installs Python. The third puts
`~/.local/bin`, the folder both install into, on your `PATH`. Run these once; the last line adds a
line to `~/.zprofile` each time it runs. The first two run each vendor's published installer as
your account, trusting the vendor's HTTPS site, as their own instructions do:

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

Then do everything in [Before you start](installing.md#before-you-start) that you have not done yet:
the six repositories cloned into `~/src`.

## Run the install

Run the install as your account, from your home directory, in a login shell, while your Screen
Sharing session is logged in. Every command runs as your account, so the code reaches what your
account holds, including the credentials the install writes.

```
python3 ~/src/shipwright/bin/provision-backend --no-install
sh ~/src/shipwright/bin/install-payload
python3 ~/src/shipwright/bin/stand-up-backend --shape single --seed-registry --activate
```

`provision-backend --no-install` never uses `sudo`. It checks every program and, if one is missing,
stops, names it and says how to install it, and installs nothing. On the test Mac, `stand-up-backend`
reported `registry seeded, not the tree's` as it placed the backend, which means it started your
projects registry from Builder's seed as it should. [Installing on Debian or Ubuntu with
sudo](install-linux.md#run-the-install) says what each of the three commands does.

Then open a new login shell, so the commands the install linked are on your `PATH`, and check with
`command -v co agentctl`, which prints two paths under `~/.local/bin`. Those two paths are how you
know the install worked.

The services start at the desktop login. If you run the install with no desktop session, it reports
`work left in: supervise`, because macOS refuses to start an account's services then. They start at
your next desktop login.

## After the Mac restarts

A Mac logs in only one account by itself after it restarts, so your account comes back logged out
and your crews stay down until you log in again. Deck's Hosts window shows the account as logged out
then. To check from your own computer, run this line, which asks the Mac whether your account has a
desktop login and prints the answer:

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

## Next

Go on to [After the install](after-installing.md), which shows what the install put where and takes
you to the steward and your first crew. If a step refused, find its message under [When something
goes wrong](installing.md#when-something-goes-wrong).
