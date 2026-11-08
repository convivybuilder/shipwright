# One account vs. multiple accounts on the server

Builder installs in one of three shapes on the machine that runs your sessions, and you name the
shape when you install. A shape's name counts every account on that machine, your own included. The
shape decides which user account on that machine Builder runs as, and that decides what an agent can
reach. A session is a conversation with Claude, an AI model, in a terminal, and an agent is a model a
session puts to work on a task. How many machines you install Builder on is a separate choice, which
[How many machines Builder runs on](where-everything-runs.md) covers.

The install never moves you from one shape to another by itself: when the three-account install
cannot complete, it stops and says what it lacked. This release installs only the single-account
shape; the two-account install is not built yet, and the three-account install comes in a later
release.

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

**If you can get administrator rights, use the three-account install once it is built.** Today the
single-account install is the only shape built, and you install it whether or not you have the
administrator password. [Installing Builder](installing.md#which-install-is-yours)
says which route fits your machine. On Debian or Ubuntu with an account that can use `sudo`, that
route's first command runs Builder's checked-out code as root, once, and [Before you
start](installing.md#before-you-start) says so before you run it.

## The two-account install

Builder runs as one account of its own, `agents`, separate from yours, and that account also runs
the agents that review a change. There is no separate `reviewers` account and no approver, so a
review is one more thing `agents` does rather than something only another account can sign: the
boundary the three-account install draws between writing a change and reviewing it does not exist
here.

**This shape is not built yet.** [What works and what does not yet](install-status.md) tracks what
is.

## The three-account install

Builder runs under accounts of its own, separate from yours. The install creates two accounts on
each machine that runs it, with the administrator password, and leaves your own account to you.

- **`agents` runs everything Builder does**: the steward, which is the first session you meet,
  every crew's session, the agents they put to work, the Library, Orient and the background jobs. A
  crew is one project and everything working on it. The Library is where Builder keeps everything a
  project knows, and Orient is the view of the whole system. Builder's folder, `~/builder`, is in
  this account. The account holds none of your credentials and has no administrator rights.
- **`reviewers` runs the agents that review a change.** `agents` can ask for a review and cannot
  sign one. One rule lets it start a single program that the administrator account owns, and that
  program fixes which pull request and commit are reviewed, runs the reviewer as `reviewers`, and
  posts the verdict to GitHub itself. A pull request is a proposed change waiting to be accepted,
  and a commit is one recorded version of it.

You reach your sessions over SSH as `agents`, which is what Deck, the desktop application where you
pilot each project, does for you. SSH is a standard way to open a terminal as another account or on
another machine. You read what the sessions wrote through your membership of each account's group,
without `sudo`, the command that borrows administrator rights. Neither account can read the other's
folder, and neither can read yours.

**This is what keeps a merge yours to decide.** To merge a change is to accept it into the project.
An agent that can edit Builder's code can change what the other agents run, since they all run as
`agents`. It cannot make a change merge on its own say, because GitHub accepts only review checks
signed with a key that only the administrator account and the review program can read, and the only
way to get one is for the review program to run. The exceptions are the kinds of merge your agent
policy hands to agents, which still need a passed review. A review check is a reviewer's pass or
fail verdict, posted on the pull request.

## Where to go next

- **[How many machines Builder runs on](where-everything-runs.md)** covers putting Builder on one
  machine or several, and what a second machine buys you.
- **[Connecting GitHub](connecting-github.md)** sets up the GitHub App your agents act as.
- **[Installing Builder](installing.md)** walks through the install.
- **[The glossary](glossary.md)** explains each word Builder uses.
