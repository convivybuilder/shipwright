# What does not work yet

_Last checked against Builder 0.8.0, on 2026-11-26._

Every step on the install pages has been run on a Debian 12 or macOS 26 test machine, except what
this page lists. Where there is something to do in the meantime, each entry says what.

## Installing

- **The one command's GitHub App step has not been run on a test machine.** Near its end, the
  install pauses to create your GitHub App. Until that step has been tested, add `--no-github-app`
  to the install and create the App by hand, as [Connecting GitHub](connecting-github.md) shows.
- **On a Mac, the one command has not yet installed a published release from the site.** It has on
  Debian.
- **The manual steps on [Installing on a Mac](install-mac.md) have not been run on a clean Mac.**
  The one command has.
- **No install has yet passed a rehearsal on Ubuntu 24.04**, the platform that replaces Ubuntu
  22.04 as supported in this release. The one 24.04 rehearsal ran before that change, and its
  install stopped.
- **The two-account install (`--shape two`) has not been run end to end on a real machine.** It has
  been run against throwaway roots and stub account tools. The single-account and three-account
  installs have been rehearsed end to end on Debian 12 and macOS 26 test machines. This release's
  three-account rehearsals ran with `--no-github-app`.
- **The two-account install's merge rule is not built.** It needs two GitHub rulesets on `main`,
  one that refuses every update except a pull request the operator merges, and the command that
  would print and check them, `github-gate --shape two`, does not exist yet. Merge each pull request
  yourself, from another device, through GitHub's own web page, until it ships.
- **On a Mac, nobody has yet seen the steward create a crew whose session writes code.** On Debian
  it has.
- **Orient fails its first start on a fresh install.** Its supervisor restarts it moments later, and
  it runs from then on. The error that first start leaves in Orient's log needs nothing from you.

## Working from a laptop

- **Deck's steps for adding a server have not been run against a real server and laptop.** [After
  the install](after-installing.md#meet-the-steward) gives them.
- **Deck does not notify you when the account that runs your crews is logged out.** Its Hosts window
  shows it.
- **Deck on a second Mac, reaching the first over SSH, has not been seen working.**

## Using Builder

- **Orient's pages refuse every visitor on a fresh install.** The install sets up no way to sign in
  to Orient, and the command that will is not built yet.
- **The Library approves every merge you start from Deck or Orient.** It does not yet stop a merge
  nobody reviewed. An agent's merge takes a separate path, which refuses anything your [agent
  policy](customizing.md#the-agent-policy) does not permit.

## Updating and removing

- **The updater has been rehearsed against rehearsal releases, not yet against published ones.**
  The single-account update was rehearsed on Debian on 2026-11-17. The three-account update
  (`--shape three`) was rehearsed on Debian 12 and macOS 26 on 2026-11-19, and so was a
  three-account rollback on macOS 26, which put the earlier release back with every job running.
  The two-account update (`--shape two`) has not been rehearsed on a real machine yet. An install from before
  0.7.0 moves once by the manual route in [After the
  install](after-installing.md#moving-to-a-later-release), to reach a signed release first.
  Nobody has yet carried an earlier install's registered crews forward through an update.
- **Rerunning `stand-up-backend --shape two|three` on an install from before the Library had its
  own service account moves the Library's data to that account and takes its old units, which
  still named `agents`, out of the supervisor, so the step right after writes the account's own
  fresh ones rather than refusing a unit it does not recognise. Seen on a Debian 12 rehearsal,
  not yet on a real adopter's machine.**
- **The uninstaller has not been run end to end on a real machine.** [Removing
  Builder](after-installing.md#removing-builder) describes it.

## Checking a release

**Only the release manifest is signed; the release tags and the `stable` branch are not.** The one
command checks every clone against the signed manifest before installing. If you cloned the
repositories yourself, check them with this, putting your release's version in place of `vX.Y.Z`:

```
curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --verify vX.Y.Z
```
