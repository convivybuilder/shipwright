# How Builder works

Builder is a way to build software, or any project, with AI agents, in which a project's goal, plan,
decisions and history all live where the agents can read them. This page explains how its parts
work together, and it assumes you have met none of them. Like a bead, which is a project's short
description of where it is going, the page describes Builder as it is designed to work, and the
system is still catching up to that design. Each term is explained where it first appears, and the
[glossary](glossary.md) lists them all.

The page follows the order in which you would meet things. It starts with who you talk to, then
covers how a project is planned, where everything is kept, how a change is made and reviewed, how an
agent is put to work, and the two applications you watch it all through.

## Sessions, the steward and crews

You work with Builder through **sessions**, which are conversations with Claude, an AI model,
running in a terminal. A terminal is a window where you type instead of clicking. In a session you
write what you want in plain language, and Claude answers and does the work.

The first session you meet is the **steward**. It owns no project of its own. It asks what you want
to build, sets up projects, and carries decisions between them.

Each project is run by a **crew**. A crew is a working directory, which is the folder holding the
project's files, together with the sessions that work in it and the agents those sessions put to
work. An **agent** is a model given a named role, such as a reviewer, and one task to do. The
steward creates your first crew in your first session.

## How a project takes shape

A project develops in four steps, and each step leaves a record the agents can read later.

1. **The crew writes its bead.** A bead is a short description, a few hundred words, of where the
   project is going: what it is for and how it will work once finished. It describes the
   destination, so it changes only when the destination does.
2. **The gap becomes epics.** The crew compares the bead with what exists and turns the difference
   into **epics**, which are pieces of work large enough to plan. Each epic carries a
   **specification**, describing the project once the epic is done, and a **definition of done**,
   the conditions that show it is.
3. **The epics are ordered into a Course.** A **Course** is the crew's route from where the project
   stands to where its bead says it is going. It puts the epics in order and sets no dates.
4. **The work arrives as work items.** Each epic breaks into **work items**, each with a definition
   of done and a concrete course of action. Work that arrives outside the plan, such as a defect
   found along the way or a small fix, goes into the **corrections queue**. That queue holds
   interruptions to the plan, and its length says nothing about progress.

Here is an invented example. Suppose you want a tool that records the birds you see. The bead says
what the finished tool does for you. One epic might be "sightings can be saved and listed", with a
definition of done you could check by saving one. A work item under it might be "add the form that
saves a sighting". A typo you notice in a label along the way goes into the corrections queue.

## The Library: where everything is kept

Every document and record of a project goes into the **Library**. Builder sorts everything into two
kinds.

- **Canonical knowledge** is what the project holds to be true.
- **Memory** is a record of what happened.

A design proposal is memory while it is a draft and becomes canonical knowledge once it is accepted.

Most memory is kept. What keeps search useful is deciding what goes into the search index, the
catalogue that search reads. Most of the routine records a project generates as it runs stay
reachable directly but out of search by meaning, which is search that finds a record because it is
about what you asked. A kind of memory is discarded only when it stops being useful, never for its
age.

The Library holds it all in three parts, called **vaults**.

- **The Reference Room holds canonical knowledge**: beads, decision records, architecture and
  how-to documents. Many systems call this the **knowledge base**. Its documents are files in a
  git repository, so every change is kept as a diff and many sessions can read them at once. Git is
  a tool that records every change to a folder of files, a repository is a folder it keeps that
  way, and a diff is its line-by-line record of one change.
- **The Chart House holds the state of every project**: epics, work items, Courses, and who is
  working on what. It is memory kept close at hand because every session needs it, and it is the
  one vault that settles competing claims on the same item.
- **The Archives hold the rest of memory**: reviews, comments, records of each agent's run, and
  **signals**, which are observations worth keeping. They are written once and read for context.

A component called the **librarian** answers requests and refuses the ones that break a rule. One
search index covers all three vaults and holds what is worth finding by meaning, so asking what is
relevant to the work you are about to start can return a document, a related work item or a review
from months ago.

Keeping it all in one place is the point. When a project's plan lives in a separate ticket tracker
and its reasoning lives in pull request descriptions, the agents doing the work cannot reach either
when it matters. [Why Builder](why-builder.md) makes that argument in full.

## Checkout: how a crew changes something

To change a document or a work item, a crew **checks it out**, the way you would borrow a book
from a library. Checkout gives the crew a **lease**, a hold that stops anyone else changing the same
item, along with a short briefing on nearby work that might already cover it. The crew makes its
change and returns it.

Where the change lands depends on what was changed.

- **A change to a work item** is written straight into the Chart House.
- **A change to canonical knowledge** lands one of two ways. A decision you state yourself in a
  session is approved by you there. Every other change goes back to the Library as a pull request,
  which is reviewed before it merges, and that includes the steward's own edits. The exception is a
  change pushed to your knowledge repository's `main` with git, which no one reviews. You make one
  when you change an agent, a profile or the policy, which on a fresh install is the only way to
  change them. A crew's session can make the same push as you, held back only by the instruction
  every agent carries, and the install's update of the starter set lands on `main` the same way.
  [Customizing Builder](customizing.md) says how. A **pull request** is a proposed change, packaged
  so it can be read and checked before it is accepted, and to **merge** it is to accept it.

A lease on a work item covers its whole epic, so two crews cannot take up the same piece of work
under two different names. A lease lapses on its own when its holder stops showing signs of
activity, so an abandoned session blocks nobody for long.

## Review: what decides a merge

This section explains how Builder makes sure a change was reviewed before it is accepted, and where
that protection is weaker. The protection depends on the install's shape. The next two paragraphs
describe the two-account install, which is not built yet; the single-account install, the only
shape built today, comes after them and has the weaker protection.

A change to code becomes a pull request, and two agents review it: a **reviewer**, who reads it for
mistakes, and a **security reviewer**, who reads it for what an attacker could do with it. Each
posts its verdict to GitHub, the website that hosts the project's repository, as a **review check**.
A check is a pass or fail mark GitHub shows on a pull request, and a passing one is called green. A
rule on `main`, the repository's current version, lets the pull request merge only when both checks
are green against `main`.

The reviewers do not run as the crew that wrote the change. Builder runs as an account called
`agents`, which is a separate user account on your computer, and reviews run as a second account,
`reviewers`, started by one program that `agents` may ask to run and cannot change. The checks are
signed by the **approver**, a GitHub App whose key only the machine's administrator account and the
review program can read, so a green check means a review ran on exactly that commit. A GitHub App
is an identity on GitHub that belongs to a program, and a commit is one recorded change. A crew
that rewrote Builder's own code still could not produce a green check.

That is the two-account install. The single-account install runs Builder as your own account and has
no approver: the reviewers post their findings on the pull request, and the rule on `main` that you
set on GitHub can require a pull request and the repository's own automated checks. Its agents reach
GitHub as an App you create, and you choose one of two merge modes, which [Connecting
GitHub](connecting-github.md) sets up. In **Enforced**, the rule on `main` requires an approval from
the one person a file named `CODEOWNERS` lists, you, so GitHub refuses to merge a pull request an
agent opened until you approve it. On a pull request you opened and only you pushed
to, GitHub asks for no code owner's review and would count an agent's approval, as [What Enforced
still allows](connecting-github.md#what-enforced-still-allows) explains. In **Instruction only**, nothing on GitHub stops an
agent from merging, so the rule that you merge is held by the machine-wide instruction every session
reads, `~/.claude/CLAUDE.md`. That instruction stands in both modes. The install writes that file
only when you have none, and [Where everything runs](where-everything-runs.md#the-single-account-install)
says what to do if you had one.

The decision to merge is yours. On the two-account install the review checks say a change may merge;
on either install you decide that it does, unless your agent policy names that kind of change. The
agent policy is a file you own that lists what agents may do without you. Your knowledge repository,
the git repository that holds the Reference Room, is the one place the Library merges for itself.
`agentctl kb merge`, the command the Library merges through, and `agentctl docs merge`, which merges
reviewed documentation, each read the policy and refuse anything it does not permit. On the
single-account install that refusal covers only merges made through those commands. In Enforced
mode GitHub refuses the rest without your approval, except on a pull request you opened, where only
the instruction stops an agent approving; in Instruction only, an agent could merge
another way, and the `~/.claude/CLAUDE.md` instruction above is the rule against it. A merge you start from Deck or Orient takes a separate path, through a merge check in
the Library, and that check approves every merge it is asked about for now, as [Installing
Builder](installing.md) says.

## The Bosun: how an agent is put to work

An **agent** is a named role that can be put to work: a persona, a model and the tools it may use.
The **Bosun** is the part of Builder that governs agents. It approves each request for an agent,
authorizes every action an agent takes, such as running a command or writing a file, keeps agents
out of each other's way, and records what each run cost and whether it worked. Which documents
matter to a piece of work, which model suits a role and what a run may spend are all decided in the
Library, and the Bosun carries those decisions out.

Bringing an agent into being is called **individuation**. Nothing new is created: one individual
agent is drawn out of the knowledge, documents and code that already exist, with a clean place to
work, the documents its role needs, and only the powers the role allows.

Individuation runs in four steps. They involve two credentials, which are proofs of permission that
one program shows another.

1. **A session asks for an agent.** It names the role and the work item, and asks the
   **Individuator**, the component on its own machine that individuates agents. The Individuator
   passes the request to the Bosun.
2. **The Library writes a call slip.** The Bosun asks the Library, which checks out the work item
   and issues a **call slip**, a single-use credential naming the work item, the documents that work
   needs, the model the agent will use and what it may spend. The Library chooses those documents
   from the crew's **profile**, its list of what each role should read, and adds the project's plan
   and state from the Chart House. The Bosun signs the slip's persona and permissions and passes it
   back to the Individuator.
3. **The call slip becomes a library card.** The Individuator trades the call slip, once, for a
   **library card**, a credential bound to that one agent for its working life. The Individuator
   holds the card and makes every Library request for the agent, and the Library can withdraw a card
   at any time.
4. **The agent starts with its documents in hand.** The Individuator builds the agent's workspace
   with the documents the call slip named already checked out, connects it to its model, and starts
   it.

The result is an agent that begins its task already holding the work item, the relevant decisions
and the project's plan, with no permission beyond what its role allows.

The names come from closed-stack libraries, where a patron hands a slip across the desk to receive
material and carries a card from one visit to the next.

## Where you work and where you watch

Two applications show the system. **Deck** is where you pilot each project hands-on. It shows the
state of everything in that project as it happens, and it makes it easy to move from one project to
another whenever you want. **Orient** is a view of the whole system, less for doing things than for
understanding them. You can narrow it to one crew when you want to, and the global view is always
one step away.

## Where to go next

- **[Getting started](getting-started.md)** takes you from installing Builder to your first crew.
- **[Where everything runs](where-everything-runs.md)** shows which parts can live on which machine.
- **[The glossary](glossary.md)** explains each word Builder uses.
