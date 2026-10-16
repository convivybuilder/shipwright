# Release notes

This page says what changed in each release of Builder, newest first, for anyone deciding whether to
install it or move an existing install to a later release. [After the install](after-installing.md#moving-to-a-later-release)
shows how to move.

## 0.6.3, 2026-10-16

### The Library

- **The cold-tier mover waits out a busy Library rather than failing.** The mover is the job that
  moves old signals out of the Library's main database into its cold one. When the Library was
  writing at the moment the mover tried to start a batch, the mover's pass could end with a
  "database is locked" error. It now retries for a bounded time, so a pass that meets a busy
  Library finishes once the write is done.

### Jobs

- **The `ci-result-fetch` job is gone.** It ran a script the Library no longer has, so a machine
  that turned it on would see it fail on every run. A fresh install never started it. Moving to
  this release does not remove a copy you turned on yourself, so turn that copy off.

## 0.6.2, 2026-10-15

### Installing

- **A Mac can install with Homebrew.** `brew install convivybuilder/tap/builder` installs Builder's
  installer, pinned to this release, along with Python 3.11 and `tmux`. Then run `builder-install`,
  or `builder-install --role laptop` on the laptop you work from. Each release now updates the
  Homebrew formula, so `brew upgrade` brings the installer to the newest release.
  [Installing Builder](installing.md) gives both the Homebrew and the one-line `curl` install.
- **The laptop install asks only for what Deck needs**: `git`, Python 3.11, and `swift` from Apple's
  Command Line Tools. It used to refuse a laptop without Claude Code or `tmux`, which only the server
  runs.

### Spending limits

- **The Bosun now enforces both of a project's spending limits.** The Library decides what each
  project may spend. When a project crosses its soft limit, the Bosun refuses to start an agent for
  any of that project's work items and records why, so `agentctl status` says the limit stopped it rather than
  something else. When a project crosses its hard limit, each agent already running on that project
  ends its run once it notices. A running agent checks no more often than once every 20 seconds,
  and only between steps, so it can take several more steps, or finish a long command such as a build, before it
  stops.

### Work items and the Course

- **A work item filed under the wrong project can move**, with everything under it and all of its
  history. Before this release it had to be closed and filed again.
- **A re-approved epic returns to its old place on the Course** rather than the end, when nothing but
  new epics has moved since it was demoted.
- **A work item can carry a short description**, of up to 25 characters, for places with no room for
  a title, such as Deck's compact view of the Course.

### Orient

- **Each page shows only the projects its viewer may see**, and a viewer who may see none gets a page
  that says so.
- **A table in a Reference Room document can be edited as it appears**, cell by cell, the way a paragraph
  can. The Reference Room holds your project's canonical knowledge; many systems call it the
  knowledge base.
- **Build-plan documents in the Reference Room can be browsed.**

### Agents

- **A run ends with every process its agent started**, so nothing an agent left running in the
  background outlives the run.
- **A crew's repository can live under a GitHub owner other than your main one.** An agent working
  in it gets its GitHub token from your GitHub App's installation on that owner.

### This site

- **[Choosing a tool](choosing-a-tool.md)** is new. It compares the tools for building software with
  AI agents, Builder among them, and is linked from the top of every page.

## 0.6.1, 2026-10-13

These notes begin with 0.6.2. GitHub shows every change 0.6.1 made to the installer and the
documentation in [a comparison of the two releases](https://github.com/convivybuilder/shipwright/compare/v0.6.0...v0.6.1).

## 0.6.0, 2026-10-10

The first public release.
