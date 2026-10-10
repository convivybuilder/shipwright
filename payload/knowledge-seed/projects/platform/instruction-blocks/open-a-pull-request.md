---
id: platform/instruction-blocks/open-a-pull-request
kind: instruction-block
project: platform
title: Open a pull request and run its review cycle
status: current
scope: crew
binds_sessions: [interactive]
audience: [team]
topics: [review, pull-requests]
shipped_in: "@RELEASE@"
last_reviewed: 2026-09-25
authors: [builder]
---

Title a pull request with a Conventional Commits type: `feat:` when it adds capability, otherwise
`fix:`, `refactor:`, `perf:`, `chore:`, `docs:`, `test:`, `build:`, `ci:` or `revert:`, chosen by
the headline change.

Every pull request you open gets a `reviewer` and a `security-reviewer`, dispatched with `agentctl
spawn <agent> --on <repo> --pr <N> --task '<what to check>'` once the required CI is green.
`agentctl spawn` detaches the run, so start `agentctl wait <run-id>` in the background to hear when
it ends. Revise on any substantive finding and dispatch both again on the new head, including after
a one-line fix.

Read `agentctl review-status --pr <N> --repo <owner/repo>` as the verdict, and check each stamp's
reviewed commit against the current head. `review_rounds_per_role` in the agent policy,
`projects/platform/policy/agent-policy.yaml` in the knowledge repository, sets how many rounds each
reviewer role runs before the operator decides whether another happens. If the policy is missing or
cannot be read, the cap is five. At the cap, dispatch nothing more and bring the operator the open
findings with a recommendation.

When you give the operator a pull request's URL while its review is in flight, label it: "in review,
not ready to merge". Give a bare URL only for one that has passed. Post the full URL, since a
Markdown link renders as only the number.

A pull request that reverts merged work carries `Reverts: #<original PR>` and `Revert-reason:`, one
of `unwarranted` (the change rested on a wrong premise, even if its code was correct), `bug`,
`superseded`, or `other` with a one-line note.
