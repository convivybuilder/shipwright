# Forking Builder

A fork is your own copy of Builder's repositories, which you change as you like and install from with
the same commands as anyone else. Builder does not update a fork. Each release describes what it
changed, and your steward reads that description against your fork so you choose which changes to
take.

Fork Builder when you want to change its code: the installers, the services, the skills. To change
what your agents are told or what they may do, you need no fork; [Customizing
Builder](customizing.md) covers that. You can use Builder fully without ever forking it.

Like [Installing Builder](installing.md), this page describes Builder as it runs now.
**Builder's first published release is 0.6.0**, but every command on this page was run before that
release, on a test machine, against two releases built the same way: `0.9.0` and `0.9.1`. The output
shown is what that machine printed.

## Words this page uses

Forking is done with git, the tool that records every change to a folder of files. This page uses
git's vocabulary throughout.

- **A repository** is a folder whose whole history git keeps. **A commit** is one recorded change
  in it.
- **To clone** a repository is to copy it, history included, onto your machine. The copy is called
  a clone.
- **A fork** is your own copy of someone else's repository, which you are free to change.
  **Upstream** is the original that your fork came from, which here is Builder's own repository.
- **A remote** is a named link from your clone to another copy of the repository. **To fetch** is
  to download that copy's latest commits without changing your own files.
- **A branch** is a separate line of changes inside a repository. **`main`** is the branch that
  holds the current version.
- **A pull request** is a proposed change that is read and approved before it is accepted, and
  accepting it is called merging.
- **A release** is a numbered version of Builder, such as `0.9.1`.
- **The steward** is the first session you meet in Builder, a conversation with Claude that sets up
  your projects. **A skill** is a set of instructions a session loads for a particular job.

## Which repositories to fork

Builder is five repositories: `shipwright`, `agent-platform`, `library`, `convivy-orient` and
`write-better`. There are two good ways to use Builder. Use it as it is, and ask for the features
you want. Or fork all five and build your own system from them: once you change one repository you
are developing Builder, and the changes you want will reach across all five. The install
looks for all five side by side in one folder, meaning five folders next to each other inside one
parent folder, and it does not care which of them are forks.

**Fork `shipwright` from a release.** A release of `shipwright` carries two files at its root that a
clone of its source repository does not: `release.json`, which names the release and the commit of
every repository it was built from, and `CHANGES.md`, which describes each change since the release
before it. Taking upstream changes starts from the `release.json` in your fork, because that file is how the
tools know which release your fork began from.

**The other repositories should match your release.** A release is built and tested with the commits
its `release.json` names, and the install does not compare your clones with them. On the test machine, a `shipwright` from an older release installed
beside a newer `library` stopped at the background-jobs step with `init_vectors: LIBRARY_VECTORS_DB is
not set`, because the newer Library needs a setting the older job declaration did not give it.

## Install from your forks

Clone each fork, and each repository you did not fork, into one folder. In the commands below,
replace each `<...>` with that repository's address, and note that `~/src` is a folder named `src`
in your home folder. This example forks two repositories and takes the other three from Builder:

```
mkdir -p ~/src && cd ~/src
git clone <your fork of shipwright> shipwright
git clone <your fork of agent-platform> agent-platform
git clone <Builder's library> library
git clone <Builder's convivy-orient> convivy-orient
git clone <Builder's write-better> write-better
```

Then install as [Installing Builder](installing.md) says for your machine and account, with
its commands as written. On the
test machine, the forks of `shipwright` and `agent-platform` each carried one commit of their own, the
install ended with `every step reported success (5 of 5 ran)`, and both forks' commits were what it
placed.

**Push a change to your fork before you install it.** The install takes each repository from its
`stable` branch when your clone has one, and from `main` when it does not: `install-payload` reads
the local branch, and the backend reads `origin/stable` or `origin/main`, as your clone last fetched
it. A fork GitHub makes with its default settings copies only `main`, so it installs from `main`. If
your fork also has a `stable` branch, the install takes that one, so push your change there. A
change that exists only in your working files, or only on another branch, is not
installed.

## How upstream changes reach a fork

Builder publishes a description of each change, called the change digest, and you decide what to
do with each one. Taking upstream changes pushes nothing into your fork unless you ask it to, and
then only the branch of a change you chose to take, as [opening pull
requests](#take-a-clean-change) below describes.

The digest is the file `CHANGES.md`. Each release's `CHANGES.md` has an entry for every change since the release before it. An entry
looks like this:

```
## The glossary says where each entry leads
What: the glossary's opening says that each entry names where to read more.
Why: a reader arriving at one entry did not know the entries link onward.
If your fork has diverged: take the one sentence into your own opening.
Files:
- `payload/docs/glossary.md` changed
```

Every file the release changed is listed in exactly one entry. The last line of prose says what to
check if your fork has changed the same files.

**The digest covers `shipwright` only.** The other repositories have no public release yet, so
nothing yet describes their changes for a fork. `release.json` still names the commit of each one a
release was built from.

## Taking upstream changes

Taking changes has three stages: you connect your clone to Builder's repository, you ask what has
changed, and you answer for each change.

Add Builder's `shipwright` as a remote of your fork's clone, once. The first line below moves into
your clone, the second names Builder's repository `upstream`, and the third downloads its latest
commits:

```
cd ~/src/shipwright
git remote add upstream <Builder's shipwright>
git fetch upstream
```

Then ask the steward what has changed upstream, in plain language. It uses the `take-upstream`
skill, which the install
put in `~/.claude/skills`. On the test machine, the steward was asked *"My fork of Builder is checked
out at ~/src/shipwright, with Builder as the upstream remote. What has changed upstream?"* and
answered that the fork was on `0.9.0`, that `0.9.1` held three changes, that two were clean and one
conflicted with the fork's own edit, and asked which to take, decline or leave for later.

The report marks each change with one of four words:

- **CLEAN**: it can be taken as it is. A file your fork also edited counts as clean when the two sets
  of edits touch different lines.
- **CONFLICTING**: your fork and the change edit the same lines. Someone merges it by hand.
- **TAKEN**: your fork already holds it.
- **DECLINED**: you declined it before.

**Nothing is taken until you choose it.** A change you leave unchosen is offered again next time.

The steward runs one command for each step, and you can run them yourself. They are shown here from
`~/src/shipwright`, with the test machine's output.

### See what has changed

```
python3 ~/.claude/skills/take-upstream/upstream.py report
```

```
This fork is at 0.9.0. Releases after it on upstream/main: 0.9.1

CONFLICTING  0.9.1/installing-on-a-mac-starts-with-two-settings
...
CLEAN        0.9.1/the-glossary-says-where-each-entry-leads
...
CLEAN        0.9.1/what-you-need-grows-with-you
```

The report prints each change's What and Why, and for a conflicting change its "If your fork has
diverged" line.

### Take a clean change

```
python3 ~/.claude/skills/take-upstream/upstream.py apply 0.9.1/the-glossary-says-where-each-entry-leads
```

It makes one branch per change, `upstream/0.9.1-the-glossary-says-where-each-entry-leads` here,
built from `main` with one commit carrying the change's What and Why. Your working tree, which is the
files as they sit in your folder, and your current branch are left as they were. Add `--open-prs`
when your fork is on GitHub and `gh`, GitHub's command-line program, is signed in, and
each branch is pushed and gets a pull request of its own, so every change goes through your fork's
review. Without it, merge the branch the way your fork takes any change.

### Merge a conflicting change by hand

A conflicting change is one where Builder and you edited the same lines, so no tool can know which
wording you want. A change is also marked conflicting when Builder gives a path as anything but a
regular or executable file, or when it touches the fork's `.builder/` folder, which holds this
tool's own record. `apply` refuses a conflicting change, answering `only a change that applies
cleanly is applied here`. Read upstream's version of the file with `git show upstream/main:<path>`,
and combine it with your edit on a branch of its own. That branch goes through your fork's review
like any other change, as a pull request where your fork has them. This is the one path where
upstream's lines and yours are mixed by hand, so it most needs a second reader. Record that you
merged it, and commit the record on the same branch:

```
python3 ~/.claude/skills/take-upstream/upstream.py merged 0.9.1/installing-on-a-mac-starts-with-two-settings
```

Without the record, a merge that keeps your edit on the lines that conflicted still compares as a
conflict, and the change is offered again.

### Decline a change

Declining records that you do not want a change, so the report marks it DECLINED from then on:

```
python3 ~/.claude/skills/take-upstream/upstream.py decline 0.9.1/what-you-need-grows-with-you
```

`decline` and `merged` both write to `.builder/upstream-decisions.json` in your fork. **Commit that
file through your fork's review.** Until it is on `main`, only this clone knows the decision.

### After

With the branch merged and the record committed, the same report reads:

```
TAKEN        0.9.1/installing-on-a-mac-starts-with-two-settings
TAKEN        0.9.1/the-glossary-says-where-each-entry-leads
DECLINED     0.9.1/what-you-need-grows-with-you
```

It still says `This fork is at 0.9.0`, because your `release.json` names the release you forked
from, and every later release is read against it. Run `install-payload` again to install what you
merged: on the test machine it answered `installed main at <commit>`, naming the merge.

## Publishing your own fork

`bin/publish-payload` and `bin/publish-engine` build the public tree a release ships from, and they
come with your fork, since they live under `bin/`, which installs the same way everywhere. Each one
scans everything about to ship when you build and publish a release of your own fork, so that
nobody's name, machine or private detail leaves by accident.

A page you wrote yourself, under your own name, can mark itself exempt from that scan. Make the
first line of a markdown page exactly:

```
<!-- authorship: human -->
```

The published site then shows that page with a Human badge instead of the usual one, and the scan
never refuses it. The mark has to sit on the first line; on any later line it is ordinary text, and
the page keeps the usual badge and the usual scan.

The scan still runs on a marked page, and still reports what it finds — it just never refuses the
build over it. Each finding is printed as a notice naming the place and the category, never the
matched text, the same way a private name or a machine name is withheld everywhere else in this
tree. That is a safeguard against two mistakes rather than against you: an agent marking its own
text as human-written, and a page that was clean when you signed it but has since picked up
something that should not ship. Read the notices before you publish.

Each tool reads the mark from the page itself, since both ship and each has to tell on its own which
pages are yours. Marking a page you did not write changes its badge on the published site, a visible
claim for whoever reviews the change before it goes out.

## When something goes wrong

Each heading below is a message one of these commands can print, followed by what caused it and what to do.

### `main has no readable release.json`

The report was run somewhere that is not a fork of a `shipwright` release: another repository, or a
clone of `shipwright`'s source repository. Run it from the root of your `shipwright` fork.

### `upstream/main names no commit`

The clone has no `upstream` remote, or it has not been fetched. Add and fetch it as shown above. If
your remote for Builder has another name, pass `--upstream <remote>/main` to every command.

### `branch upstream/0.9.1-… already exists`

That change was applied before. If its branch has a pull request, the change is in review. If not,
push the branch and open one, or delete the branch and apply again.
