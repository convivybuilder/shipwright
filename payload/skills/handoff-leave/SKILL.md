---
name: handoff-leave
description: Invoked as /handoff-leave when ending a co session that has work in flight
  or context worth preserving for a future session, such as before a break or before
  re-activating after a knowledge-base change.
---

# `/handoff-leave` — write a handoff doc before exit

This `co` session is about to exit. Capture session state in a structured doc so a
future `co` session can `/handoff-pickup` and continue. Keep it tight — this is a
handoff to the next session, not a deliverable.

## Where to write

Run this. It creates the directory and prints its absolute path:

```
agentctl session-dir --product "$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")"
```

Write `handoff.md` inside the directory it printed. **Do NOT compose the directory
name yourself, and do NOT infer the local time** — a `co` session that did exactly
that converted a UTC instant through "Mountain Time", picked up a daylight-saving
offset Arizona does not observe, and named its handoff an hour into the future. The
command makes that impossible: one clock read, in one place.

(The path it prints is absolute — surface that form, never a `~/` form, since on some
setups shorthand resolves against the wrong machine's home.)

Don't reuse an existing run-id directory — handoffs live in their own date-scoped dir,
not co-mingled with agentctl-spawned worker runs. `session-dir` already gives you one of
those.

## What to write

Use this exact section structure so `/handoff-pickup` knows where to look. Be specific
in each section; vague "we worked on stuff" is failure mode.

```markdown
# Co session handoff

**Product:** <product>
**Started:** <approximate session start time, your best estimate>
**Left:** <date +%Y-%m-%d %H:%M %Z>
**Why exiting:** <one line — sleep, re-activate after KB change, context approaching limit, etc.>

## State summary

<2–4 sentences. What was the goal of this session? What's the current state of the work? Lead with the most actionable framing.>

## In-flight items

<Bullet list. For each: what it is, where it lives (PR URL / run dir path / file path), and what step it's at. Include PRs awaiting the operator's merge, pending review cycles, deferred decisions. Dispatched workers still running go in the machine-written section below, not here.>

- ...

## In-flight runs (machine-written)

<Run `agentctl list --co-session "$CLAUDE_CODE_SESSION_ID"` and paste its output here verbatim, including `(no active runs)` if that is what it printed. Do not list runs from memory.>

## Decisions made this session

<Bullet list of meaningful choices that affect future work. Skip routine choices. Include any ADR / ARCH numbers if surfaced. If none, write "None.">

- ...

## Open questions / blockers

<Anything the operator needs to think about or resolve before the next session can proceed. If none, write "None.">

- ...

## Recommended next move

<One short paragraph. What should the next session do first? Be specific — "run `make test` then dispatch reviewer on PR #X" beats "continue the work.">
```

## State a cause only where you observed it

**When you write that something died, give the exit code, the signal, or the reason the
task notification itself stated, quoted.** "The waiter exited 3 and `agentctl status`
showed the run alive" is a handoff fact. So is "the task notification said it was
stopped because the system was running low on memory". What does not belong in a handoff
is a cause you read nowhere: supplying memory pressure, a timeout, a rate limit or a
flaky network because it fits the story. The same holds for every cause a handoff names.
Write what you saw, and the command or notification that showed it.

**Both reasons the harness names are real, and it names them in the notification.**
Claude Code reaps every running background task on a `memoryPressure` event, stamping
the reason `memory_pressure`, whose text is "stopped because the system is running low
on memory"; the env switch `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` turns that reaper
off. Its other named reason is a timeout, the cap on how long a backgrounded task may
live. Memory pressure is the common reason on an install where the reaper is still on,
arriving in bursts at one instant as the reaper takes every live task at once, where a
timeout arrives alone. **This reaper can be switched off for good** by setting
`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` in `~/.claude/settings.json`, where the
switch stays once set. **The switch reaches a session already running**, not only one
launched afterwards: settings `env` entries are written into the harness's own
environment when settings load or reload, and the per-task registration reads that
environment, so a task started after the change is exempt whatever its session's age.
**A task that was already registered keeps the handler it had**, so it can still be
reaped for memory until it ends. For everything started since the switch was set, a
timeout is the reason left. Which reason a given notification carries is still the
notification's to state, so read it and repeat its reason rather than deducing one from
whether the switch is set.

**This section exists because a handoff's prose is read as fact by whoever picks it up,
and the pickup copies it forward with the hedging gone.** Several handoffs have said
waiters, watchers or poll loops were "killed for low memory" while citing nothing, and
one named a watcher process with no source file and no log. The first correction went the
other way and was also wrong: a `log show` query for a kernel memorystatus kill returns
nothing, and that silence was read as proof no such kill happens. The kernel only raises
the pressure warning; the harness does the killing and records it in the transcript,
where no kernel predicate can see it. Neither an unevidenced claim nor an unevidenced
denial is a handoff fact.

## Release every kb lease before you go

**A lease does not survive the session that took it.** `kb_checkout` records the holder
as `session:<id>`, and a successor session has a new one, so a document held "for the
next session" refuses that session's own checkout with `error: leased` until the
four-hour TTL expires. A rollover closes the predecessor's pane, so nothing can release
it politely. A handoff has held a document for the very PR its successor was told to
open, blocking the successor for hours.

**So list your leases with `kb_leases`, release each one this session holds with
`kb_release`, and name the documents in the in-flight item that needs them**, saying the
next session must check them out itself. The checkout belongs to whoever does the
writing.

`agentctl kb release --holder <session id>` frees a lease recorded under another
session's name, **and it is the operator's command to run rather than yours**, including
when the operator says in session that the lease should go. The reason is in the
mechanism rather than in a rule written elsewhere: this lease is a flat four-hour TTL and
nothing more. So "the holder is dead" is your belief rather than anything the store can
confirm, and a release made on a wrong one drops a live fence with no error. Other lease
systems in this product keep breaking a live hold for a person, and they at least carry a
heartbeat to judge liveness by; this one carries none, which argues the same way with
less to go on. Releasing before you exit is what keeps anyone from needing it.

## Hand back every work-item checkout before you go

**A work-item checkout outlives its session the same way.** `issue_checkout` records the
`owner` you passed, and only that owner may write the item: resolve it, correct it, link
a PR to it. A successor has its own name and may not pass yours, so an item you hold
stays shut to it until the lease's grace period runs out, four hours from the last
heartbeat. A session has rolled over holding an item whose PR the operator merged an
hour later, and the successor could not close it for hours more.

**So list what you hold with `lease_list(holder="<your owner name>")`, and release each
item with `issue_release`, passing that same owner.** What a release does depends on the
item's state:

- **`pr-open`:** the release drops only the fence. The item stays `pr-open` and nothing
  re-queues it, so this costs nothing.
- **`claimed`:** the release returns the item to `open`, where any session can take it.
  Release it anyway, and put it first in "Recommended next move", so the successor's
  first act is to take it again.

Name each released item in its in-flight entry by key and id, with the state you left it
in, and say the next session acts on it under its own name, as `/handoff-pickup`
describes. Then add a line near the top of the handoff saying that you released every
work-item checkout and naming any release that was refused, quoting the refusal. A
refused release stays held until its grace period ends, and the successor must wait for
it to end rather than write as you.

## On completion

Surface a one-line ack to the operator with the path:

> Handoff at `$(builder-root)/agent-runs/2026-05-20/co-shop-2245/handoff.md`. Pick up
> next session with `/handoff-pickup`.

Don't ask the operator if the doc looks right; it can always be edited later. Don't post
to Slack. Don't dispatch further workers — this is a session-end skill, not a
continuation.

## When NOT to leave a handoff

- The session has no in-flight work and no non-obvious context (e.g. you just answered a
  one-shot question). Tell the operator "no handoff needed — nothing to carry forward"
  and exit cleanly.

A worker still running when the operator invokes this is not a reason to stop and ask:
dispatched runs outlive this session. Record them in the "In-flight runs
(machine-written)" section from `agentctl list --co-session "$CLAUDE_CODE_SESSION_ID"`,
and the successor's `/handoff-pickup` re-attaches to them.
