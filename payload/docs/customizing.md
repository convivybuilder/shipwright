# Customizing Builder

Builder's agents work from documents you own: what each agent is told, the rules composed into every
crew's instructions, which documents a crew starts with, and what agents may do without you. This
page names each of those documents, says what it controls, and walks through one change to each.

Like [Installing Builder today](installing.md), this page describes Builder as it runs now, on a
machine installed from that page. Every change on it was made on a test machine, and the result
shown is what that machine did.

You do not need to be a programmer to make these changes. Each one is a line or two of plain English
added to a text file, followed by a few typed commands that this page gives you and explains.

## Words this page uses

- **An agent** is an AI model given a named role, such as a reviewer, and the tools that role may
  use. What an agent is told is an ordinary document.
- **A crew** is one project and everything working on it. **A session** is a conversation with
  Claude in a terminal, and each crew has one that runs its work. **The steward** is the first
  session you meet, which creates crews.
- **Your knowledge repository** is the folder that holds the Reference Room, Builder's store of
  what your projects hold to be true, which many systems call a knowledge base. It is a git
  repository, meaning the tool git records every change to it.
- **To commit** is to record a change in git. **To push** is to send your commits to the
  repository's shared copy, which git calls its remote and names `origin`. **`main`** is the
  repository's current version, so `origin/main` is the current version of the shared copy.
- **A pull request** is a proposed change that is read and approved before it is accepted.
- **To individuate** a crew is to individuate its agents: each one gets a clean place to work, the
  documents its role needs and only the powers its role allows. A crew picks up a changed document
  when you individuate it again.
- **The operator** is Builder's word for you.

## What you can change

Builder installs a starter set of documents into your knowledge repository, `~/builder/knowledge`.
In a path, `~` stands for your home folder. The starter set holds three kinds of document besides
the agents themselves. An instruction block is a set of rules composed into an agent's instructions.
A profile is a crew's list of the documents each of its roles should read. The agent policy says
what agents may do without you. To dispatch an agent is to send it off to do one task.

| path | what it controls |
|---|---|
| `projects/platform/agents/planning-orchestrator.md` | the crew's own session, which `co` starts: how it chooses work, what it does itself and what it hands to other agents |
| `projects/platform/agents/coder.md` | the agent a crew dispatches to make one change and hand it back committed |
| `projects/platform/agents/reviewer.md` | the agent that reviews a pull request and posts a verdict |
| `projects/platform/agents/security-reviewer.md` | the agent that reviews a pull request for security risks |
| `projects/platform/instruction-blocks/working-with-the-operator.md` | how a crew's session works with you, composed into every crew's instructions |
| `projects/platform/instruction-blocks/open-a-pull-request.md` | how a crew's session opens a pull request and runs its review, composed into every crew's instructions |
| `projects/platform/instruction-blocks/review-a-pull-request.md` | how a dispatched reviewer does its work |
| `projects/platform/profiles/default.yaml` | which documents a crew starts with, when it has no profile of its own |
| `projects/platform/policy/agent-policy.yaml` | what agents may merge, how many review rounds run before you decide, and how many agents run at once |

Two more files sit outside the knowledge repository, and you edit them where they are:

| path | what it controls |
|---|---|
| `~/.claude/CLAUDE.md` | the rules every Claude Code session on the machine reads |
| `~/builder/steward/CLAUDE.md` | the steward's charter, which is its instructions |

## How a change reaches the agents

Every change in the knowledge repository takes the same three moves. You edit the file, you send
the edit to the repository with git, and you let each crew pick it up. This section explains why
it works that way and gives the commands.

**You change the knowledge repository's files with git.** A session's knowledge tool for writing to
the Reference Room directly, `kb_update`, refuses these paths. It answers `refused —
projects/platform/agents/reviewer.md is a roster path, which takes the PR path under every
provenance`, because a bad commit to one of them changes what every agent does. The route it offers
is `kb_propose`, which opens a pull request for you to merge, and it answers `refused — the
knowledge repo's origin is not GitHub, and kb propose needs GitHub connected` on a machine whose
knowledge repository has no GitHub remote. The install gives it none: its remote is
`~/builder/.remotes/knowledge.git`, on the same machine. So on a fresh install, git is the way to
make these changes.

**Read what you are about to push.** The pull request these tools ask for is a review, and pushing
to `main` skips it, so a mistake in an agent, an instruction block, a profile or the policy reaches
every crew without anyone else reading it. Nothing on the local remote checks a push, so your own
reading is the only review it gets. `git diff origin/main` shows exactly what the push will send.
The install's update of the starter set lands the same way, as a commit on `main`.

**A crew's session can make the same push.** It runs as the same account, in a mode where it runs
commands without asking you first, so on a fresh install the only thing that keeps it from pushing
to the policy or an agent's instructions is the instruction every agent carries. The policy file
says it is changed through a pull request you merge, and that becomes true once your knowledge
repository is connected to GitHub. Until then, read every change to these files now and then with
`git log -p origin/main -- projects/platform/`. A crew's commits carry your name, because the
session commits as you, so read what each change does rather than who made it.

So each change below follows the same steps. First go to the knowledge repository and ask git what
has changed there:

```
cd ~/builder/knowledge
git status
```

**Start from a clean `git status`.** A clean status is one where git reports nothing waiting to be
committed. A file something else left staged goes into your commit with
`git commit -a`, which is how one of the test machine's commits picked up a stray document. Commit
only the files you changed:

```
git commit -m "<what you changed>" -- <the files you changed>
git diff origin/main
git push origin main
agentctl kb sync
```

Those four lines do four things. `git commit` records your change, with a short message saying what
it was. `git diff origin/main` shows you, line by line, what you are about to send. `git push origin
main` sends it. `agentctl kb sync` brings your working copy and the search index up to date with
what you pushed.

You will know it worked when `agentctl kb sync` answers `up to date at <commit>, verified — N docs
indexed`, naming the commit you just pushed. A git identity is the name and email address git
writes on each commit. If your account has no git identity, `git commit` refuses. Set one with `git config
--global user.name` and `user.email`, or pass `-c user.name=… -c user.email=…` to that one commit.

**What makes the change take effect depends on the file.**

- **An agent, an instruction block or a profile** reaches a crew when the crew individuates again.
  Until then the crew keeps the copies it was given. On the test machine, the one crew individuated
  after a change to `reviewer.md` had the new line, and the crew that was not had the old file.
- **The agent policy** takes effect when you push. The tools that enforce it read the file at
  `origin/main` of your knowledge repository, every time. On the test machine the concurrency limit,
  which is how many agents may run at once, still read `max_concurrent=16` after the commit and read `12` after `git push`.

To individuate a crew again, leave its session first, because `knowledge-ctx` refuses to write into
a directory a Claude session is running in (`live Claude Code processes detected in target —
aborting`). Each crew's session runs inside tmux, a program that keeps terminal sessions running in
the background. Attach to the crew's session with `tmux attach -t <crew>`, putting the crew's name
in place of `<crew>`, and type `/exit`. Claude closes, and you are left at an ordinary command
prompt, which is called a shell, in the crew's folder. Run both commands there, because
`knowledge-ctx use` rewrites the `.claude/` folder of whichever folder it runs in, clearing its
agents and skills first:

```
cd ~/builder/<crew>
knowledge-ctx use default --force
co
```

The first line individuates the crew from its profile, and `co` starts the crew's session again.

Use `daytime` in place of `default` when the crew has a profile of its own, as in [a profile for one
crew](#a-profile-for-one-crew) below. `knowledge-ctx list`, run in the crew's folder, names the
profiles it can use.

## One change to each

Each part below makes one small, harmless change to one document, so you can see the whole route
work before you make a change you care about. The example lines are only examples, and you can put
any instruction of your own in their place.

### The crew orchestrator

The crew orchestrator is a crew's own session, the one the `co` command starts. It chooses the work,
does some of it itself and hands the rest to other agents. Its instructions are in
`projects/platform/agents/planning-orchestrator.md`, a file that still carries the name planning
orchestrator.

Add a line to the end of that file:

```
Before starting anything you expect to take more than an hour, say what it is and wait for me.
```

Push it with the steps above, then individuate each crew that should work this way. Every crew's session starts from this
file, so the line reaches every crew you individuate again.

### The coder, the reviewer and the security reviewer

The test machine appended this line to `projects/platform/agents/reviewer.md`:

```
Keep each review under 400 words.
```

After the push, `knowledge-ctx use default --force` in one crew's folder wrote a
`.claude/agents/reviewer.md` ending in that line. The coder and the security reviewer change the same
way, in `coder.md` and `security-reviewer.md`. An agent's frontmatter, the block between the `---`
lines, is what the Library indexes it by: change its body, and leave `id`, `kind` and `audience` as
they are.

### The instruction blocks

An instruction block holds rules that Builder composes into instructions elsewhere, so one edit
reaches every crew or reviewer that receives the block.

The test machine appended this line to
`projects/platform/instruction-blocks/working-with-the-operator.md`:

```
When the operator asks for a summary, keep it to five lines.
```

After the push, individuating a crew wrote it into that crew's `.claude/CLAUDE.md`. The line reached
the index before `agentctl kb sync` ran, since a background service indexes each commit; the sync
confirms it. `open-a-pull-request.md` changes the same way. `review-a-pull-request.md` is for the
reviewers a crew dispatches.

### The default profile

`projects/platform/profiles/default.yaml` lists the documents a crew starts with when it has no
profile of its own: the four agents, and every current skill, decision and runbook under `platform`.
To give every such crew the decisions you record under another project, add a rule to its `include`
list:

```yaml
  - kind: decision
    project: [<your project>]
    status: current
```

That rule reads as "include every current decision in this project". Put your project's name in
place of `<your project>`.

### A profile for one crew

To give one crew a different set of starting documents, copy the default into that crew's project,
named `daytime.yaml`, and change its first line to name it. For a crew called `garden`, run these
in the knowledge repository. The first line makes a folder for the crew's profiles and the second
copies the default profile into it:

```
mkdir -p projects/garden/profiles
cp projects/platform/profiles/default.yaml projects/garden/profiles/daytime.yaml
```

Change the first line of the copy to `profile: garden/daytime`, and add rules for the crew's own
documents. The test machine added the crew's bead:

```yaml
  - kind: bead
    project: [garden]
```

After the push, `knowledge-ctx list` in the crew's folder printed:

```
profiles for garden:
  daytime
```

Then `knowledge-ctx use daytime --force` printed `profile: garden/daytime`.

**Name the copy `daytime.yaml`.** On the test machine a copy named
`projects/garden/profiles/default.yaml` was ignored: `knowledge-ctx use default` answered `project
garden has no profiles; using platform/default`, and `agentctl crew doctor garden` reported the
crew's agents as coming from the wrong profile.

### The agent policy

The agent policy is where you decide what agents may do without asking you. Out of the box, it names
nothing they may merge. `agentctl kb merge`, the command the Library merges through, reads the
policy and refuses anything it does not permit. A merge you start from Deck or Orient takes a
separate path, through a merge check in the Library, and that check approves every merge it is asked
about for now, as [Installing Builder](installing.md) says.

`projects/platform/policy/agent-policy.yaml` holds its own rules in its comments. Each setting is a
line of exactly `key: value`, and a file that breaks any rule is read as the defaults it names, with
no agent merging anything.

To let agents merge a reviewed change to your Reference Room, change:

```
agents_may_merge_knowledge: false
```

to:

```
agents_may_merge_knowledge: true
```

This covers a pull request the Library opened through `kb_propose` in which every file is a document
under `projects/` and none is an instruction. Once its review has passed, `agentctl kb merge` reads
this setting and merges it. It still refuses a pull request whose review has not passed on its
current commit, that ran more review rounds than the policy allows, or that has a commit the
Library's tools did not write. `agents_may_merge_knowledge_instructions` is the same for a proposal
that changes an instruction, such as an agent or a profile. Turning it on lets an agent merge a
change to what agents are told to do, including the instructions of the reviewers who check that
agent's work, so one change that passed review can alter the review the next change has to pass, and
the review that gates it is an agent's, with no person reading the change. Every pull request
outside these settings and `agents_may_merge_documents`, below, is still yours to merge, and no
agent ever merges a change to `projects/platform/policy/`. `kb_propose` needs GitHub, so these
settings have nothing to act on until your knowledge repository is connected to it.

`agents_may_merge_documents` covers a pull request in which every file sits in its repository's
top-level `docs/` folder, has no front matter and is not an instruction, in a repository you list in
`docs-merge-app.json`, the configuration file of the GitHub App that merges documents. Once its
review has passed, `agentctl docs merge` reads this setting and merges it, whoever opened the pull
request. It refuses one opened from a fork.

The same file sets how many agents run at once. The test machine changed `max_concurrent: 16` to
`max_concurrent: 12`. After the push, the dispatcher, the program that starts agents, read the new
value. Its reading of the policy, which `agentctl spawn` prints on every dispatch, was `concurrency limits from the policy file at origin/main of
…/builder/knowledge: max_concurrent=12`.

### The rules every session reads

`~/.claude/CLAUDE.md` holds the rules for checking work before reporting it, and its Merging section
holds the rule that an agent merges only what your agent policy permits. On the single-account
install nothing else enforces that rule, so keep the section when you edit the file. Every Claude
Code session on the machine reads it, the steward and every crew included. Edit it in place; a
session started after the edit reads the new version. The test machine appended:

```
Prefer short commit messages.
```

Running the install again left the edited file alone, saying `untouched: it differs from the
machine-wide instruction file shipped at <commit> … and an existing one is never overwritten`.

### The steward's charter

`~/builder/steward/CLAUDE.md` is the steward's instructions: what it owns, how it creates a crew and
how it routes work between crews. Edit it in place, then start a new steward session. The test
machine appended:

```
Always answer in British English.
```

Running the install again left it alone, saying `untouched: it differs from the charter shipped at
<commit> … and an installed charter is never overwritten`.

## When you install a newer release

Builder's starter set improves from one release to the next, and you will have edited some of it by
then. This section explains how an update keeps your edits.

Running `install-payload`, the installer command that places the steward and the starter set, from a
newer release brings the starter set in your knowledge repository up
to that release, one document at a time. It compares each document with the version Builder last
shipped there:

- **A document you never changed** is replaced with the new release's version. That includes the
  agent policy, so before each update run `install-payload --dry-run` to see whether the policy
  would change, and read the new release's version,
  `payload/knowledge-seed/projects/platform/policy/agent-policy.yaml` in your `shipwright` clone,
  before you run the update.
- **A document the new release is the first to ship** is added.
- **A document you edited, deleted or wrote before Builder shipped one** is left exactly as you have
  it. Builder's new version goes to `~/builder/steward/builder-updates/`, at the same path, with a
  `.diff` of what Builder changed, which is a line-by-line listing, and a `README.md` naming the
  release.

A test container installed one release, appended a line to `reviewer.md` and pushed it, then
installed a release that changed both `coder.md` and `reviewer.md`. The install said, for the two:

```
replaced projects/platform/agents/coder.md, which was as Builder shipped it, with this release's version
left projects/platform/agents/reviewer.md, which differs from what Builder shipped, and handed this release's version to the steward at …/builder/steward/builder-updates/projects/platform/agents/reviewer.md
```

It makes one commit, `The starter set, updated to Builder <commit>`, and makes it in the knowledge
repository's remote. Your working copy and the index catch up at the next `agentctl kb sync`, which
a background service runs every ten minutes; run it yourself to see the change at once.
`install-payload --dry-run` lists what each document would get and changes nothing.

**Ask the steward about anything in `builder-updates/`.** For each document it offers to replace
yours with Builder's, keep yours, or merge the two, and it writes your choice with the steps
[above](#how-a-change-reaches-the-agents). A document you keep is offered again at the next update,
because it still differs from the version Builder last shipped. The folder is replaced on every
install, and removed once nothing in it is left to offer.

This happens only when the knowledge repository's remote is on the same machine, as the install
creates it. A knowledge repository connected to a hosted remote, such as one on GitHub, is left
alone, since a push to its
`main` from the install would go around that host's review.
