---
id: platform/instruction-blocks/working-with-the-operator
kind: instruction-block
project: platform
title: Working with the operator
status: current
scope: crew
binds_sessions: [interactive]
audience: [team]
topics: [operator]
shipped_in: "@RELEASE@"
last_reviewed: 2026-09-25
authors: [builder]
---

Say what you are working on with `co-working-on "<what this session is doing right now>"`, and run
it when the work changes rather than on a schedule. Re-announcing the same text refreshes liveness
without resetting the duration, and new text starts its own clock. Write what someone watching the
pane would want to know, in at most 200 characters.

Reach the operator through your reply, and record work in the queue:

- A call that needs the operator: ask in session, ending on one concrete proposal with the legwork
  done, and name the alternative you would take if they say no.
- A defect or work item: `issue_create`, within the filing bar, then work it under a checkout and
  resolve it. The queue's state is the truth, so do not narrate the same status anywhere else.
- An observation worth keeping: `signal_log`.
