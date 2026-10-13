# Contributing

This repository is a release: a snapshot published from where the project
is actually written, with each release's commit stacked on the last.
Pull requests are welcome against `main`, and they get your change back to
where the project is written, for review there.

## Opening a pull request

Branch from `main` and open a pull request against it, as you would against
any repository.

**Sign off every commit.** Each commit needs a `Signed-off-by` trailer
naming you, which `git commit -s` adds for you:

```
git commit -s -m "Fix the thing"
```

Signing off is the Developer Certificate of Origin
(<https://developercertificate.org>): your statement that you wrote the
change, or otherwise have the right to submit it under this project's
licence. A commit with no `Signed-off-by` line, or one that does not match
the commit's own author, cannot be brought in.

## What happens next

A maintainer brings your pull request's commits into the repository where
the project is written, as one commit crediting you by name and email and
carrying your sign-off, and it is reviewed there like any other change. If
it needs changes, that conversation happens here, on the pull request.

This repository's own `main` never receives a merge. Once your change ships
in a release, this pull request closes with a comment linking that
release's commit, the point where your change first appears in this
repository's history.

## Licence

This repository is licensed under the Apache License, Version 2.0; see
[LICENSE](LICENSE) and [NOTICE](NOTICE). Opening a pull request with your
sign-off is how you agree your contribution is offered under those same
terms.
