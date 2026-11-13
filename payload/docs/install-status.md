# What does not work yet

_Last checked against Builder 0.7.1, on 2026-11-08._

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
- **The single-account install is the only complete one.** The three-account install
  (`--shape three`) has not been run end to end on a real machine, and there is no two-account
  install yet. These pages cover only the single-account install.
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

- **`builder-update` has not been run end to end on a real machine.** It moves only a
  single-account install, and only one already on 0.7.0 or later; an install from before 0.7.0
  moves once by the manual route in [After the
  install](after-installing.md#moving-to-a-later-release). Nobody has yet carried an earlier
  install's registered crews forward this way.
- **The uninstaller has not been run end to end on a real machine.** [Removing
  Builder](after-installing.md#removing-builder) describes it.

## Checking a release

**Only the release manifest is signed; the release tags and the `stable` branch are not.** The one
command checks every clone against the signed manifest before installing. If you cloned the
repositories yourself, check them with this, putting your release's version in place of `vX.Y.Z`:

```
curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --verify vX.Y.Z
```
