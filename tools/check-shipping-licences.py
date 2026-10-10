#!/usr/bin/env python3
"""Every repository a release ships carries LICENSE and NOTICE.

Builder is licensed Apache-2.0 **for the NOTICE mechanism
specifically**: it is how Convivy's attribution survives redistribution. A
repository without a NOTICE gives a forker nothing to retain, so the licence
does not do the one job it was chosen for.

**This checks presence, not content, and the NOTICE half is the reason.** Under
Apache-2.0 a NOTICE accumulates the attributions of whatever a repository
bundles, so two shipping repositories are *expected* to diverge as soon as one
vendors a dependency the other does not. A byte-comparison against shipwright's
copy would refuse that, which is the file working rather than failing. Nobody
has yet seen a wrong or truncated licence here, so there is no content rule to
write; presence is what was asked for and presence is what this checks.

It takes PATHS rather than repository names, so it carries no list of what
Builder ships — `bin/publish-payload` resolves `--ships` and passes the roots.
Run standalone with the roots you care about:

    tools/check-shipping-licences.py ~/code/shipwright ~/code/library

**DO NOT MAKE THIS ENUMERATE REPOSITORIES.** Taking roots from the caller is
what keeps other repositories out, and keeping them out matters. A company's
website repository, for one, must never receive these files: there an absent
LICENSE means all rights reserved, and adding Apache-2.0 would not retain
anything but would grant the public a licence to copy the site's content, its
posts and its design. It vendors no engine code, so nothing it distributes carries a
section 4(d) obligation either.

The hazard is the obvious sweep, *add LICENSE to every repository missing one*,
which is a fix everywhere else and a giveaway there. A checker that walked
every repository on disk and reported what it found would invite exactly that
sweep and would report the website repository as a finding. This one cannot, because it is told what to look at.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROG = "check-shipping-licences"
REQUIRED = ("LICENSE", "NOTICE")


def findings_for(roots: list[Path], labels: list[str]) -> list[str]:
    """One line per missing file, or per root that cannot be checked."""
    findings = []
    for root, label in zip(roots, labels, strict=True):
        if not root.is_dir():
            findings.append(f"{root}: not a directory, so its licence files cannot be checked")
            continue
        for name in REQUIRED:
            if not (root / name).is_file():
                findings.append(f"{label}/{name}: missing")
    return findings


def main(argv: list[str]) -> int:
    # `--names a,b,...` labels the roots in order. Without it each root is
    # labelled by its directory name, which is wrong for a git worktree:
    # `publish-payload` run from one reported the worktree's directory as a
    # repository it had verified, so it passes the `--ships` names instead.
    labels = None
    if argv[:1] == ["--names"]:
        if len(argv) < 2:
            print(f"{PROG}: --names needs a comma-separated list", file=sys.stderr)
            return 2
        labels = argv[1].split(",")
        argv = argv[2:]
    if not argv:
        print(f"{PROG}: name at least one repository root to check", file=sys.stderr)
        return 2

    roots = [Path(arg).resolve() for arg in argv]
    if labels is None:
        labels = [root.name for root in roots]
    elif len(labels) != len(roots):
        print(
            f"{PROG}: --names gave {len(labels)} name(s) for {len(roots)} root(s)",
            file=sys.stderr,
        )
        return 2
    findings = findings_for(roots, labels)

    if findings:
        print(f"{PROG}: FAIL — a shipping repository is missing its Apache-2.0 files")
        for finding in findings:
            print(f"  {finding}")
        print()
        print("Builder is licensed Apache-2.0 for the NOTICE mechanism, which")
        print("is what retains Convivy's attribution when someone forks. A repository")
        print("without one hands a forker nothing to keep.")
        return 1

    # SAYS WHAT IT VERIFIED, with the count and the names. A bare "ok" here would
    # read the same whether it checked five roots or none, and an empty argument
    # list is exactly how this check would silently stop checking anything —
    # which is why no argument is an error above rather than a vacuous pass.
    noun = "repository" if len(roots) == 1 else "repositories"
    verb = "carries" if len(roots) == 1 else "carry"
    print(
        f"{PROG}: PASS — {len(roots)} {noun} {verb} "
        f"{' and '.join(REQUIRED)}: {', '.join(sorted(labels))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
