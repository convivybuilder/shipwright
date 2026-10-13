# Installing on Linux, without administrator access

This page installs Builder into one ordinary Linux account that cannot install software for the
whole machine (on Linux, an account that cannot use `sudo`), such as an account on a work machine. Everything runs as that account. On a Mac, follow [Installing on a
Mac](install-mac.md). If your account can use `sudo`, [Installing on Linux, with administrator access](install-linux.md) is
shorter.

These steps were run on Debian 12, in a container, by an account that could not use `sudo`
(`sudo -l -U <the account>` answered `is not allowed to run sudo`), except where a step says it was
not run. A container is an isolated Linux system running inside another machine. Ubuntu has not
been tested on this path.

Two people take part, the machine's administrator and the owner of the account Builder will run in.
If you are both, do both parts.

## What the machine's administrator does once

The account cannot install system packages, so someone who administers the machine installs them
first:

```
apt-get update
apt-get install git zsh lsof tmux curl python3-venv acl
```

Run both as root. The Debian test machine had `git` already and installed the rest with that
`apt-get install` command. `provision-backend`, which the account runs later, names the venv package
as `python3.11-venv`; Debian 12's `python3-venv` depends on it and installs it, and on the test
machine `apt-cache depends python3-venv` listed it.

So that the account's services keep running after it logs out, the administrator also runs this as
root, with the account name checked first:

```
loginctl enable-linger <the account>
```

That command was not run in the Debian test.

**Never run the account's copy of Builder as root.** The account can change those files, so running
them as root would hand it root. When `provision-backend --no-install` later names something
missing, treat its output as something to read: install only what the list above names, and never
run a command it prints, since the account can change the program that prints it.

**Check what is listening.** `ss -ltnu` lists what the machine listens on. Stop any listener bound
to every interface (shown as `*:` or `0.0.0.0:`) that nobody needs. A listener is a program waiting
for connections. This check has not been run on this path.

## What the account's owner does

Install Claude Code as your account, open a new shell, and sign in:

```
curl -fsSL https://claude.ai/install.sh | bash
claude
```

The first line runs Anthropic's published installer as your account, trusting its HTTPS site, as its
own instructions do. This step was run on a Mac only.

Then do everything in [Before you start](installing.md#before-you-start) that you have not done yet:
the six repositories cloned into `~/src`.

## Run the install

Run the install as your account, from your home directory, in a login shell. Every command runs as
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
projects registry from Builder's seed as it should, and ended with `every step reported success (5
of 5 ran)`. [Installing on Linux, with administrator access](install-linux.md#run-the-install) says what
each of the three commands does.

Then open a new login shell, so the commands the install linked are on your `PATH`, and check with
`command -v co agentctl`, which prints two paths under `~/.local/bin`. Those two paths are how you
know the install worked.

If `stand-up-backend` says `lingering could not be enabled`, Builder's services stop when you log
out and start again at your next login. To keep them going, whoever administers the machine runs
`loginctl enable-linger <the account>`, as in the administrator's part above, with the account name
checked, and never a command copied from the message, which your account's copy of Builder prints.

## Next

Go on to [After the install](after-installing.md), which shows what the install put where and takes
you to the steward and your first crew. If a step refused, find its message under [When something
goes wrong](installing.md#when-something-goes-wrong).
