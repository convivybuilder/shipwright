# What works and what does not yet

_Last checked against Builder 0.7.0, on 2026-11-02._

This page lists what has been seen working in Builder, on which test machine, and what does not work
yet. [Installing Builder](installing.md) links here from its end.

**Working on Debian, seen in the Linux container rehearsals** (run 2026-09-25 and 2026-10-02/03
from an account with no `sudo`, and on 2026-11-01 against 0.7.0 from an account with it):
`install-payload` and `stand-up-backend --shape single
--seed-registry --activate` complete.

- A crew's session can read and write its own folder, run programs and commit to git: the steward
  created a crew whose session, started by `co`, built and committed a program that runs.
- The Library, Orient, the knowledge watcher and the run register all run as systemd user services.
- No step asked for GitHub when the install had none configured.
- With no GitHub connected, `agentctl spawn coder --on knowledge` started a run that finished, and
  it read the work item a `co` session had filed, each through its own crew credential.
- Running the install a second time changed nothing.
- With the projects registry emptied, the Library answers 503 and both `co` and `agentctl spawn`
  refuse, each saying why.
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

**The single-account install's GitHub App, seen working on Debian** (a clean Debian 12 container
with 0.7.0, an App created under an organisation with `create-github-app --org`, installed on one
scratch repository, run 2026-11-02): `connect-github --mode instruction` connected the install, and
a dispatched coder's work went from commit to a reviewed pull request under the App.

- The App's installation reached only the repository it was installed on.
- A coder dispatched to that repository committed its own work.
- `agentctl publish` pushed it and `agentctl pr-open` opened a draft pull request. A reviewer and a
  security reviewer each posted a verdict, and the pull request then left draft.
- Each of those steps used a token minted for that step alone, scoped to the one repository and
  revoked once the step finished, and the mint log recorded what GitHub granted each one.
- GitHub refused a push from the App that added a file under `.github/workflows`.

**The one command, seen working on Debian** (a clean Debian 12 container, with the published 0.6.1):
`curl -fsSL https://convivybuilder.org/install.sh | sh` completed a single-account install.

- The first run stopped, named Claude Code as missing, and installed nothing.
- Once Claude Code was installed, the second run exited 0, and `command -v co agentctl` printed both
  commands.
- A third run changed nothing.

**Not working yet, or not yet seen, on any machine:**

- **The one command's release check.** The install now refuses any release without a signed
  manifest. The Debian rehearsal above used 0.6.1, which predates the check, so no rehearsal has
  yet run the one command with the check in place.
- **The one command on a Mac.** It has been seen working on Debian, as described above, but nobody
  has yet run it against a clean Mac. On a Mac, follow [Installing on a Mac](install-mac.md) until
  it has.
- **The one command creating the GitHub App.** The one-command install now pauses near the end to
  create the operator's GitHub App, as [Connecting GitHub](connecting-github.md) describes, but that
  step has not yet been rehearsed; the Debian and Mac rehearsals above both predate it. Run it with
  `--no-github-app` and create the App by hand, as before, until it has.
- **Homebrew has not been rehearsed.** The `convivybuilder/tap/builder` formula, added in 0.6.2, is
  published and pins the release archive by its sha256, but nobody has yet run `brew install
  convivybuilder/tap/builder` against a clean Mac.
- **The one command installing its own prerequisites has not been rehearsed.** Starting with this
  release, it installs `git`, Python 3.11, Claude Code and, on a Mac, `tmux` itself where it has a
  route — `apt-get` on Linux with `sudo`, Homebrew on a Mac, bootstrapping Homebrew itself when an
  administrator is at the keyboard — rather than only naming them missing. This is tested, but
  nobody has yet run it against a clean machine; this page will say so once that rehearsal runs.
- **Orient's pages.** On the tailnet listener, Orient asks the local Tailscale daemon, by `whois`,
  which login owns the connecting peer, and serves that viewer only the projects it may see; a peer
  `whois` cannot name, including a tagged node with no user, gets `403 Forbidden`, the same refusal an
  unidentified loopback request gets. This has not been seen on a rehearsal machine. A fresh install
  writes no `tailnet.json` and no Cloudflare Access settings, so it has no way to log in and Orient
  refuses every page. The command that will set this up is not built yet.
- **The merge check.** A merge is the acceptance of a proposed change into a project. A merge you
  start from Deck or Orient asks the Library first, and the Library approves every one, its log
  saying `merge admission STUBBED (always approves)`, so it does not yet stop a merge that nobody
  reviewed. An agent's merge takes a separate path, through `agentctl kb merge` or `agentctl docs
  merge`, and each of those refuses anything your agent policy does not permit.
- **The three-account install.** `builder-install --shape three` now runs `provision-accounts`,
  `install-privileged`, `install-payload` and `stand-up-backend --shape three` in order, checking
  administrator rights and the platform before any of them runs; its code is merged and
  unit-tested against throwaway roots and stub account and supervisor tools, but nobody has yet run
  it end to end on a real machine. These pages describe only the single-account shape.
- **The two-account install.** Its account and root-install pieces (`provision-accounts`,
  `install-privileged`, `bin/uninstall-builder`) are built and unit-tested, but `stand-up-backend
  --shape two` still refuses outright, so there is no complete two-account install to run yet.
- **Deck's steps for adding a server have not been rehearsed end to end.** [After the
  install](after-installing.md#meet-the-steward) gives them; nobody has yet run them against a real
  server and a real laptop.
- **An updater run end to end on a real machine.** `builder-update --shape single` reports what
  moving to a later release would do, asks you to confirm, then moves every clone, stops jobs,
  snapshots the database, reinstalls the payload and backend, and starts everything again, putting it
  all back on any failure; `--rollback` finishes an update that stopped partway, and `--plan` only
  reports. `--shape two` refuses before it reads anything; `--shape three` fetches the target
  release, verifies it, and prints the full update plan, then refuses, because the root half and
  the `sudo -u agents` steps are not built for either shape. It checks the target release
  against the INSTALLED release's own copy of `builder-install --verify` and its own
  `release-signers`, so moving an install made before this release, whose trust list holds no key,
  still refuses at that check; only an install already on a signed release can move past it. Nobody
  has yet run an update end to end on a real machine.
- **A way to check that a release is genuine, run against a real published release.** Starting with
  this release, `release-signers` carries the key that signs every release manifest, and
  `builder-install --verify <version>` checks a release's signature against it, each of the six
  clones' commit against what the manifest names, and the published archive's sha256, fetching the
  manifest and signature itself when you point it at nothing. The release tags and the `stable`
  branch themselves are still not signed, so a plain clone of `stable` is only as trustworthy as your
  connection to GitHub and the `convivybuilder` organisation's control of its repositories;
  `--verify` is the check that closes that gap, and the one-command install runs the same check
  before any installer. Nobody has yet run either against a real, published release.
- **The uninstaller.** [Removing Builder](after-installing.md#removing-builder) describes
  `bin/uninstall-builder`, whose code now covers the single-, two-, and three-account shapes;
  nobody has yet run any of it end to end on a real machine.
- **The install repository.** `stand-up-backend`'s `place` step creates `install` inside the
  Builder root as its own git repository with no remote, for the install's own non-secret
  configuration. The 2026-11-01 Debian rehearsal ran it; the Mac rehearsal above predates it.
- **The projects registry.** It is one table, held by the Library, never a file on any machine.
  `stand-up-backend`'s `place` step works out the seed document — carrying an adopter's registered
  crews forward from either place an earlier release left them, or taking the release's seed
  otherwise — and stages it where the Library's own first-start step loads it into that table, once.
  Crews register into it over the wire from then on. The 2026-11-01 Debian rehearsal loaded the
  seed; nobody has yet carried registered crews forward on a real machine.
