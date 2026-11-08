# Supported setups

This page lists the setups Builder 1.0 supports. A setup is supported when a newcomer holding only
these pages can go from an empty machine to a crew whose session produces working code, and when the
updater and the uninstaller have both been run on it. Builder 1.0 does not ship until that is true of
every setup below. [What works and what does not yet](install-status.md) says how far each one has
been seen working in the current release.

## The machines

Builder runs on two machines: a server that runs the sessions, and a Mac laptop you work from.
[Installing Builder](installing.md#a-server-and-a-laptop-to-work-from) says why.

**The server is one of these three:**

| Operating system | Processor |
|---|---|
| Debian 12 | 64-bit Intel or AMD |
| Ubuntu 22.04 | 64-bit Intel or AMD |
| macOS 26 | Apple silicon |

**The laptop is any Mac running macOS 14 or later.** It runs Deck, the app you work from, and
reaches the server over SSH, a standard way to open a terminal on another machine.

## The four setups on each server

Builder installs on the server in one of three shapes, and the shape is the number of accounts on
the server that Builder uses, your own included. An account is a user on the machine, with its own
home folder and its own files. [One account vs. multiple accounts on the
server](accounts-on-the-server.md) explains what each shape keeps apart.

- **The single-account install** runs Builder as your own account.
- **The two-account install** runs Builder as an `agents` account beside yours, so the agents cannot
  read what your account holds.
- **The three-account install** adds a `reviewers` account, so the agents that review a change run
  apart from the agents that wrote it.

Creating an account takes the machine's administrator password, so which shapes you can install
depends on whether you have it:

| Your access on the server | Shapes supported |
|---|---|
| No administrator password | single-account |
| The administrator password | single-account, two-account, three-account |

That makes four setups on each server, and twelve in all. Each one is worked from Deck on a separate
Mac.

## Anything else

Builder's installers accept other versions of Debian, Ubuntu and macOS, and they may work. They are
not on this list because nobody has rehearsed them, so a problem found there is one nobody has seen
before. Other Linux distributions are not supported: on Linux, the installers install the programs
Builder needs with `apt-get`, the package manager Debian and Ubuntu use.

## Where to go next

- **[What you need](what-you-need.md)** lists what has to exist before you begin.
- **[Installing Builder](installing.md)** walks through the install.
- **[What works and what does not yet](install-status.md)** says which of these setups the current
  release has been seen working on.
