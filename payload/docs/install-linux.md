# Installing on Linux, with administrator access

This page is for a Debian or Ubuntu account that can install software for the whole machine,
which on Linux means it can use `sudo`; [Installing Builder](installing.md#words-these-pages-use)
explains `sudo` and how to check. On a Mac, follow [Installing on a Mac](install-mac.md). For a Linux
account that cannot, follow [Installing on Linux, without administrator access](install-linux-without-sudo.md).

It has been tested on Debian 12. On Ubuntu 22.04 it has been tested only as far as the package step.

Before you begin, do everything in [Before you start](installing.md#before-you-start): Claude Code
signed in, and the six repositories cloned into `~/src`.

## Run the install

Run these three commands in order, from your home directory, which is where a new terminal window
starts. Type each line, press Return, and wait for it to finish before typing the next. The list
under the commands says what each one does. The first asks for your password, because it uses
`sudo`.

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
   which is the only shape built so far. `--seed-registry` starts your projects registry, the list
   of your projects, from Builder's seed, because the source repositories carry the registry of the
   crews that build Builder, which is not yours. It writes `operator.json`, the file that names
   you as the operator, into the settings folder `~/.config/convivy`, unless you already have one.
   It places Builder's backend, links its commands and the two writing skills, registers the tools
   a session uses to reach the Library, and installs and starts the background services. Before the Library first starts, it creates the Library's
   database and two credentials Orient uses to reach the Library. It prints what each step did and
   ends with `every step reported success (6 of 6 ran)`.

**Run the first command as root only this once, before any crew exists.** A crew's session runs as
your account and can edit the files in `~/src`, so a later `sudo` run of that code would run
whatever a session changed as root. After the first install, install a package a newer release needs
with `sudo apt-get install` yourself, and run `provision-backend` without `sudo` and with
`--no-install`, which checks each package and names what is missing without installing anything.

The other two commands are safe to run again. A second run changes only what is missing or out of
date, and it never replaces a credential: it prints `skipped … since … exists` for each one already
there.

## What the installers print that these pages do not ask you to do

The installers print more steps than these pages give. You can leave every one of them alone. None
of them is needed to meet the steward and build a first crew:

- **A credentials file for the LLM gateway**, `~/.config/convivy/llm-gateway.env`. The gateway is
  a local service that lets agents use models from providers other than Anthropic. It is off by
  default, and nothing on these pages uses it.
- **Checks such as `bin/register-mcp --check` and `bin/provision-backend --check`**, and a pointer to
  `bin/install-jobs --help`. `stand-up-backend` has already run the steps these check, and printed
  what each one did.
- **`claude mcp get ops`**, which asks whether the work-queue tools can reach what they need.
- **A note that Ubuntu 22.04's `python3` is version 3.10.** It does not apply on Debian 12, where
  `python3` is 3.11.

## Next

Go on to [After the install](after-installing.md), which shows what the install put where and takes
you to the steward and your first crew. If a step refused, find its message under [When something
goes wrong](installing.md#when-something-goes-wrong).
