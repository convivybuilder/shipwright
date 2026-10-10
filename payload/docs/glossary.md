# Glossary

This page explains, one at a time and in alphabetical order, the words you will meet using Builder.
Like a bead, which is a project's short description of where it is going, the page describes Builder
as it is designed to work, and the system is still catching up to that design.
[How Builder works](how-builder-works.md) shows how the parts fit together.

There are two kinds of entry here. Some are Builder's own words, such as crew, bead and steward.
Others are ordinary tools of software work, such as pull request and SSH, which the other pages use
and which you may never have met. A word set in `code type` is a name you will see typed exactly
that way. You do not need to learn these before you start. The steward, the first session you talk
to, explains each one when the work reaches it.

**adjacency briefing** — The short list of nearby work you receive when you check out a work item.
It names items close enough to yours that you may be about to duplicate one. It warns and never
blocks.

**agent** — A named role Builder can put to work. An agent is made of three things, which are a
persona, a model and the tools it may use. You ask for an agent by its name, such as a reviewer.

**agent policy** — The file in your knowledge repository that says what agents may do without you.
It names the kinds of pull request an agent may merge once review passes, how many review rounds run
before you decide, and how many agents run at once. Out of the box it names nothing an agent may
merge. `agentctl kb merge`, the command the Library merges through, reads the policy and refuses
anything it does not permit. A merge you start from Deck or Orient takes a separate path, through a
merge check in the Library, and that check approves every merge it is asked about for now, as
[Installing Builder](installing.md) says. [Customizing Builder](customizing.md#the-agent-policy)
shows how to change it.

**`agents`** — The account the two-account install runs Builder as. The steward, every crew's
session, the agents they put to work, the Library and Builder's background jobs all run there, and
`~/builder` is in it. It holds none of your credentials and has no administrator rights. You reach
it over SSH and read what it writes through its group.

**approver** — The GitHub App that posts review checks on the two-account install. Its key is read
only by the machine's administrator account and the program that runs a review, so no agent can post
a check itself.

**Archives** — The part of the Library that holds records of what happened, such as reviews,
comments, records of agent runs, and signals. Each entry is written once and kept for context.

**bead** — A crew's short description, a few hundred words, of where its project is going. It says
what the project is for and how it will work once finished. A crew writes its bead first, with the
`write-bead` skill, and changes it only when the destination changes.

**Bosun** — The part of Builder that governs agents. It approves each request for an agent,
authorizes every action an agent takes, and records what each run cost and whether it worked. What
an agent may read or spend is decided in the Library, and the Bosun carries it out. The name comes
from the ship's officer who assigns a crew its work.

**call slip** — A single-use credential the Library issues when a work item is checked out for an
agent. It names the work item, the documents that work needs, the model the agent will use and what
it may spend. The Individuator trades it once for a library card.

**canonical knowledge** — What a project holds to be true, which covers its bead, its decisions, how
it is built and how to work it, including every design proposal that has been accepted. It is kept
in the Reference Room, which many systems call the knowledge base. A change to it lands either as a
decision you state yourself and approve in the session, or as a pull request reviewed before it
merges, which is how the steward's own edits land too.

**Chart House** — The part of the Library that holds the state of every project, meaning its epics,
work items, Courses, and who has checked out what. It is the one part of the Library that settles
competing claims on the same item.

**charter** — The steward's instructions, kept in a file named `CLAUDE.md` in the steward's
directory. It says what the steward owns, how it creates a crew and how it routes work between
crews, and it is yours to edit.

**checkout** — How you begin changing anything in the Library. Checking out a document or a work
item gives you a lease, so nobody else changes it while you work, and for a work item it also gives
you an adjacency briefing. You make the change and return it.

**Claude Code** — The program that lets you talk with Claude, an AI model, in a terminal. Every
Builder session is a conversation in Claude Code.

**`co`** — The command that starts a crew's session, the crew orchestrator, in the crew's directory.

**corrections queue** — Where work arriving outside the plan goes, such as a defect found along the
way or a small fix. Every work item belongs either to an epic or to this queue. Its length measures
nothing about progress.

**Course** — A crew's route from where its project stands to where its bead says it is going. It is
an ordered list of epics, and it sets the order and no dates.

**crew** — One project and everything working on it, which is a directory, the sessions that work
there and the agents they put to work. The steward creates crews with the `new-crew` skill.

**crew orchestrator** — The session that runs a crew's work. It chooses the work, does some of it
itself and hands the rest to other agents. You start one with the `co` command.

**Deck** — The desktop application where you pilot each project hands-on. It shows the state of
everything in a project as it happens, and it makes it easy to move from one project to another.

**definition of done** — The checkable conditions that end a piece of work. Every epic and work item
carries one, so anyone can tell when it is finished.

**epic** — A piece of work large enough to plan, carrying a specification and a definition of done.
A Course orders epics, and each epic breaks into work items. Checking out any work item under an
epic holds the whole epic.

**git** — The tool that records every change made to a folder of files, so any earlier version can
be read or restored and several people or agents can change the same files safely. A folder git
keeps this way is called a repository.

**GitHub** — A website that hosts git repositories. It is where a pull request is opened, reviewed
and merged, and it keeps a copy of your work off your own disk.

**GitHub App** — An identity on GitHub that belongs to a program instead of a person, with narrow
permissions of its own. Builder acts on GitHub through three GitHub Apps you create on your own
account, one for the Library, one for the Bosun, and the approver. The single-account install has no
approver, and its agents act through an App of their own instead.
[What you need](what-you-need.md#the-three-apps) explains them.

**Homebrew** — A free program for the Mac that installs other programs from one typed command.

**individuation** — Bringing an agent into being from a role, with a clean place to work, the
documents the role needs, and only the powers the role allows. Nothing new is created. One
individual agent is drawn out of the knowledge, documents and code that already exist, and it starts
with the documents its call slip named already checked out. The verb is individuate.

**Individuator** — The component on each machine that individuates agents for the sessions there. It
trades each call slip for a library card, builds the agent's workspace, and makes the agent's
Library requests with the card.

**instruction block** — A document of rules that Builder composes into a crew's instructions, such
as how a crew's session works with you or how it opens a pull request.

**Keel** — The engine underneath Builder, of which the Library and the Bosun are parts. It shapes
how work is done, whether it succeeds and what it costs. It has no screen of its own, and you reach
it through Deck and Orient. The name comes from the backbone a ship is built on.

**knowledge base** — What many systems call a store of canonical knowledge. Builder calls it the
Reference Room.

**knowledge repository** — The git repository that holds the Reference Room's documents. The install
puts it at `~/builder/knowledge`.

**lease** — The hold checkout gives you on a document or a work item, which stops anyone else
changing it until you finish. A lease on a work item covers its whole epic. It lapses on its own
when you stop showing signs of activity.

**librarian** — The component inside the Library that answers requests and refuses the ones that
break a rule, such as a change to an item someone else has checked out.

**Library** — Where Builder keeps everything a project knows. It has three parts, which are the
Reference Room for canonical knowledge, the Chart House for the state of every project, and the
Archives for records of what happened. Every change goes through it, except a change pushed to your
knowledge repository with git, by you, by a crew's session or by the install's update of the starter
set, which [Customizing Builder](customizing.md) describes.

**library card** — The credential a call slip is traded for, bound to one agent for its working life.
The Individuator holds it and makes every Library request for the agent, and the Library can
withdraw it at any time.

**`main`** — The main line of a repository, which is the version everyone treats as current. A
change joins the project when it is merged into `main`.

**memory** — Builder's word for any record of what happened; everything else it keeps is canonical
knowledge. A design proposal still in draft is memory. Most memory goes to the Archives, where most
of the routine records a project generates are kept and are left out of the search index. Memory
needed constantly, such as the state of every project, is kept in the Chart House. A kind of
memory is discarded only when it stops being useful.

**merge** — To accept a pull request, so that its change becomes part of `main`.

**model** — The AI system that does the reading, reasoning and writing, such as Claude. An agent is
a model given a role and tools.

**operator** — Builder's word for you, the person directing the work.

**Orient** — The view of the whole system, less for doing things than for understanding them. You
can narrow it to one crew, and the global view is always one step away.

**profile** — A crew's list of the documents each of its roles should read. The Library uses it to
choose the documents an agent starts with. [Customizing
Builder](customizing.md#a-profile-for-one-crew) shows how to give a crew its own.

**pull request** — A proposed change to a repository, packaged so that it can be read, checked and
discussed before it is accepted. Accepting it is called merging.

**Reference Room** — The part of the Library that holds canonical knowledge, which is beads, decision
records, architecture and how-to documents. Its documents are files in a git repository, so every
change is kept as a diff, a line-by-line record of what changed.

**repository** — A folder of files whose whole history git keeps. Builder's own code lives in
repositories, and so do the Reference Room's documents and the projects your crews build.

**review check** — On the two-account install, a reviewer's verdict on a pull request, posted to
GitHub by the approver. The rule you add on `main` lets a pull request merge only when both review
checks, the reviewer's and the security reviewer's, are green against `main` and were posted by the
approver, so a check of the same name posted by anyone else does not count. An organisation
administrator is exempt from the rule.

**reviewer** — The agent that reads a pull request for mistakes and reaches a verdict. On the
two-account install the approver posts that verdict to GitHub as a review check.

**`reviewers`** — The second account the two-account install creates, which runs the agents that
review a change. `agents` can start a review only through one program the administrator account
owns, which fixes the pull request and commit and posts the verdict itself.

**run** — One agent doing one piece of work from start to finish, with a record of what it did and
what it cost.

**security reviewer** — The agent that reads a pull request for what an attacker could do with it.

**session** — A conversation with Claude in a terminal. The steward is a session, and each crew
works through sessions of its own.

**signal** — An observation worth keeping that is not yet a piece of work, such as a risk noticed in
passing. Signals are kept in the Archives, where each one can be looked up directly, and whether a
kind of signal is also found by search is decided for that kind.

**single-account install** — The install shape that runs Builder as your own account, for a machine
where you have no administrator password, or for starting without GitHub. It creates no account and
has no approver. Its agents reach GitHub as an App you create, and in the merge mode called
Enforced, GitHub refuses to merge a pull request an agent opened until you approve it; in
Instruction only, the agents'
instructions hold that rule. [Connecting GitHub](connecting-github.md) sets it up.

**skill** — A set of instructions a session loads for a particular job. Builder installs four of
its own: `new-crew` and `new-subcrew`, which create a crew and an extra session within one,
`write-bead`, which writes a crew's bead, and `take-upstream`, which brings later changes to Builder
into a fork. It also links two writing passes, `write-better` and `talk-better`.

**Slate** — A sheet in Deck for each crew, where the crew's session leaves the questions it needs
you to answer and you keep notes to send it at a break point. [The Slate](the-slate.md) explains it.

**specification** — The description, carried on an epic, of how the project will stand once the
epic is done. It describes that end state and leaves history and plans out.

**SSH** — A standard way to open a terminal on another machine, or as another account on the same
machine, over an encrypted connection.

**starter set** — The documents Builder installs into your knowledge repository to begin with,
which are four agents, their instructions, a default profile and the agent policy.

**steward** — The first session you meet after installing Builder. It owns no project. It asks what
you want to build, creates crews, and carries decisions between them. It lives in its own directory,
`~/builder/steward` in the `agents` account by default, and its instructions there are yours to
edit.

**Tailscale** — A private network across your own devices. Each machine you sign in gets a stable
address the others can reach, and nothing is published to anyone else.

**terminal** — A window where you type commands and read what the computer answers. On a Mac the
application is called Terminal. In a path typed there, `~` stands for your account's home folder.

**tmux** — A background program that keeps terminal sessions running after you close the window, so
you can leave a session working and come back to it.

**two-account install** — The install shape that runs Builder as `agents` and its reviews as
`reviewers`, with the administrator password, so a merge waits on review checks no agent can post.
This release installs only the single-account shape; the two-account install comes in a later
release.

**vault** — One of the Library's three parts, which are the Reference Room, the Chart House and the
Archives. Each holds a different kind of thing under its own rules.

**waypoint** — A point on a Course that marks progress along the route. A waypoint can be the
completion of one epic. A synthetic waypoint is reached when a set of epics and corrections are all
done, which marks progress that no single piece of work delivers on its own.

**work item** — A single piece of work with a definition of done and a concrete course of action.
Each belongs either to an epic or to the corrections queue.

**work queue** — The list of every piece of work across your projects, each one a work item. The
Library serves it and keeps it in its database.
