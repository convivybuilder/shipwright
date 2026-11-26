# One account vs. multiple accounts on the server

Builder installs in one of three shapes on the machine that runs your sessions, and you name the
shape when you install. A shape's name counts every account on that machine, your own included. The
shape decides which user account on that machine Builder runs as, and that decides what an agent can
reach. A session is a conversation with Claude, an AI model, in a terminal, and an agent is a model a
session puts to work on a task. How many machines you install Builder on is a separate choice, which
[How many machines Builder runs on](where-everything-runs.md) covers.

The install never moves you from one shape to another by itself: when the three-account install
cannot complete, it stops and says what it lacked. This release installs the single-account and
two-account shapes; the three-account install comes in a later release.

## The single-account install

Some machines give you no administrator password, such as a work computer on which you cannot create
accounts. There Builder runs as your own account. The install creates no account and asks for no
password, and Builder's background jobs run as you. There is no `reviewers` account and no approver,
which is the identity that signs review checks on the three-account install. This shape can also
start without a GitHub account, for work that is not software, and adding GitHub later turns on
reviews without a reinstall.

**It gives up the boundary the three-account install draws.** Every session can read everything your
account holds. The reviewers still run and post their findings on each pull request, and the rule
on `main`, the project's current version, that you set on GitHub can require a pull request and the
repository's own automated checks. The reviewers' findings are not among those checks.

**That includes the credentials that can act as a person.** Orient's server holds a credential that
lets it do what Builder reserves for a person, such as approving an epic, and on this shape that
file sits in your account. An agent dispatched for one task runs in a sandbox that denies it the
folder holding that file. A session runs outside that sandbox, so it could read the file, and what
stops it using the credential is the instructions it follows, which is a convention. Nothing in the
operating system separates an agent from you on this shape.

**What GitHub can still enforce depends on the identity your agents use there.** Connect GitHub as
[Connecting GitHub](connecting-github.md) describes, and the agents act as a GitHub App you create
while your own login stays off the machine. In the merge mode called Deterministic, GitHub lets
only you merge into `main` and refuses the App's merge, so you merge each pull request by hand on
github.com from another device; [Connecting GitHub](connecting-github.md#the-two-merge-modes)
describes it. In Instruction only, or with your own GitHub login still on the machine, nothing on GitHub
enforces that a person merges: an agent acting as your account could approve or merge a change
itself. What holds the line then is the machine-wide
instruction every session reads, `~/.claude/CLAUDE.md`, that an agent merges only what your agent
policy permits. The install places that file only when you have none, so if you had one already, add
the Merging section and the Library section from Builder's version to it; the install prints that
version's path when it leaves yours alone. The rest is you pressing merge after reading the change
and the reviewers' findings. The Library section tells an agent never to hand-build a branch or pull
request for a path under `projects/` in your knowledge repository, and it carries the rules for work
items and for a missing tool as well.

**If you can get administrator rights, the two-account install separates `agents` from your own
account; the three-account install, which also keeps review separate, comes later.** You install
the single-account shape whether or not you have the administrator password.
[Installing Builder](installing.md#which-install-is-yours) says which route fits your machine. On
Debian or Ubuntu with an account that can use `sudo`, that route's first command runs Builder's
checked-out code as root, once, and [Before you start](installing.md#before-you-start) says so
before you run it.

## The two-account install

Builder runs as one account of its own, `agents`, separate from yours, and that account also runs
the agents that review a change. There is no separate `reviewers` account and no approver, so a
review is one more thing `agents` does rather than something only another account can sign: the
boundary the three-account install draws between writing a change and reviewing it does not exist
here. A root-owned half of Builder under `/opt/builder` holds the code `agents` runs, and the
install pins that half to the commits the signed release names.

The install also creates a third account with no login of its own for the Library, the service
every session reaches for its knowledge base and its work queue — `_library` on a Mac, `library` on
a Linux machine. That account owns the Library's database, its credentials and its state; `agents`
reaches it only over its own network listener, never by reading its files directly. A no-login
account does not count toward the shape's name, so this is still called the two-account install.
Add `--shape two` to the install command, the way [Installing
Builder](installing.md#which-install-is-yours) adds `--shape three` for the three-account install.

**The catch is that one account both writes a change and reviews it.** You still merge every pull
request in every project repository, until you add your agents' GitHub App to a repository's merge
ruleset bypass list. The documentation says this beside the shape's description. Because a coder
can steer a review, this shape's review findings are called advice, in those words: the same
account writes the code and runs the review, so a coder can change what the reviewer sees. The
Library's own App merges a knowledge pull request the same way, once its review passes, and that
review also runs as `agents` on this shape, so it is steerable advice too; removing the Library's
App from the merge ruleset's bypass list returns every knowledge merge to you.

**The merge rule this shape relies on is not in this release.** It needs two rulesets on `main`,
one that refuses every update except a pull request you merge, and the command that would print and
check them, `github-gate --shape two`, is not built; `github-gate --shape` offers only `three` and
`single` today. Until it ships, merge each pull request yourself from another device, through
GitHub's own web page, rather than from a command this install prints. [What does not work
yet](install-status.md) says more.

## The three-account install

Builder runs under accounts of its own, separate from yours. The install creates two accounts that
count toward this shape on each machine that runs it, with the administrator password, and leaves
your own account to you.

- **`agents` runs everything Builder does**: the steward, which is the first session you meet,
  every crew's session, the agents they put to work, Orient and the background jobs other than the
  Library's own. A crew is one project and everything working on it, and Orient is the view of the
  whole system. Builder's folder, `~/builder`, is in this account. The account holds none of your
  credentials and has no administrator rights.
- **`reviewers` runs the agents that review a change.** `agents` can ask for a review and cannot
  sign one. One rule lets it start a single program that the administrator account owns, and that
  program fixes which pull request and commit are reviewed, runs the reviewer as `reviewers`, and
  posts the verdict to GitHub itself. A pull request is a proposed change waiting to be accepted,
  and a commit is one recorded version of it.

The install creates a third account too, for the Library, the service every session reaches for its
knowledge base and its work queue, with no login of its own: `_library` on a Mac, the platform's own
naming convention for an account like this one, and `library` on a Linux machine, where no such
convention applies. That account owns the Library's database, its credentials and its state
directory; neither `agents` nor `reviewers` reaches any of that directly, only over the Library's own
network listener. A no-login account does not count toward the shape's name, so this is still called
the three-account install.

You reach your sessions over SSH as `agents`, which is what Deck, the desktop application where you
pilot each project, does for you. SSH is a standard way to open a terminal as another account or on
another machine. You read what the sessions wrote through your membership of each account's group,
without `sudo`, the command that borrows administrator rights. Neither `agents` nor `reviewers` can
read the other's folder, your folder, or the Library's.

**This is what keeps a merge yours to decide.** To merge a change is to accept it into the project.
An agent that can edit Builder's code can change what the other agents run, since they all run as
`agents`. It cannot make a change merge on its own say, because GitHub accepts only review checks
signed with a key that only the administrator account and the review program can read, and the only
way to get one is for the review program to run. The exceptions are the kinds of merge your agent
policy hands to agents, which still need a passed review. A review check is a reviewer's pass or
fail verdict, posted on the pull request.

**An update never overwrites a background job's unit file you edited by hand.** It replaces one
only when it matches what an earlier update of Builder itself wrote there; a job's unit written
before that update, or ever hand-edited, is instead left as it is, and every update names it as
skipped. To take Builder's version, remove that unit file and run the update again.

## Where to go next

- **[How many machines Builder runs on](where-everything-runs.md)** covers putting Builder on one
  machine or several, and what a second machine buys you.
- **[Connecting GitHub](connecting-github.md)** sets up the GitHub App your agents act as.
- **[Installing Builder](installing.md)** walks through the install.
- **[The glossary](glossary.md)** explains each word Builder uses.
