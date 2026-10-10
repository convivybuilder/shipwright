---
name: new-subcrew
description: Create a child session under the crew you are already working in — its tmux session in the crew's directory, and the spec Deck reads to draw it nested under the parent. Use when you need a second session for the same project (a long-running build, a parallel investigation, a side conversation). Any co can run this for its OWN crew; creating a whole new crew is the steward's new-crew instead.
---

Create a child session under your own crew: a tmux session in the crew's working directory, and a pinned-child entry Deck reads to draw it nested under the parent row.

**Only for your own crew.** If the session belongs to a different project, or needs its own directory, it is a crew rather than a child — ask the steward to run `new-crew`. A child shares its parent's working directory; that is what makes it a child.

## Establish the parent first

You are running inside the parent's tmux session, so read it rather than assuming:

```bash
tmux display-message -p '#{session_name}'
```

This form is safe because it asks about the CURRENT session and passes no `-t` target. Then confirm the crew's spec exists and read its directory:

```bash
cat ~/.config/convivy/deck/crews.d/<parent>.json
```

If there is no spec for your crew, stop and say so. Do not create one — a crew without a spec was made outside this path, and inventing its directory is how a child ends up somewhere the parent is not.

## Name the child

The name is **`<parent>--<child>`**, with a DOUBLE hyphen. That separator is what Deck's grouping matches on (`SessionGrouping.matchesByName`); a single hyphen makes the session look like an unrelated crew whose name happens to start with the parent's, and it will not nest.

Keep `<child>` short and descriptive of the work: `shop--build`, `shop--catalog-import`.

## Create it in the parent's directory

```bash
tmux new-session -d -s "<parent>--<child>" -c "<the parent's workingDirectory>" 'co; exec "$SHELL"'
```

**`co` is the pane's command, never typed into it.** A pane's shell is whatever `$SHELL` the tmux server started with, and inside a Claude session that is zsh once zsh is installed. On an account with no zsh startup files, an interactive zsh opens its new-user wizard, and a typed `co` answers the wizard instead of running. The steward met exactly that on a fresh Linux install. A pane command runs without an interactive shell, so the wizard never starts before `co` does. `exec "$SHELL"` gives the pane a shell once `co` exits, and on such an account that shell shows the wizard then; it is harmless there, since `co` has already run. Answer `0` to it, which leaves a `~/.zshrc` holding only a comment.

**Pass `-c` with the parent's directory every time.** Without it tmux creates the session in `$HOME`, `bin/co` will not find the project, and the row cannot be grouped under the parent. `-c` is honoured only at creation — a session made without it must be killed and recreated, not patched.

## Capture the session id

```bash
tmux list-sessions -F '#{session_id} #{session_name}' |
  while read -r sid name; do [ "$name" = "<parent>--<child>" ] && printf '%s\n' "$sid"; done
```

**Use this exact form. Never a bare `tmux ... -t <name>` target**, and do not use the `=` exact-match prefix — measured on tmux 3.6a it still matched a different session whose name merely started with the target. Comparing each full name in the listing is the only form that cannot resolve to a neighbour.

The id is a dollar sign followed by a number, and it survives a rename. Recording it is what lets Deck tell a renamed session from a new one; without it, renaming a child makes Deck draw two rows for one session.

## Append to the parent's spec

Add an entry to the parent's `sessions` array in `~/.config/convivy/deck/crews.d/<parent>.json`. Read, append, write — never overwrite the file with only your entry.

```json
{
  "name": "<parent>--<child>",
  "displayName": "<what a person reads, e.g. Build>",
  "sessionId": "<the $N captured above>"
}
```

`displayName` is what the rail shows, so make it a short human label rather than repeating the tmux name.

## Report

Say the session name, that it is running in the parent's directory, and what it is for. If Deck does not draw the nested row, the session is still reachable — it will appear under the parent through discovery, or under OTHER SESSIONS.

## Clean up when the work is done

A child session left running holds a row forever and a stale spec entry outlives the session it names. When the work it was made for is finished, kill the session and remove its entry from the parent's `sessions` array. **Removing the entry without killing the session, or the reverse, is what leaves a row that resurrects itself when clicked** — Deck attaches with `tmux new-session -A`, which creates when the session is absent.
