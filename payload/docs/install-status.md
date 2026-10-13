# What works and what does not yet

This page lists what has been seen working in Builder 0.6.0, on which test machine, and what does not
work yet. [Installing Builder](installing.md) links here from its end.

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
  Mac restarts](install-mac.md#after-the-mac-restarts).
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
now works when run with the App's own token. Not yet seen: Deck on a second Mac, reaching the first
over SSH, with a session started there.

**Not working yet, on any machine:**

- **The one command has not been rehearsed yet.** `bin/builder-install`, served at
  `https://convivybuilder.org/install.sh`, has its own planted-failure test suite, but nobody has
  yet run `curl -fsSL https://convivybuilder.org/install.sh | sh` against a real, empty machine the
  way the manual steps above have been. Follow the pages under [Which install is
  yours](installing.md#which-install-is-yours) until it has.
- **Orient's pages.** Orient answers every page with `403 Forbidden`, a web server's way of
  refusing, until the way it identifies a person is built.
- **The merge check.** A merge is the acceptance of a proposed change into a project. A merge you
  start from Deck or Orient asks the Library first, and the Library approves every one, its log
  saying `merge admission STUBBED (always approves)`, so it does not yet stop a merge that nobody
  reviewed. An agent's merge takes a separate path, through `agentctl kb merge` or `agentctl docs
  merge`, and each of those refuses anything your agent policy does not permit.
- **An updater.** To move to a later release, pull `stable` in each clone, as [Moving to a later
  release](after-installing.md#moving-to-a-later-release) describes; no command does that for you.
- **A way to check that a release is genuine.** The `v0.6.0` tag and the `stable` branch are not
  signed, so a clone is only as trustworthy as your connection to GitHub and the `convivybuilder`
  organisation's control of its repositories.
- **The two-account install.** 0.6.0 installs only the single-account shape these pages describe.
- **Deck's steps for adding a server have not been rehearsed end to end.** [After the
  install](after-installing.md#meet-the-steward) gives them; nobody has yet run them against a real
  server and a real laptop.
- **Updating the backend and its services.** Moving the starter set to a later release has been
  tested; updating the rest of what runs has not.
