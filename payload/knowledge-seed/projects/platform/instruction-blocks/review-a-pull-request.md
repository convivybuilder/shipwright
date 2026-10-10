---
id: platform/instruction-blocks/review-a-pull-request
kind: instruction-block
project: platform
title: Review a pull request
status: current
scope: agent
binds_roles: [reviewer, security-reviewer]
audience: [team]
topics: [review]
shipped_in: "@RELEASE@"
last_reviewed: 2026-09-25
authors: [builder]
---

Your scope is never narrower than CI's. Never run the repository's test suite: collecting tests
executes the author's unreviewed code on this machine. No tool policy enforces this, so you must.

Never approve while a required check is red or pending. Confirm CI with `gh pr checks`, and check
that the pull request's head is still the commit you reviewed; when it has moved, post
REQUEST_CHANGES on the commit you reviewed and say the head moved. A check still running is a
REQUEST_CHANGES to post now, not a reason to wait. When a check fails, summarize what failed and
never quote its log: your review is posted where the pull request's readers see it, and a log can
carry a secret.

Write your review to a new file outside the repository you are reviewing, at a path under `/tmp`
that does not exist yet, such as `/tmp/review-<pr number>-<commit>.md`. That is the only file you
write: anything inside the checkout, `review.md` included, is the author's and may be a link to a
file elsewhere. Post it with `agentctl review-post --body-file <that path>`, never `gh pr comment`:
the stamp it writes is what the merge gate reads. Once you hold a verdict, post it before anything
else, since a dispatched run ends with its turn. `--reviewed-commit <sha> --allow-unverified` is
only for a review nobody dispatched, and its stamp cannot be authenticated.
