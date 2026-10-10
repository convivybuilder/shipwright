# Where everything runs

Builder runs on one computer, and it is built so that its parts can sit on different machines as you
add them. This page says which parts those are, and what each machine is doing. Like a bead, which
is a project's short description of where it is going, the page describes Builder as it is designed
to work. [Installing Builder today](installing.md) covers the install itself, as Builder's first
public release runs it. [How Builder works](how-builder-works.md) explains the parts themselves.

You can use Builder without reading this page. It is here for two moments: when you choose how to
install Builder, and when you want a second machine to keep work going while your laptop is shut.

The page names several parts of Builder, so here they are in one place.

- **A session** is a conversation with Claude, an AI model, in a terminal, and it is how work gets
  done.
- **An agent** is a model given a role and the tools it may use, put to work on a task by a session.
- **The Library** is where Builder keeps everything a project knows.
- **The Bosun** is the part of Builder that governs agents.
- **Deck** is the desktop application where you pilot each project, and **Orient** is the view of
  the whole system.

## One machine is the whole system

Install Builder on a laptop and everything is there: the Library, the sessions you work in, the
agents they put to work, and Deck. Nothing talks to anything off that machine except Claude and
the services your projects use. This is where everyone starts, and for a project you work on while
sitting in front of it, it is where you can stay.

What one machine cannot do is carry on without you. Your sessions live as long as the machine is
awake, so an overnight run wants somewhere that stays on. That is what a second machine is for.

## Two install shapes

Builder installs in one of two shapes, and you name the shape when you install. The shape decides
which user account on the machine Builder runs as, and that decides what an agent can reach. The
install never moves you from one shape to the other by itself: when the two-account install cannot
complete, it stops and says what it lacked. This release installs only the single-account shape;
the two-account install comes in a later release.

### The two-account install

Builder runs under accounts of its own, separate from yours. The install creates two accounts on
each machine that runs it, with the administrator password, and leaves your own account to you.

- **`agents` runs everything Builder does**: the steward, which is the first session you meet,
  every crew's session, the agents they put to work, the Library, Orient and the background jobs. A
  crew is one project and everything working on it. Builder's folder, `~/builder`, is in this
  account. The account holds none of your credentials and has no administrator rights.
- **`reviewers` runs the agents that review a change.** `agents` can ask for a review and cannot
  sign one. One rule lets it start a single program that the administrator account owns, and that
  program fixes which pull request and commit are reviewed, runs the reviewer as `reviewers`, and
  posts the verdict to GitHub itself. A pull request is a proposed change waiting to be accepted,
  and a commit is one recorded version of it.

You reach your sessions over SSH as `agents`, which is what Deck does for you. SSH is a standard
way to open a terminal as another account or on another machine. You read what the sessions wrote
through your membership of each account's group, without `sudo`, the command that borrows
administrator rights. Neither account can read the other's folder, and neither can read yours.

**This is what keeps a merge yours to decide.** To merge a change is to accept it into the project.
An agent that can edit Builder's code can change what the other agents run, since they all run as
`agents`. It cannot make a change merge on its own say, because GitHub accepts only review checks
signed with a key that only the administrator account and the review program can read, and the only
way to get one is for the review program to run. The exceptions are the kinds of merge your agent
policy hands to agents, which still need a passed review. A review check is a reviewer's pass or
fail verdict, posted on the pull request.

### The single-account install

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
administrator password. [Installing Builder today](installing.md#which-parts-of-this-page-to-read)
says which route fits your machine. On Debian or Ubuntu with an account that can use `sudo`, that
route's first command runs Builder's checked-out code as root, once, and [Before you
start](installing.md#before-you-start) says so before you run it.

## The three seams

A seam is a place where Builder can be split across machines. There are three, and everything else
follows from them.

**The Library serves machines it does not sit on.** Sessions, Deck and Orient all reach it as a
service, over the network, and never by opening its files. So the Library can live on the machine
that stays on while you work from your laptop.

The Library is one service holding all three of its parts, which are called vaults, and the vaults
are not placed separately. The Reference Room holds what a project holds to be true, and many
systems call it a knowledge base. The Chart House holds each project's plan and state. The Archives
hold records of what happened. All three share one librarian, the component that answers requests,
and one search index, because "what matters to the work I am about to start" is a single question
whose answer may be a document, a work item or a review from months ago.

**Sessions run wherever you start them, and you drive them from wherever you are.** Every machine
that hosts sessions runs an Individuator, the part that brings agents into being there. When a
session asks for an agent, its Individuator gets the approval and the documents, then builds and
runs that agent on its own machine, so the agent works next to the files it is changing. Deck
reaches a session on another machine over SSH and shows it to you as though it were local.

**The Bosun is one service for every machine.** It approves each request for an agent, authorizes
what agents do and records what each run cost, which makes it the one part that has to see all of
them. It can share a machine with the Library or have one of its own.

## The usual two-machine arrangement

| machine | what it runs |
|---|---|
| your laptop | Deck, and a session when you want to work on something locally |
| the machine that stays on | the Library, the Bosun, Orient, the sessions that do long or overnight work, and any app you host for yourself |

You open Deck on the laptop, pick a project, and work in a session that is running on the other
machine. Shut the laptop and the session carries on, because nothing about it was running on the
laptop. Open Deck again in the morning and you are back in the same session where it got to.

The two machines need a network path between them, and Tailscale, a private network across your own
devices, is the easy way to get one. [What you need](what-you-need.md) covers that, along with the
hardware.

## What crosses between machines

This section is for a reader who wants to know what travels over the network, and what stays on
the machine where the work happens. Three things cross.

**Your terminal crosses.** Deck runs your session over SSH as the `agents` account, so what travels
is the session's output and your typing. The Slate, where a session leaves you questions, crosses
the same way: Deck reads and writes it over that SSH connection.

**Library requests cross.** A session asks the Library for a document or a work item over the
network, and the Library knows which machine is asking, because each machine holds an identity of
its own that the request proves. The documents an agent needs are fetched by the Individuator on
the agent's machine, so a large document never travels through the session that asked for it.

**Approvals cross, and what they are about stays put.** A tool call is one action an agent takes,
such as running a command or writing a file. An agent's every tool call goes through its local
Individuator, which asks the Bosun whether it is allowed; the answer comes back and the file or the
command never leaves the machine. An agent holds no credential of its own, so cutting one off means
the Individuator declines to act for it, and nothing you are using has to be revoked.

## Adding more machines

The same three seams answer the larger case without changing shape. One Library on a capable
machine serves many people, the Bosun sits beside it or on its own machine, and every machine that
hosts sessions runs an Individuator, including each person's laptop. Everyone reaches their own
sessions through Deck, and Orient gives whoever wants it a view across all of them.

A team's arrangement is therefore the same Builder as a single laptop's, with the parts spread
further apart, which is what putting the seams in these three places buys.

## Where to go next

- **[What you need](what-you-need.md)** covers the hardware, accounts and network.
- **[How Builder works](how-builder-works.md)** shows how the parts fit together.
- **[The glossary](glossary.md)** explains each word Builder uses.
