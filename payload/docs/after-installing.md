# After the install

This page picks up where each install page ends. It shows what the install put where, how to move to
a later release, and takes you to the steward and your first crew. It also covers backups.

## What the install put where

This table is for reference, and you do not need to learn it. It tells you where to look when you
want to read, edit or back up something Builder made.

| path | what it is |
|---|---|
| `~/builder` | everything Builder owns: one folder per crew |
| `~/builder/steward/CLAUDE.md` | the steward's charter, which is its instructions and yours to edit |
| `~/builder/knowledge` | your knowledge repository, which holds the Reference Room, starting with Builder's starter set: four agents, their instructions, a default profile and the agent policy |
| `~/.claude/CLAUDE.md` | the machine-wide instructions every session reads at start, placed only when you have none, since an existing one is never replaced |
| `~/.claude/skills` | the skills: `new-crew`, `new-subcrew`, `take-upstream`, `write-bead`, `rollover`, `handoff-pickup` and `handoff-leave`, and the writing passes `write-better` and `talk-better` |
| `~/.claude/settings.json` | your Claude Code settings, to which the install adds one hook that tells a starting session when the backup is stale, and changes nothing else |
| `~/.local/deploy` | the installed copy of each repository, which is what runs |
| `~/.local/bin` | thirteen commands, including `co`, which starts a crew's session, `builder-backup`, `builder-update` and `mint-crew-ops-credentials` |
| `~/.local/state/builder-backup` | your backups: the latest, the one before it, and every blob either has held |
| `~/.config/systemd/user` on Linux, `~/Library/LaunchAgents` on a Mac | the background services |
| `~/.local/state` | the services' logs |
| `~/.local/state/library` | the Library's database, and the two files listing the credentials it accepts |
| `~/.orient-control` | Orient's database, its two Library credentials, `library-token` and `library-client-token`, the credential reviewers post their records with, `agent-platform-token`, the credential agent-platform code reads the crew registry with, `agent-platform-registry-reader-token`, the credential `agentctl crew register` adds a crew with, `agent-platform-registry-writer-token`, the credential Deck approves, declines and sets a model with, `deck-library-token`, `ops-mcp-token`, which only `agentctl crew doctor` still falls back to, and two more files per registered crew, `ops-<crew>-token` and `ops-co-<crew>-token`, which a dispatched run and that crew's own session present to the work queue |

The seven fixed credential files are secrets, as are each crew's `ops-<crew>-token` and
`ops-co-<crew>-token`, and `api-tokens.json`, `client-tokens.json` and `bosun-client-token` in
`~/.local/state/library`. Only your account and anyone with administrator rights on the machine can
read them; on a test Mac each was mode 600, a permission setting that keeps other ordinary accounts
out, in a folder other ordinary accounts cannot open. Check yours with
`ls -l ~/.orient-control ~/.local/state/library`: each credential file should read `-rw-------`.
Each token in `~/.orient-control` is one the install, or `mint-crew-ops-credentials`, generated on
this machine, and the Library accepts it because the same run also recorded it in
`~/.local/state/library`. Nothing copied a credential from anywhere else.

To check that the Library accepts each one, run the seven lines below. Each reads one credential
file and asks the Library, at an address on this machine, whose credential it is:

```
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/library-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/library-client-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/ops-mcp-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/agent-platform-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/agent-platform-registry-reader-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/agent-platform-registry-writer-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/deck-library-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
```

The token goes to `curl` on its input rather than as an argument, so it never appears in the
process list another account on the machine can read.

They answer with `"actor":"orient","kind":"agent"`, `"actor":"orient","kind":"approved_client"`,
`"actor":"ops-mcp","kind":"agent"`, `"actor":"agent-platform","kind":"agent"`,
`"actor":"agent-platform-registry-reader","kind":"agent"`,
`"actor":"agent-platform-registry-writer","kind":"registrar"` and
`"actor":"deck","kind":"approved_client"`, each followed by what that credential
may do. The orient agent token and the registry-reader token both list `registry.read`; the
`agent-platform` token's list includes `review_record.create`; the registry-writer token lists
`registry.write` and nothing else; the `deck` token's list includes `epic.approve`. An answer of `no
resolvable identity` means the Library does not know that token; [a missing credential
file](installing.md#the-install-stops-at-mint_credentialpy-saying-already-has-a-credential) shows how
to replace one.

**`ops-mcp-token` answering here does not mean a crew's ops tools work.** No session presents it any
more; `bin/co` passes a crew's own `ops-co-<crew>-token` and a dispatched run its own
`ops-<crew>-token`, and only `agentctl crew doctor` still reads the shared one. [Your ops tools
fail](installing.md#claude-mcp-list-shows-kb-and-ops-as-connected-and-their-tools-fail) covers the
per-crew file instead.

**Your clones in `~/src` are separate from what runs.** The install copies each repository from its
`stable` branch into `~/.local/deploy`, since that is what you cloned, so you can edit or switch
branches in `~/src` without changing what is running.

To see what is installed, and whether it is current:

```
python3 ~/src/shipwright/bin/stand-up-backend --shape single --status
```

## Moving to a later release

Move an install to a later release with the one command that installs Builder, adding `--update`
and naming your install's shape:

```
curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --update --shape single
brew upgrade builder && builder-install --update --shape single          # on a Mac with Homebrew
```

Name the shape the way [One account vs. multiple accounts on the
server](accounts-on-the-server.md) names it: `--shape single`, `--shape two` or `--shape three`.

On a two- or three-account install, run the command from the administrator's own account, never
from `agents`, and expect the administrator password once.

`--update` installs nothing itself: it finds your install's own `builder-update` and hands off to
it, passing `--release` and `--plan` along when you give them. An install whose release already
carries `builder-update` can also run it directly:

```
builder-update --shape single
```

It reports the installed release, the release it will move to, every step it will take and which
account runs each one, warns that the Library and Orient will be down until it finishes, and asks
you to confirm. `--plan` prints the same report and stops there without asking anything;
`--release vX.Y.Z` names a release other than the latest one.

Once you confirm, it moves every clone, stops every job, takes a snapshot of the database, places
the new release — running `install-payload`, `install-backend`, `link-commands` and
`register-mcp` for you, and, on the three-account install, the root-owned half as well —
re-renders and starts the jobs again, and checks itself, putting everything back if a step fails.
`--rollback` finishes an update that stopped partway.

Before it moves anything, it checks the target release the same way `builder-install --verify`
does, using the INSTALLED release's own copy of `release-signers`. It fetches the target's signed
manifest and checks the manifest's signature against that trust list, and each clone's commit
against what the manifest names. An install made before 0.7.0 carries no `release-signers` of its
own, so it refuses at that check; only an install already on a signed release can move past it. A
two- or three-account install also needs a release carrying `--restore-previous` (0.8.0) before it
can update; an install on an earlier release refuses.

Moving a single-account install from before 0.7.0 needs the manual route below once, to reach a
signed release; `builder-update` works from there on.

Running `install-payload`, which the step above does for you, also brings the starter set in your
knowledge repository up to the new release, when the repository's remote is a folder on this
machine, as the one the install made is. A knowledge repository whose remote is hosted, on GitHub
or elsewhere, is left alone, and the install says so. The update leaves any document you changed as
you have it and hands Builder's version to the steward. [Customizing
Builder](customizing.md#when-you-install-a-newer-release) says what it does to each document.

### Moving by hand

Pulling each clone's `stable` branch by hand, instead of running `builder-update`, checks nothing:

```
git -C ~/src/shipwright pull --ff-only origin stable
git -C ~/src/agent-platform pull --ff-only origin stable
git -C ~/src/library pull --ff-only origin stable
git -C ~/src/convivy-orient pull --ff-only origin stable
git -C ~/src/convivy-deck pull --ff-only origin stable
git -C ~/src/write-better fetch origin
git -C ~/src/write-better checkout -B main "$(curl -fsSL https://convivybuilder.org/releases/X.Y.Z/release-manifest | awk '$1 == "write-better" {print $2}')"
```

`write-better` has no `stable` branch; each release names the commit of it that belongs to the
release, and the last line puts the clone's `main` at that commit, where `builder-update` expects
it. What these commands pull is unverified until you
check it yourself. Run `curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --verify
vX.Y.Z`, naming the release you just pulled, before running `install-payload` and
`stand-up-backend`. Use the site's copy rather than `bin/builder-install` from your clone: a copy
run from inside a git checkout refuses to check the clones, because a clone's own trust list cannot
vouch for itself. Pointed at no local manifest, it fetches the release's signed manifest from
`convivybuilder.org` and checks the manifest's signature against `release-signers`, each of the six
clones' commit against what the manifest names, and the published archive's sha256, printing one
line per item; a release before 0.7.0 has no signed manifest to fetch, so there is nothing yet for
this check to confirm. Once that check passes, run `install-payload` and `stand-up-backend` again,
as your install page gives them; `install-payload --dry-run` shows what it would change first.

## Meet the steward

With the server installed, open Deck on your Mac laptop and add the server to it. Install Deck with
the same command, run on the laptop instead, if you have not already:

```
curl -fsSL https://convivybuilder.org/install.sh | sh -s -- --role laptop
```

In Deck, press **⌘,** to open Settings, click the **Hosts** tab, then the **+** button. Fill in the
server's **Name:**, **User:** and **Address:** — or pick it from Deck's list of machines on your
Tailnet, if it offers one — then click **Pair this Mac…**.

Deck shows the server's host key fingerprint, a line starting `SHA256:`. The server's install
printed the one to expect as it finished, after "When Deck asks you to trust the machine, check
that it shows exactly:", along with the address and user to fill in. If that output is gone, run
this on the server to print it again:

```
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Click **Trust** once the two match.

On a Mac server, the file is the same. A fingerprint that does not match means Deck reached some
other machine, so do not trust it. Click **Cancel**, check the server's **Address:** for a typo and
that the laptop is on the network you expect, and pair again; cancelling and retrying is always safe.
If the fingerprints still differ, stop and find out why before going further.

Once you click **Trust**, Deck asks for the account's password once, in a **Password** field, and
sends it over the connection you just checked. Deck uses it to install the laptop's own key on the
server's account, so a later connection needs no password. Enter it and click **Install Key**.

Back in the Add Host sheet, click **Add**. Once the server is reachable and holds no crew yet, Deck
creates the steward and shows it on the rail, with a note reading "Steward crew created on
"<name>"". Click that row to open a terminal attached to it. The steward is the first session you
meet; tell it what you want to build, in plain language. It asks what it needs to know and then
creates a crew for the project.

**These steps have not been rehearsed end to end**, as [What does not work
yet](install-status.md) says.

**If Deck cannot reach the server**, meet the steward by hand instead. On the server:

```
cd ~/builder/steward
claude
```

The first line moves into the steward's folder, and the second starts Claude there; the conversation
that opens is the steward.

## Approving from Deck with a Touch ID press

Deck's **Approve**, **Decline** and model-choice buttons work without any of this, carrying your
account's own credential the way every other call to the server does. What this section adds is a
proof, signed on your Mac with a Touch ID press, that the server checks before it accepts one of
those three acts — so the act is tied to a key only your Mac's Secure Enclave holds, rather than to
whichever process on the server happens to hold Deck's credential. Skip this section and those three
buttons keep working exactly as they do today; add it and they start asking for a Touch ID press,
and the server starts refusing an approve, a decline or a model choice that arrives without one.

**Do this once per Mac, and once per server.** The root below is made once, ever, on whichever Mac
makes it first. Each Mac that runs Deck then gets its own signing certificate, under that same root;
a second Mac never makes a second root. The server gets the root certificate once, and gets one more
signing certificate enrolled for every Mac you add after the first.

### On the Mac: make the root, once

`root-ca` is linked into `~/.local/bin` by the laptop install, alongside Deck itself, so it is already
on your PATH once Deck is installed. Making the root asks for Touch ID (or your account's password, on
a Mac with no Touch ID), because the key it protects is generated inside the Secure Enclave and never
leaves it:

```
root-ca generate-root --out ~/root-ca.crt
```

Keep `~/root-ca.crt`; you will copy it to the server below, and to every other Mac's own copy of this
step is unnecessary — only the FIRST Mac runs `generate-root`. A second Mac goes straight to the next
section, using this same root certificate, carried over from the first.

### On the Mac: make this Mac's own signing key, in Deck

Open Deck's signing-key settings and create this Mac's own Secure Enclave key and a certificate
request from it; Deck exports the request as a file. This is also behind Touch ID, since the key it
makes is a second Secure Enclave key, never the root's.

### On the Mac: sign this Mac's request

```
root-ca sign-signer --email <your email> --machine your-mac-name \
  --csr ~/Downloads/deck-signing-request.csr --root-cert ~/root-ca.crt --out ~/deck-signer.crt
```

`--email` is your own email, lower case; `--machine` is a short name for this Mac (lowercase letters,
digits and hyphens only), which is what the server's refusal message below names when this Mac's
signature does not verify. This asks for Touch ID again, to use the root's key, and prints the
request's own public-key fingerprint before it signs — compare that against the fingerprint Deck's
settings show for the request it made, and stop if they differ; signing the wrong request would hand
a certificate naming this Mac to a key that is not this Mac's own. It then prints the issued
certificate's fingerprint and expiry, which is what the server will report back once you enroll it.

### On the Mac: give the certificate back to Deck

Back in Deck's signing-key settings, import `~/deck-signer.crt`. Deck now holds, behind the Secure
Enclave, the one key it needs to sign an approve, a decline or a model choice.

### On the server: enroll this Mac's signing certificate

Copy both files to the server — `scp` or any other way you already trust — then run the one command
that places the root (the first time) and enrolls this Mac's signer (every time):

```
python3 ~/src/shipwright/bin/enroll-signer --root-cert root-ca.crt --signer-cert deck-signer.crt
```

It checks the signing certificate against every rule the Library's protocol states for one — signed
directly by the root, with the right purpose, key usage and subject names — before it changes
anything, and refuses naming which rule failed if the certificate does not meet them. On a two- or
three-account install, run it with `sudo`; the Library's own account holds the root certificate and
the registry this enrolls into, and only root can reach that account without opening its home
directly. `--check` reports whether the root is placed and whether a given signer is enrolled,
without changing anything:

```
python3 ~/src/shipwright/bin/enroll-signer --check --root-cert root-ca.crt --signer-cert deck-signer.crt
```

**If you skip this, or enroll the wrong certificate, Deck's Approve, Decline and model-choice acts
still work for everyone else**, and for this Mac too, carried by your account's own credential as
they were before. The one thing that changes once ANY Mac has been enrolled is that an act carrying a
signature the server cannot verify — a certificate it has never seen, one signed by a different root,
or one whose Touch ID proof has expired — is refused rather than quietly falling back; Deck shows that
as a failed approve or decline, and re-pressing it asks for Touch ID again.

### Adding a second Mac

Repeat "make this Mac's own signing key, in Deck", "sign this Mac's request" and "give the
certificate back to Deck" on the new Mac, using the SAME `root-ca.crt` the first Mac made — copy that
one file over, rather than running `root-ca generate-root` again. Then run `bin/enroll-signer` on the
server again, with that new Mac's own `--signer-cert` and the same `--root-cert`; the server already
holds the root, so this only enrolls the new signer. Making a second root would strand every
certificate the first one signed, and `bin/enroll-signer` refuses before it would let that happen.

## Your first crew

When the steward creates a crew, three things appear:

- a folder, `~/builder/<crew>`, where the crew's work lives, set up with the starter agents;
- a `tmux` session with the crew's name, where the crew's own Claude session runs as its crew
  orchestrator, started by `co`;
- a file under `~/.config/convivy/deck/crews.d/` that Deck reads. Deck is a Mac app, so on a Linux
  machine the file waits for a Mac to read it.

To watch or talk to the crew, attach to its session, putting the crew's name in place of `<crew>`:

```
tmux attach -t <crew>
```

You will see the crew's conversation with Claude, and you can type into it. To step away, press
`Ctrl-b` then `d`, which leaves the session running.

**A new crew's session waits for you before it starts.** Claude Code asks whether to trust the
crew's folder, once for each crew. On your first crew it also asks whether to accept
bypass-permissions mode, once for the account, because `co` starts every crew in that mode, where a
session runs commands without asking you first. These are yours to answer, and the steward leaves
them to you: attach to the crew's session and answer there.

The steward may tell you the crew's registration is incomplete. That check still looks for settings
Builder no longer uses, and its fix is under way; the crew's session works regardless.

## Backups

You do not have to set backups up. Every six hours, starting when it first runs, the install backs
up the Library's database, which holds the work queue; the Library's cold store,
`~/.local/state/library/cold.db`, where a job moves older signals every six hours; Orient's
database, `~/.orient-control/control.db`; the Library's blobs, which are the files it keeps outside
its database; and your knowledge repository. The projects registry is part of that Library backup:
it is one table in the Library's own database, never a file of its own. It does not back up your
crews' folders under `~/builder/<crew>` or Deck's list of crews, so keep a copy of those yourself,
for example by pushing each crew's work to its own remote. Each backup is checked before
it counts. Each copied database has to pass SQLite's integrity check and hold the same number of
rows as the database it came from, before Orient's push subscriptions are removed from its copy, and
the copy of the knowledge repository has to pass `git bundle verify`. Credentials and TLS keys, the
keys that secure the backend's encrypted connections, are left out, because a new install makes its
own. So are Orient's web-push subscriptions, one for each browser you let Orient notify, because
none would work after a restore: a new install makes its own notification key.

The backups stay on this machine, in `~/.local/state/builder-backup`. Your machine's own backups,
such as a VM snapshot, are what carry them off it.

**This covers the single-account install this page describes.** On the two- and three-account
shapes, the `agents` account that takes this backup must never get a readable copy of the
Library's database, cold store or blobs, so those three are backed up separately, every six hours,
by a job that runs as the Library's own service account, into `.local/state/builder-backup` under
that account's own home. On those shapes, `agents`' own `~/.local/state/builder-backup` holds only
Orient's database and the knowledge repository. The stale-backup notice at the start of a session
reports `agents`' backup alone, so nothing warns you if the Library account's backup stops. Restoring either shape is not written up here yet; nobody has rehearsed it end to end.

To take one now, before a reboot for instance:

```
builder-backup
```

It prints what it copied and ends with `bundle verified`. To see when the last one succeeded:

```
builder-backup --status
```

That prints `ok` with the time, or `STALE` when no backup has succeeded in the last 24 hours, and
then exits 1. When a run fails, `--status` also prints the reason.

You will hear about a stale backup without asking. Each Claude Code session runs the same check as
it starts or resumes, through a hook the install added to `~/.claude/settings.json`, and says
nothing while the backup is fresh. When it is stale, the session shows the `STALE` line and tells
you about it before anything else.

### Restoring onto a new install

Use these steps when a machine is lost or replaced and you want the Library, your projects
registry and your Reference Room back on a new one. Your crews' folders come back from wherever
you kept them. In outline, you stop Builder's services, put the backed-up databases and knowledge
repository in place, force-push the restored knowledge repository to its remote, and run the
install again.

**Run this only on a new install.** It replaces the new machine's database and knowledge repository
with the backup's, and anything written on that machine since its install is gone. The force push
also replaces `main` on the knowledge repository's remote, so if that remote is hosted, for example
on GitHub, anything pushed there since the backup is gone too.
`git -C ~/builder/knowledge remote -v` shows which remote that is. On a fresh install it is
`~/builder/.remotes/knowledge.git`, and if it names anything else, stop and decide whether you mean
to replace that remote's `main` before you run the push.

These steps have been run on Linux only; on a Mac the services are launchd jobs, and `systemctl`
does not exist. Install Builder on the new machine as [Installing Builder](installing.md) describes, then copy the backup's
`latest` folder to it, here as `~/restore`. Copy the backup's `blobs` folder too: it sits beside
`latest` in `~/.local/state/builder-backup`, not inside it, and holds the files the Library's
records point at. Then:

```
systemctl --user stop com.convivy.library.service com.convivy.orient.service com.convivy.knowledge-watcher.service
systemctl --user stop com.convivy.library.cold-tier.timer com.convivy.knowledge-autopull.timer com.convivy.builder-backup.timer
install -m 600 ~/restore/library.db ~/.local/state/library/library.db
rm -f ~/.local/state/library/library.db-wal ~/.local/state/library/library.db-shm
install -m 600 ~/restore/cold.db ~/.local/state/library/cold.db
rm -f ~/.local/state/library/cold.db-wal ~/.local/state/library/cold.db-shm
install -m 600 ~/restore/orient-control.db ~/.orient-control/control.db
rm -f ~/.orient-control/control.db-wal ~/.orient-control/control.db-shm
git -C ~/builder/knowledge fetch ~/restore/knowledge.bundle main:refs/remotes/backup/main
git -C ~/builder/knowledge reset --hard backup/main
git -C ~/builder/knowledge push --force origin main
python3 ~/src/shipwright/bin/stand-up-backend --shape single --seed-registry --activate
agentctl kb sync
```

The second line stops the three timed jobs that would otherwise open the database, pull into the
knowledge repository or start a backup partway through the restore. `stand-up-backend` starts them
again.

`install -m 600` copies each database readable by your account alone, which `cp` does not
guarantee for a file it creates.

Copy the contents of the backup's `blobs` folder into `~/.local/state/library/blobs/` before the
`stand-up-backend` line. Without them, the restored Library's records point at files that are not
there. Your projects registry needs no step of its own: `library.db`, copied into place above,
carries it as one of its tables, so restoring the database restores your crews with it.

The restore brings back the knowledge repository's `main` branch, which is what the Reference Room
serves. `stand-up-backend` brings the restored database up to the installed Library's version and
starts the services again. `agentctl kb sync` ends with `up to date at <commit>`, naming the last commit in the
backup. In a rehearsal on two Debian machines, a backup taken on the first was restored onto a fresh
install on the second, and every line above exited 0 there. A document and a work item created before the backup, with a comment on the work
item, read back the same after the restore through a session's `kb_get` and `issue_get`, and
Builder's services were running again. The crew's folder came back from the copy kept in its own
remote, and its program ran.

Orient can stop once and start again during the `stand-up-backend` line, with `preflight FAILED`
in `~/.local/state/orient.log`, because it starts while the Library is still starting. A later
`preflight ok` in that log means it recovered.

## Removing Builder

This covers the single-account install this page describes. `bin/uninstall-builder` also removes
the two- and three-account shapes, each detected from what `install-privileged` recorded; those two
need `sudo`, since each stops the agents account's own system-scope jobs and removes the root-owned
tree and the accounts themselves. A three-account rehearsal found four defects in it, since fixed;
a two-account removal has not yet been rehearsed on real hardware.

```
python3 ~/src/shipwright/bin/uninstall-builder --dry-run
python3 ~/src/shipwright/bin/uninstall-builder
```

On the two-account and three-account shapes, run the same command with `sudo`:

```
sudo python3 ~/src/shipwright/bin/uninstall-builder --dry-run
sudo python3 ~/src/shipwright/bin/uninstall-builder
```

Every line above runs under whatever `python3` is first on `PATH`. On a Mac that is Apple's own,
older than the Python 3.11 a job declaration needs to read; this reexecs itself under Homebrew's
`python3.11` before that matters, or refuses, naming what to install, when neither is new enough.

The first line of each pair lists what it would remove and changes nothing. The second stops and
removes Builder's background jobs, the deploy areas under `~/.local/deploy`, the linked commands
and skills, the MCP registrations, the one hook it added to `~/.claude/settings.json`, and the rest
of Builder's state under `~/.local/state`. It also removes `~/.claude/CLAUDE.md` when it still matches
what this install shipped, and `~/.knowledge-index` when every entry in it is one it recognizes as part
of agent-platform's derived index. It removes only what an install placed; a file or link it did not
make stays, and the closing report names it and says why.

It asks before removing the Library's store and your backups, since they hold your work: the work
queue, the Library's own copy of what it has indexed, and every backup `builder-backup` has taken.
Answer no, or pass `--keep-data`, to keep them without being asked. Neither your crews under
`~/builder`, your knowledge repository, the steward's charter, nor the operator config under
`~/.config/convivy` are touched; they are yours, not the install's.

## Next

[Getting started](getting-started.md) describes a first week with the steward. [What does not work
yet](install-status.md) lists what Builder cannot do yet.
