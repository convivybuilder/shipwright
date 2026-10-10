# Getting started

This page takes you from installing Builder to your first crew. Like a bead, which is a project's
short description of where it is going, the page describes Builder as it is designed to work.
[Installing Builder today](installing.md) covers the install itself, as Builder's first public
release runs it.

There are four stages, and this page takes them in order. You gather what Builder needs, you
install it, you meet the steward, and the steward sets up your first crew. A crew is one project
together with the AI agents working on it, and the steward is the guide you talk to first. You do
not need to have written a program before.

## What you need

- **A Mac**, and a terminal you are comfortable opening. A terminal is a window where you type
  commands, and on a Mac the application is called Terminal.
- **The Mac's administrator password, for the two-account install**, which uses it to create the
  two accounts Builder runs as. This release installs only the single-account shape; the
  two-account install comes in a later release. Without one, choose the single-account install.
  Both are explained under Install, below.
- **Claude Code, signed in to your Claude account.** Claude Code is the program that lets you talk
  with Claude, an AI model, in a terminal. Every Builder session is a conversation with Claude in a
  terminal.
- **A GitHub account, for the two-account install**, which keeps its merge gate on GitHub. GitHub
  is a website that stores a project's files and history, and the merge gate is the rule that a
  change must pass review before it is accepted. The single-account install can start without a
  GitHub account.

On the two-account install, Homebrew installs anything else Builder needs; Homebrew is a free
program for the Mac that installs other programs. The single-account install names anything missing
for you to install. [What you need](what-you-need.md) covers the rest: the machine that keeps
working while your laptop is shut, the accounts Builder acts through, and where the apps you build
can live.

## Install

Builder installs from a terminal with a single Homebrew command, which this page will give once
Builder is public, and you name the install's shape as you run it. The shape decides which user
account on your Mac Builder runs as, and there are two.

- **The two-account install** creates two accounts, `agents`, which runs Builder, and `reviewers`,
  which runs the agents that review a change, and asks you to turn on Remote Login for `agents` if
  it is off. Remote Login is the Mac setting that allows a login over SSH, which the next section
  uses. The install puts everything Builder owns under one folder in the `agents` account,
  `~/builder` unless you choose another. In a path, `~` stands for an account's home folder.
- **The single-account install** creates no account and puts `~/builder` in your own account.

Today the single-account install is the only shape built, and [Installing Builder](installing.md)
gives its steps. Once the two-account install is built, choose it when you have the administrator
password, because it keeps the agents away from your own files and credentials. The first install
names the folder where you meet the steward. [Where everything
runs](where-everything-runs.md#two-install-shapes) says how the two shapes differ, and why the
two-account install does not run Builder as you.

## Meet the steward

The steward is the first session you meet, and it owns no project of its own. It asks what you want
to build, then gets the smallest real version of that running with you.

To meet it, you open a terminal, go to the steward's folder and start Claude there. On the
two-account install, Builder's sessions run as `agents`, so you first reach that account over SSH,
a standard way to open a terminal as another account or on another machine. On the single-account
install, leave out the `ssh` line:

```
ssh agents@localhost
cd ~/builder/steward
claude
```

The first line opens a terminal as `agents` on this same Mac, which is what `localhost` means. The
second moves into the steward's folder. The third starts Claude, and the conversation that opens is
the steward. Tell it, in plain language, what you want to build.

From another machine, use the Mac's address in place of `localhost`. Deck, Builder's desktop
application, does the same for you once you have added the Mac to it.

## Your first crew

The steward builds your first project by creating a crew for it: a folder under `~/builder`, a
session that works there, and an entry for Deck. From then on that crew's session does the
building, and the steward carries decisions between crews as you add more.

The crew's first job is its bead, a short description of where the project is going. It writes one
with the `write-bead` skill, which is a set of instructions a session loads for that job, and every
piece of work after that is measured against it.

## Advice for the first week

**Bring a problem.** You do not need a specification, the written description of how your project
will stand once a large piece of work, called an epic, is done. The steward's fastest route to one
is a working thing you can react to.

**Correct it with the reason attached.** "No, do it this way" gets you compliance. "No, because
that path drops the error and we lost a day to it" gets you a rule the steward can apply to cases
you never mentioned.

**Some decisions stay yours.** Merging, spending money, publishing anything, changing what a project
is for and deleting things are your call, however much you come to trust the steward, and the one
exception is a kind of merge you choose to hand over. Merging means accepting a proposed change,
called a pull request, into the project. The steward brings these decisions to you with a
recommendation. You can decide some merges in advance: the agent policy,
`projects/platform/policy/agent-policy.yaml` in your knowledge repository, names the kinds of pull
request an agent may merge once review passes. Out of the box it names none. `agentctl kb merge`,
the command the Library merges through, reads the policy and refuses anything it does not permit. A
merge you start from Deck or Orient takes a separate path, through a merge check in the Library, and
that check approves every merge it is asked about for now, as [Installing Builder](installing.md)
says. Your knowledge repository holds the Reference Room, Builder's store of what your projects hold
to be true, which many systems call a knowledge base.

**Its instructions are yours to edit.** The steward's charter is `~/builder/steward/CLAUDE.md`, in
the `agents` account or, on the single-account install, in yours. A charter is the file of
instructions the steward follows. It records what the two of you learn about working together, and
it is worth reading every few weeks.

**Work on one thing at a time in each crew.** Builder shows you everything you have in flight, and
a long list is how you notice you have stopped finishing things.

## Where to go next

- **[How Builder works](how-builder-works.md)** shows how the parts fit together.
- **[Where everything runs](where-everything-runs.md)** shows which parts can live on which machine.
- **[The glossary](glossary.md)** explains each word Builder uses.
