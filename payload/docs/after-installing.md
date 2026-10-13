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
| `~/.claude/skills` | the skills: `new-crew`, `new-subcrew`, `take-upstream` and `write-bead`, and the writing passes `write-better` and `talk-better` |
| `~/.claude/settings.json` | your Claude Code settings, to which the install adds one hook that tells a starting session when the backup is stale, and changes nothing else |
| `~/.local/deploy` | the installed copy of each repository, which is what runs |
| `~/.local/bin` | eleven commands, including `co`, which starts a crew's session, and `builder-backup` |
| `~/.local/state/builder-backup` | your backups: the latest, the one before it, and every blob either has held |
| `~/.config/systemd/user` on Linux, `~/Library/LaunchAgents` on a Mac | the background services |
| `~/.local/state` | the services' logs |
| `~/.local/state/library` | the Library's database, and the two files listing the credentials it accepts |
| `~/.orient-control` | Orient's database, its two Library credentials, `library-token` and `library-client-token`, the work-queue tools' credential, `ops-mcp-token`, and the credential reviewers post their records with, `agent-platform-token` |

The four credential files are secrets, as are `api-tokens.json`, `client-tokens.json` and
`bosun-client-token` in `~/.local/state/library`. Only your account and anyone with administrator
rights on the machine can read them; on a test Mac each was mode 600, a permission setting that
keeps other ordinary accounts out, in a folder other ordinary accounts cannot open. Check yours with
`ls -l ~/.orient-control ~/.local/state/library`: each credential file should read `-rw-------`.
Each of the four tokens in `~/.orient-control` is one the install generated on this machine, and the
Library accepts it because the install also recorded it in `~/.local/state/library`. Nothing copied
a credential from anywhere else.

To check that the Library accepts each one, run the four lines below. Each reads one credential
file and asks the Library, at an address on this machine, whose credential it is:

```
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/library-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/library-client-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/ops-mcp-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
printf 'Authorization: Bearer %s\n' "$(cat ~/.orient-control/agent-platform-token)" | curl -s -H "Library-Protocol: 1" -H @- http://127.0.0.1:8100/whoami
```

The token goes to `curl` on its input rather than as an argument, so it never appears in the
process list another account on the machine can read.

They answer with `"actor":"orient","kind":"agent"`, `"actor":"orient","kind":"approved_client"`,
`"actor":"ops-mcp","kind":"agent"` and `"actor":"agent-platform","kind":"agent"`, each followed by
what that credential may do. The last one's list includes `review_record.create`. An answer of `no
resolvable identity` means the Library does not know that token; [a missing credential
file](installing.md#the-install-stops-at-mint_credentialpy-saying-already-has-a-credential) shows how
to replace one.

**Your clones in `~/src` are separate from what runs.** The install copies each repository from its
`stable` branch into `~/.local/deploy`, since that is what you cloned, so you can edit or switch
branches in `~/src` without changing what is running.

To see what is installed, and whether it is current:

```
python3 ~/src/shipwright/bin/stand-up-backend --shape single --status
```

## Moving to a later release

Builder has no updater yet. To move to a later release, pull `stable` in each of the five released
clones first:

```
git -C ~/src/shipwright pull --ff-only origin stable
git -C ~/src/agent-platform pull --ff-only origin stable
git -C ~/src/library pull --ff-only origin stable
git -C ~/src/convivy-orient pull --ff-only origin stable
git -C ~/src/convivy-deck pull --ff-only origin stable
git -C ~/src/write-better pull --ff-only origin main
```

`write-better` has no `stable` branch, so the last line pulls its own `main`. Then run
`install-payload` and `stand-up-backend` again, as your install page gives them.

Running `install-payload` from a newer release also brings the starter set in your knowledge
repository up to that release, when the repository's remote is a folder on this machine, as the one
the install made is. A knowledge repository whose remote is hosted, on GitHub or elsewhere, is left
alone, and the install says so. The update leaves any document you changed as you have it and hands
Builder's version to the steward. [Customizing
Builder](customizing.md#when-you-install-a-newer-release) says what it does to each document. To see
what an update would change before it changes anything, run `install-payload` with `--dry-run`
first.

Updating the rest of what runs, the backend and its services, has not been tested yet.

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

**These steps have not been rehearsed end to end** — see [What works and what does not
yet](install-status.md).

**If Deck cannot reach the server**, meet the steward by hand instead. On the server:

```
cd ~/builder/steward
claude
```

The first line moves into the steward's folder, and the second starts Claude there; the conversation
that opens is the steward.

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
its database; and your knowledge repository. It does not back up your crews' folders under
`~/builder/<crew>`, your projects registry or Deck's list of crews, so keep a copy of those
yourself, for example by pushing each crew's work to its own remote. Each backup is checked before
it counts. Each copied database has to pass SQLite's integrity check and hold the same number of
rows as the database it came from, before Orient's push subscriptions are removed from its copy, and
the copy of the knowledge repository has to pass `git bundle verify`. Credentials and TLS keys, the
keys that secure the backend's encrypted connections, are left out, because a new install makes its
own. So are Orient's web-push subscriptions, one for each browser you let Orient notify, because
none would work after a restore: a new install makes its own notification key.

The backups stay on this machine, in `~/.local/state/builder-backup`. Your machine's own backups,
such as a VM snapshot, are what carry them off it.

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

Use these steps when a machine is lost or replaced and you want the Library and your Reference Room
back on a new one. Your crews' folders and your projects registry come back from wherever you kept
them. In outline, you stop Builder's services, put the backed-up databases and knowledge repository
in place, force-push the restored knowledge repository to its remote, and run the install again.

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

The `install -m 600` form of the `library.db` line, and the lines that restore `cold.db` and
Orient's `control.db`, have not yet been run on the test machine. `install -m 600` copies each
database readable by your account alone, which `cp` does not guarantee for a file it creates.

Copy the contents of the backup's `blobs` folder into `~/.local/state/library/blobs/` before the
`stand-up-backend` line. Without them, the restored Library's records point at files that are not
there. Put your saved projects registry back at
`~/.local/deploy/agent-platform/config/projects.json` before that line too: the install keeps the
registry it finds there, and without one it starts again from Builder's seed, which lists none of
your crews.

The restore brings back the knowledge repository's `main` branch, which is what the Reference Room
serves. `stand-up-backend` brings the restored database up to the installed Library's version and
starts the services again. `agentctl kb sync` ends with `up to date at <commit>`, naming the last commit in the
backup. On the test machine, a document and two work items created before the backup, with a comment
on one, read back the same after the restore through a session's `kb_get` and `issue_get`.

## Next

[Getting started](getting-started.md) describes a first week with the steward. [What works and what
does not yet](install-status.md) lists what 0.6.0 has been seen doing, and what it cannot do yet.
