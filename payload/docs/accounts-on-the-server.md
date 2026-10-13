# One account vs. multiple accounts on the server

Builder installs in one of two shapes on the machine that runs your sessions, and you name the shape
when you install. The shape decides which user account on that machine Builder runs as, and that
decides what an agent can reach. A session is a conversation with Claude, an AI model, in a terminal,
and an agent is a model a session puts to work on a task. How many machines you install Builder on is
a separate choice, which [How many machines Builder runs on](where-everything-runs.md) covers.

The install never moves you from one shape to the other by itself: when the two-account install
cannot complete, it stops and says what it lacked. This release installs only the single-account
shape; the two-account install comes in a later release.

## The two-account install

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

## The single-account install

Some machines give you no administrator password, such as a work computer on which you cannot create
accounts. There Builder runs as your own account. The install creates no account and asks for no
password, and Builder's background jobs run as you. There is no `reviewers` account and no approver,
which is the identity that signs review checks on the two-account install. This shape can also start
without a GitHub account, for work that is not software, and adding GitHub later turns on reviews
without a reinstall.

**It gives up the boundary the two-account install draws.** Every session can read everything your
account holds. The reviewers still run and post their findings on each pull request, and the rule
on `main`, the project's current version, that you set on GitHub can require a pull request and the
repository's own automated checks. The reviewers' findings are not among those checks.

**What GitHub can still enforce depends on the identity your agents use there.** Connect GitHub as
[Connecting GitHub](connecting-github.md) describes, and the agents act as a GitHub App you create
while your own login stays off the machine. In the merge mode called Enforced, the rule on `main`
then requires your approval on a pull request an agent opened, which the App cannot give, so
GitHub refuses to merge it until you approve. On a pull request you opened, GitHub would count the
App's approval, and only the instruction that agents never approve stands against it, as
[Connecting GitHub](connecting-github.md#what-enforced-still-allows) explains. In Instruction only, or with your own GitHub login still on the machine, nothing on GitHub
enforces that a person merges: an agent acting as your account could approve or merge a change
itself. What holds the line then is the machine-wide
instruction every session reads, `~/.claude/CLAUDE.md`, that an agent merges only what your agent
policy permits. The install places that file only when you have none, so if you had one already, add
the Merging section and the Library section from Builder's version to it; the install prints that
version's path when it leaves yours alone. The rest is you pressing merge after reading the change
and the reviewers' findings. The Library section tells an agent never to hand-build a branch or pull
request for a path under `projects/` in your knowledge repository, and it carries the rules for work
items and for a missing tool as well.

**If you can get administrator rights, use the two-account install once it is built.** Today the
single-account install is the only shape built, and you install it whether or not you have the
administrator password. [Installing Builder](installing.md#which-install-is-yours)
says which route fits your machine. On Debian or Ubuntu with an account that can use `sudo`, that
route's first command runs Builder's checked-out code as root, once, and [Before you
start](installing.md#before-you-start) says so before you run it.

## Where to go next

- **[How many machines Builder runs on](where-everything-runs.md)** covers putting Builder on one
  machine or several, and what a second machine buys you.
- **[Connecting GitHub](connecting-github.md)** sets up the GitHub App your agents act as.
- **[Installing Builder](installing.md)** walks through the install.
- **[The glossary](glossary.md)** explains each word Builder uses.
