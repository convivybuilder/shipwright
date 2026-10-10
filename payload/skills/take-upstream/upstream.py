#!/usr/bin/env python3
"""upstream.py: read Builder's change digests against a fork, and take the changes chosen.

A fork of Builder has no updater. Each upstream release ships a CHANGES.md
describing every change since the release before it, and this tool reads those
digests against the fork so its owner can choose which changes to take.

    upstream.py report  [--upstream REF] [--base BRANCH] [--json]
    upstream.py apply   CHANGE_ID... [--upstream REF] [--base BRANCH] [--open-prs] [--remote NAME]
    upstream.py decline CHANGE_ID... [--upstream REF] [--base BRANCH]
    upstream.py merged  CHANGE_ID... [--upstream REF] [--base BRANCH]

Run it from the root of the fork's checkout. REF names the upstream branch
after a fetch, `upstream/main` by default. BRANCH is the fork's main branch,
`main` by default: every command reads the fork from it, and apply builds on it.

WHICH RELEASES. The release.json on BRANCH names the release the fork was
forked from. Every release on REF newer than that one is read, oldest first, so a fork
several releases behind sees every change it has not yet taken or declined.

HOW A CHANGE IS CLASSIFIED. Each file a change touches is compared three ways:
the fork's committed copy, upstream's copy in the release before the change,
and upstream's copy in the release that made it.

- The fork holds the new copy, or a later release's copy, or merging the
  change would leave the fork's copy as it is: that file is taken.
- The fork still holds the old copy, or its own edits merge cleanly with the
  change: that file applies cleanly.
- Anything else conflicts, and a person merges it by hand. So does a file
  upstream gives as anything but a regular or executable file, and anything
  under the fork's .builder/ directory, which this tool owns.

A change recorded in DECISIONS is declined or taken, as recorded. Otherwise it
conflicts if any file does, is taken if every file is, and applies cleanly if
not.

WHAT APPLY DOES. For each change it builds one branch from the base branch with
git plumbing, leaving the working tree and the current branch alone, commits the
change's files with its What and Why, and with --open-prs pushes the branch and
opens one pull request, so each change goes through the fork's own review.

WHAT DECLINE AND MERGED DO. Each records the operator's decision about a change
in DECISIONS, in the working tree, for the operator to commit through the fork's
normal review. `decline` records a change the fork will not take, and later
reports show it as declined. `merged` records a change the operator merged by
hand, and later reports show it as taken. A hand merge that combines both sides'
edits on the same lines still conflicts when compared file by file, so without
this record it would be offered again forever (review, round 2).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PROG = "upstream.py"
DECISIONS = Path(".builder") / "upstream-decisions.json"
DECISION_KINDS = ("declined", "merged")
MANIFEST = "release.json"
DIGEST = "CHANGES.md"
FIELDS = {"What: ": "what", "Why: ": "why", "If your fork has diverged: ": "diverged"}
FILE_LINE = re.compile(r"^- `([^`]+)` (added|changed|removed)$")
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-(alpha|beta|rc)(?:\.(\d+))?)?$")
PRERELEASE_ORDER = {"alpha": 0, "beta": 1, "rc": 2}
# UPSTREAM CONTENT IS UNTRUSTED. A fork reads it from a remote it does not
# control, so three things are never taken automatically (security review):
# - a file whose mode is not a regular or executable file. A symlink committed
#   at the decisions record's path let a later `decline` write outside the
#   repository through it;
# - anything under the skill's own directory in the fork;
# - control characters in text printed to a terminal or put in a pull request.
TAKEABLE_MODES = {"100644": "a file", "100755": "an executable file"}
OWN_DIR = ".builder/"
# C0 and C1 controls, and the bidirectional, zero-width, invisible-operator and
# tag characters that make text read differently from what it says, or hide
# text from a person that a model still reads (security review, rounds 2 and 3).
CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f\u061c\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]")


class Refused(Exception):
    """Something the operator has to act on. Printed, never a traceback."""


def git(*args: str, stdin: bytes | None = None, env: dict | None = None, check: bool = True) -> bytes:
    result = subprocess.run(
        ["git", *args], input=stdin, capture_output=True, check=False,
        env={**os.environ, **(env or {})},
    )
    if check and result.returncode != 0:
        raise Refused(f"git {' '.join(args)} failed: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def entry_at(commit: str, path: str) -> tuple[str, str] | None:
    """The mode and blob id of `path` at `commit`, or None when the file is not there."""
    out = git("ls-tree", commit, "--", path).decode()
    for line in out.splitlines():
        meta, name = line.split("\t", 1)
        mode, kind, blob = meta.split()
        if name == path and kind == "blob":
            return mode, blob
    return None


def blob_at(commit: str, path: str) -> str | None:
    entry = entry_at(commit, path)
    return entry[1] if entry else None


def read_blob(blob: str) -> bytes:
    return git("cat-file", "blob", blob)


def version_key(version: str) -> tuple:
    match = VERSION.match(version)
    if not match:
        raise Refused(f"{version!r} is not a Builder release version")
    major, minor, patch, pre, pre_n = match.groups()
    # A release sorts after every prerelease of the same version.
    pre_key = (PRERELEASE_ORDER[pre], int(pre_n or 0)) if pre else (3, 0)
    return (int(major), int(minor), int(patch), pre_key)


def manifest_version(commit: str) -> str | None:
    blob = blob_at(commit, MANIFEST)
    if blob is None:
        return None
    try:
        version = json.loads(read_blob(blob)).get("version")
    except (ValueError, AttributeError):
        return None
    return version if isinstance(version, str) and VERSION.match(version) else None


def fork_base(base: str) -> str:
    if not git("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}", check=False).strip():
        raise Refused(f"{base} names no branch here; pass --base with the fork's main branch")
    version = manifest_version(base)
    if version is None:
        raise Refused(
            f"{base} has no readable {MANIFEST}, so the release this fork was forked from "
            f"is unknown. Run {PROG} from the root of the fork's checkout."
        )
    return version


def clean_text(text: str) -> str:
    return CONTROL.sub("", text)


def upstream_releases(ref: str) -> dict[str, str]:
    """Every release on `ref`, as version -> the commit that carries it."""
    if not git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False).strip():
        raise Refused(
            f"{ref} names no commit. Add Builder's public repository as a remote and "
            f"fetch it first: git remote add upstream <url> && git fetch upstream"
        )
    releases: dict[str, str] = {}
    log = git("log", "--first-parent", "--format=%H", ref, "--", MANIFEST).decode().split()
    for commit in log:
        version = manifest_version(commit)
        # The newest commit carrying a version is that release. An older commit
        # carrying the same version is a rebuild that was later replaced.
        if version and version not in releases:
            releases[version] = commit
    return releases


def slug(title: str) -> str:
    """A change id's title part. It is recorded in DECISIONS, so its form must never change."""
    text = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(text) > 50:
        # Cut at a word boundary rather than mid-word.
        cut = text[:51]
        text = cut[: cut.rfind("-")] if "-" in cut else text[:50]
    return text or "change"


def parse_digest(text: str, version: str) -> tuple[str, list[dict]]:
    """The version a digest describes changes since, and its entries."""
    lines = text.splitlines()
    header = re.match(rf"^# Changes in {re.escape(version)} since (\S+)$", lines[0] if lines else "")
    if not header:
        raise Refused(f"the {DIGEST} of {version} does not start with its header")
    entries = []
    seen: dict[str, int] = {}
    for chunk in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        title, _, body = chunk.partition("\n")
        title = clean_text(title).strip()
        entry = {"title": title, "files": {}}
        for line in body.splitlines():
            for prefix, key in FIELDS.items():
                if line.startswith(prefix):
                    entry[key] = clean_text(line[len(prefix):]).strip()
            match = FILE_LINE.match(line)
            if match:
                if CONTROL.search(match.group(1)):
                    raise Refused(f"the {DIGEST} of {version} names a path with control characters")
                entry["files"][match.group(1)] = match.group(2)
        if not entry["files"]:
            raise Refused(f"the {DIGEST} of {version} has an entry, {title!r}, that lists no files")
        base = f"{version}/{slug(title)}"
        seen[base] = seen.get(base, 0) + 1
        entry["id"] = base if seen[base] == 1 else f"{base}-{seen[base]}"
        entry["release"] = version
        entries.append(entry)
    # THE HEADER'S VERSION IS UPSTREAM TEXT TOO, and it reached an error message
    # unsanitized (security review, round 3). Anything but a release version is
    # refused, which also keeps it out of every later message.
    since = header.group(1)
    if not VERSION.match(since):
        raise Refused(f"the {DIGEST} of {version} names a previous release that is not a version")
    return since, entries


def merged(fork_blob: str, old_blob: str, new_blob: str) -> bytes | None:
    """The three-way merge of a file both sides changed, or None when it conflicts."""
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, blob in (("fork", fork_blob), ("old", old_blob), ("new", new_blob)):
            path = Path(tmp) / name
            path.write_bytes(read_blob(blob))
            paths.append(str(path))
        result = subprocess.run(
            ["git", "merge-file", "-p", *paths], capture_output=True, check=False
        )
    return result.stdout if result.returncode == 0 else None


def classify_file(path: str, old_commit: str, new_commit: str, later: list[str], base: str) -> dict:
    # Case-insensitive, since a checkout on a case-insensitive filesystem
    # writes .BUILDER/ into the same directory (security review, round 3).
    if path.lower().startswith(OWN_DIR):
        return {"path": path, "status": "conflicting",
                "note": f"{OWN_DIR} holds this skill's own record, which a change never touches"}
    new_entry = entry_at(new_commit, path)
    if new_entry and new_entry[0] not in TAKEABLE_MODES:
        return {"path": path, "status": "conflicting",
                "note": f"upstream gives this path mode {new_entry[0]}, which is not a regular "
                        f"file, so it is never taken automatically"}
    fork = blob_at(base, path)
    old = blob_at(old_commit, path)
    new = new_entry[1] if new_entry else None
    # TAKEN MEANS THE FORK IS AT OR PAST THIS CHANGE. Comparing only with this
    # release's copy left a file a later release changed again reading clean or
    # conflicting forever once the fork had taken both (review, round 1).
    if fork == new or any(fork == blob_at(commit, path) for commit in later):
        return {"path": path, "status": "taken"}
    # The mode travels with the content, so a script the change adds or edits
    # keeps its executable bit.
    mode = new_entry[0] if new_entry else None
    if fork == old:
        return {"path": path, "status": "clean", "blob": new, "mode": mode}
    if fork and old and new:
        content = merged(fork, old, new)
        # A merge that leaves the fork's copy as it is means the fork already
        # holds this change, alongside edits of its own. A hand merge that
        # rewrote the conflicting lines does not end here; `merged` records it.
        if content is not None and content == read_blob(fork):
            return {"path": path, "status": "taken", "note": "taken, alongside your own edits"}
        if content is not None:
            return {"path": path, "status": "clean", "content": content, "mode": mode,
                    "note": "your edits and this change merge cleanly"}
    if fork is None:
        why = "you removed this file"
    elif new is None:
        why = "this change removes a file you have edited"
    elif old is None:
        why = "you added a file at the path this change adds"
    else:
        why = "your copy and this change both edit the same lines"
    return {"path": path, "status": "conflicting", "note": why}


def load_decisions() -> dict[str, dict]:
    if DECISIONS.parent.is_symlink() or DECISIONS.is_symlink():
        raise Refused(f"{DECISIONS} or its directory is a symlink; this skill reads and writes only a regular file there")
    if not DECISIONS.exists():
        return {}
    try:
        records = json.loads(DECISIONS.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Refused(f"{DECISIONS} is not readable: {exc}") from exc
    if not isinstance(records, list) or not all(
        isinstance(r, dict) and isinstance(r.get("id"), str) and r.get("decision") in DECISION_KINDS
        for r in records
    ):
        raise Refused(f"{DECISIONS} is not a list of decisions, each with an id and a decision of {' or '.join(DECISION_KINDS)}")
    return {record["id"]: record for record in records}


def survey(ref: str, branch: str) -> tuple[str, list[str], list[dict]]:
    """The fork's base release, the releases after it, and every change they carry, classified.

    THE FORK IS READ FROM `branch`, the branch `apply` builds on. Reading HEAD
    let a report taken on a feature branch describe a different tree from the
    one each change is then committed onto (review, round 1). The decisions
    record is the exception: it is read from the working tree, so a decision
    counts from the moment it is recorded, before it is committed.
    """
    base = fork_base(branch)
    releases = upstream_releases(ref)
    newer = sorted((v for v in releases if version_key(v) > version_key(base)), key=version_key)
    decisions = load_decisions()
    changes = []
    for version in newer:
        blob = blob_at(releases[version], DIGEST)
        if blob is None:
            raise Refused(f"release {version} on {ref} carries no {DIGEST}")
        since, entries = parse_digest(read_blob(blob).decode("utf-8"), version)
        if since not in releases:
            raise Refused(f"{version}'s {DIGEST} describes changes since {since}, which is not on {ref}")
        for entry in entries:
            later = [releases[v] for v in newer if version_key(v) > version_key(version)]
            entry["files_status"] = [
                classify_file(path, releases[since], releases[version], later, branch)
                for path in entry["files"]
            ]
            statuses = {f["status"] for f in entry["files_status"]}
            decision = decisions.get(entry["id"], {}).get("decision")
            if decision == "declined":
                entry["status"] = "declined"
            elif decision == "merged":
                entry["status"] = "taken"
            elif "conflicting" in statuses:
                entry["status"] = "conflicting"
            elif statuses == {"taken"}:
                entry["status"] = "taken"
            else:
                entry["status"] = "clean"
            changes.append(entry)
    return base, newer, changes


def report(args) -> int:
    base, newer, changes = survey(args.upstream, args.base)
    if args.json:
        print(json.dumps({
            "fork_base": base,
            "releases": newer,
            "changes": [
                {
                    "id": c["id"], "release": c["release"], "title": c["title"],
                    "status": c["status"], "what": c.get("what", ""), "why": c.get("why", ""),
                    "diverged": c.get("diverged", ""),
                    "files": [{k: v for k, v in f.items() if k in ("path", "status", "note")}
                              for f in c["files_status"]],
                }
                for c in changes
            ],
        }, indent=2))
        return 0
    if not newer:
        print(f"This fork is at {base}, and {args.upstream} has no newer release.")
        return 0
    print(f"This fork is at {base}. Releases after it on {args.upstream}: {', '.join(newer)}\n")
    for change in changes:
        print(f"{change['status'].upper():<12} {change['id']}")
        print(f"             {change['title']}")
        if change["status"] in ("clean", "conflicting"):
            print(f"             What: {change.get('what', '')}")
            print(f"             Why: {change.get('why', '')}")
            for f in change["files_status"]:
                note = f" ({f['note']})" if "note" in f else ""
                print(f"               {f['status']:<11} {f['path']}{note}")
            if change["status"] == "conflicting":
                print(f"             If your fork has diverged: {change.get('diverged', '')}")
        print()
    return 0


def pick(changes: list[dict], wanted: list[str]) -> list[dict]:
    by_id = {c["id"]: c for c in changes}
    unknown = [w for w in wanted if w not in by_id]
    if unknown:
        raise Refused(f"no such change: {', '.join(unknown)}. Run `{PROG} report` for the ids.")
    return [by_id[w] for w in wanted]


def build_branch(change: dict, base: str) -> str:
    """One commit on a new branch holding this change, built without a working tree."""
    branch = f"upstream/{change['id'].replace('/', '-')}"
    parent = git("rev-parse", f"{base}^{{commit}}").decode().strip()
    with tempfile.TemporaryDirectory() as tmp:
        env = {"GIT_INDEX_FILE": str(Path(tmp) / "index")}
        git("read-tree", parent, env=env)
        for f in change["files_status"]:
            if f["status"] != "clean":
                continue
            blob = f.get("blob")
            if "content" in f:
                blob = git("hash-object", "-w", "--stdin", stdin=f["content"]).decode().strip()
            if blob is None:
                git("update-index", "--force-remove", "--", f["path"], env=env)
            else:
                git("update-index", "--add", "--cacheinfo", f"{f['mode']},{blob},{f['path']}", env=env)
        tree = git("write-tree", env=env).decode().strip()
    message = (
        f"{change['title']}\n\n"
        f"What: {change.get('what', '')}\n"
        f"Why: {change.get('why', '')}\n\n"
        f"Taken from upstream release {change['release']} ({change['id']}).\n"
    )
    commit = git("commit-tree", tree, "-p", parent, stdin=message.encode()).decode().strip()
    # THE ZERO OLD VALUE MAKES THIS CREATE-ONLY: git refuses to move a branch
    # that already exists, so a second apply cannot replace the first one's
    # commit, even one somebody has added to since.
    try:
        git("update-ref", f"refs/heads/{branch}", commit, "0" * 40)
    except Refused as exc:
        if git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", check=False).strip():
            raise Refused(
                f"branch {branch} already exists. If its pull request is open, the change is in "
                f"review; if not, push it and open one, or delete the branch and apply again"
            ) from exc
        raise
    return branch


def github_repo(remote: str) -> str:
    """OWNER/REPO for a GitHub remote, so `gh` opens the pull request on the fork itself."""
    url = git("remote", "get-url", remote).decode().strip()
    match = re.match(r"^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)"
                     r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$", url)
    if not match:
        raise Refused(
            f"--open-prs needs {remote} to be a GitHub repository, and its URL is {url}. "
            f"Leave out --open-prs and open the pull requests by hand."
        )
    return match.group(1)


def apply(args) -> int:
    _, _, changes = survey(args.upstream, args.base)
    # WITHOUT --repo, gh CHOOSES THE REPOSITORY ITSELF, and with an `upstream`
    # remote beside `origin` it can open the pull request on Builder's own
    # repository instead of the fork (review, round 1). Resolved before any
    # branch is made, so a refusal here leaves nothing behind.
    repo = github_repo(args.remote) if args.open_prs else None
    chosen = pick(changes, args.changes)
    blocked = [c["id"] + f" ({c['status']})" for c in chosen if c["status"] != "clean"]
    if blocked:
        raise Refused(
            "only a change that applies cleanly is applied here; these are not: "
            + ", ".join(blocked)
            + ". Merge a conflicting change by hand, using its 'If your fork has diverged' line."
        )
    for change in chosen:
        branch = build_branch(change, args.base)
        print(f"{change['id']}: committed on {branch}")
        if args.open_prs:
            git("push", args.remote, f"refs/heads/{branch}:refs/heads/{branch}")
            body = (
                f"What: {change.get('what', '')}\n\nWhy: {change.get('why', '')}\n\n"
                f"If your fork has diverged: {change.get('diverged', '')}\n\n"
                f"Taken from upstream release {change['release']} ({change['id']}).\n"
            )
            result = subprocess.run(
                ["gh", "pr", "create", "--repo", repo, "--head", branch, "--base", args.base,
                 "--title", change["title"], "--body", body],
                capture_output=True, text=True, check=False,
            )
            if result.returncode != 0:
                raise Refused(f"gh pr create for {branch} failed: {result.stderr.strip()}")
            print(f"{change['id']}: pull request {result.stdout.strip()}")
    return 0


def record(args, decision: str) -> int:
    """Record the operator's decision about each change, replacing an earlier one."""
    _, _, changes = survey(args.upstream, args.base)
    chosen = pick(changes, args.changes)
    records = load_decisions()
    for change in chosen:
        if records.get(change["id"], {}).get("decision") == decision:
            print(f"{change['id']}: already recorded as {decision}")
            continue
        records[change["id"]] = {"id": change["id"], "release": change["release"],
                                 "title": change["title"], "decision": decision}
        print(f"{change['id']}: recorded as {decision}")
    DECISIONS.parent.mkdir(exist_ok=True)
    DECISIONS.write_text(json.dumps(list(records.values()), indent=2) + "\n", encoding="utf-8")
    print(f"\nRecorded in {DECISIONS}. Commit it through your fork's review so the record is kept.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog=PROG, description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("report", "apply", "decline", "merged"):
        p = sub.add_parser(name)
        p.add_argument("--upstream", default="upstream/main", help="the fetched upstream branch")
        p.add_argument("--base", default="main", help="the fork's main branch, which everything is read from and built on")
        if name == "report":
            p.add_argument("--json", action="store_true", help="print the report as JSON")
        else:
            p.add_argument("changes", nargs="+", metavar="CHANGE_ID")
        if name == "apply":
            p.add_argument("--open-prs", action="store_true", help="push each branch and open its pull request")
            p.add_argument("--remote", default="origin", help="the fork's remote to push to")
    args = parser.parse_args(argv)
    if not Path(".git").exists():
        raise Refused(f"run {PROG} from the root of the fork's checkout")
    return {
        "report": report,
        "apply": apply,
        "decline": lambda a: record(a, "declined"),
        "merged": lambda a: record(a, "merged"),
    }[args.command](args)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Refused as exc:
        print(f"{PROG}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
