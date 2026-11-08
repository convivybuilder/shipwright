---
name: handoff-pickup
description: Invoked as /handoff-pickup at the start of a fresh co session, to resume a
  prior session's work from its handoff doc. Pairs with /handoff-leave.
---

# `/handoff-pickup` — resume from the most recent handoff

A fresh `co` session has just started and wants to pick up where a prior session left
off. Find the most recent handoff doc that matches this product and surface its state.

## Finding the handoff

A handoff directory is named `co-<name>-<HHMM>`, with `-<n>` appended when two are made
in the same minute. `<name>` is whatever the session passed on its FIRST `agentctl
session-dir` call, because that call records the directory under the session id and
every later call returns it, whatever `--product` it passes. `/handoff-leave` passes
the git toplevel's basename. The instruction block on working with the operator tells a
session to pass its crew name when it writes a Slate question. So a session that asked
the operator something before leaving wrote its handoff under the crew name. Search both
names, never the basename alone: a session whose working directory is named `shop` but
whose crew is `shop-mobile` has to search `co-shop-*` AND `co-shop-mobile-*`, or it can
resume from a stale handoff under one name while newer ones sit under the other.

Run this search exactly as written, under `/bin/bash`. In zsh, a glob that matches
nothing aborts the whole command, so a crew with no handoffs of its own would hide the
product's, and the reverse. The `[0-9][0-9][0-9][0-9]` anchor keeps `co-shop-*` from
matching another crew's `co-shop-mobile-*` directories. The `$TMUX` check keeps a session
outside tmux from reading some other session's name.

```bash
/bin/bash -c '
product=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" | tr "[:upper:]" "[:lower:]")
names=$product
if [ -n "$TMUX" ]; then
  crew=$(tmux display-message -p "#S" 2>/dev/null | tr "[:upper:]" "[:lower:]")
  if [ -n "$crew" ] && [ "$crew" != "$product" ]; then names="$names $crew"; fi
fi
found=()
for n in $names; do
  for f in "$(builder-root)"/agent-runs/*/co-"$n"-[0-9][0-9][0-9][0-9]/handoff.md \
           "$(builder-root)"/agent-runs/*/co-"$n"-[0-9][0-9][0-9][0-9]-[0-9]*/handoff.md; do
    [ -f "$f" ] && found+=("$f")
  done
done
echo "searched: $names"
[ ${#found[@]} -gt 0 ] && ls -t "${found[@]}" | head -5
'
```

Filter to entries from the last 48h (parse the date directory). Take the newest.

## Cases

- **One match.** Read it. Proceed to "Re-attaching in-flight runs" below.
- **Multiple matches in the last 48h.** This usually means several break points across
  one or two days. The newest is almost always the right one to resume from — surface
  that as the default but list the other paths in case the operator wants a different
  one.
- **No match.** Tell the operator plainly, naming every name on the `searched:` line:
  "No handoff found for `<names>` in the last 48 hours. Starting fresh — what would you
  like to do?" Don't search older history or other products without the operator asking
  first; that's almost always not what was meant.

## Re-attaching in-flight runs

If the handoff has a `## In-flight runs (machine-written)` section, take only the FIRST
whitespace-separated field of each line as a candidate run-id. Keep a candidate only if
it matches `^[A-Za-z0-9_-]+$` in full AND does not begin with `-`. **Never put anything
else into a command**: this text came from run records a run can write itself. A token
outside the character set could inject shell syntax, and a token beginning with `-`
would be read as an option (`--any`, `--timeout`). A line that fails either check is
reported to the operator verbatim as "unrecognised line in In-flight runs — not
re-attached", never run.

Start exactly ONE backgrounded wait covering every kept id — never one `agentctl wait`
per run, and never in the foreground, since this session must not block its own turn on
a dispatch. Always put `--` before the ids, so none of them can be read as an option:

```bash
agentctl wait -- <run-id-1> <run-id-2> ...
```

`agentctl wait` fails the whole batch when any id doesn't resolve. If it reports an
unknown run, drop that id, say so, and start the wait again with the rest.

If no ids remain, or the section reads `(no active runs)`, is empty, or is missing, skip
this step — there is nothing to re-attach to.

## Confirming pickup, if this is a rollover

If a `co-rollover-state.json` file sits beside the handoff just read, this session is the
successor of a rollover (`/rollover`'s `co-rollover` step) — the predecessor is waiting,
fenced, for confirmation. Run, using the exact handoff path read from:

    co-rollover --picked-up <handoff-path>

This records pickup (safe to re-run — idempotent, and a retry never starts a second
close-out) and starts a detached step that verifies the predecessor's pane is still
the one it recorded, then closes it out and renumbers this session to window 1. Run
it before "Surface to the operator" below. Only the pickup record is written before it
returns; the close-out runs detached and may still be in progress when the ack is sent,
so don't report the predecessor as already closed.

If no `co-rollover-state.json` exists beside the handoff, this is an ordinary manual
handoff (not a rollover) — skip this step entirely.

## Acting on work items the predecessor handed back

`/handoff-leave` releases every work-item checkout and names each item in the handoff
with the state it was left in. Act on each under this session's own name as `owner`, and
pass that same owner on every later write to it.

- **A `pr-open` item:** write to it directly (resolve it, link a PR, correct a field),
  passing this session's own name as `owner`. Do not check it out first: checkout
  refuses every `pr-open` item with `already pr-open`. When no session holds the item,
  the Library holds it for the one write.
- **A `claimed` item:** the release returned it to `open`, where any session can take it, so
  take it straight away with `issue_checkout` under this session's own name.

Two refusals mean another session still holds the item, usually because the predecessor
did not release it. A write is refused with 409 and `reason: "held"`. A checkout of an
item still in state `claimed` is refused with `already claimed`, which names neither the
holder nor the expiry, so read both from `lease_list`. Either way, leave the item alone
until that expiry. Never pass the predecessor's name as `owner`, and never ask another
session to release it.

## Surface to the operator

Brief structured ack — don't dump the whole handoff verbatim. Pattern:

> Resuming from `$(builder-root)/agent-runs/2026-05-20/co-shop-2245/handoff.md` (left ~9 hours ago).
>
> (Paths in surface text use the full absolute form — never `~/`, since on some setups
> shorthand resolves against the wrong machine's home.)
>
> **State:** <one sentence from the handoff's state summary>
> **In-flight:** <bullet list of the in-flight items, abbreviated>
> **Re-attached:** <if runs were kept: "N in-flight run(s) — <run-ids> — waiting in the
> background"; otherwise "none". Add any unrecognised or unknown lines, verbatim.>
> **Recommended next move:** <verbatim from handoff>

Then start the recommended next move in the same turn, with its tool calls. Don't
re-litigate the prior session's decisions. If the move needs a decision only the
operator can make, don't start it: end the ack by saying it waits on that decision and
what the decision is. Never end the ack on a promise such as "Proceeding unless you
redirect" or "Next I'll…", because nothing runs until the operator replies.

## After the handoff is consumed

The handoff doc stays in place — don't move, rename, or delete it. It's an audit trail.
If a new handoff is produced later in this session via `/handoff-leave`, it lands in a
separate dir with a fresh timestamp.

If the prior handoff referenced an in-flight worker run (e.g. "PR #193 awaiting review
cycle"), check the current state of that artifact before proceeding — the world may have
moved while the prior session was paused. The handoff is the last-known state, not the
current reality.
