# Why Builder

This page makes the case for Builder to someone who has never seen it. Like a bead, which is a
project's short description of where it is going, the page describes Builder as it is designed to
work, and the system is still catching up to that design. Each term is explained where it first
appears, and the [glossary](glossary.md) lists them all.

## Two complaints you have probably made

If you have built anything with an AI model, such as Claude, you have seen it go wrong in ways that
are hard to pin down. It states something false with complete confidence. It forgets a decision you
made an hour ago and argues you out of it again. It fixes one thing, breaks another, and then undoes
its own fix, going around in circles. It tells you the work is done when it is not. People conclude
that the models are unreliable and that they hallucinate, which is the common word for a model
inventing something and presenting it as fact.

If you have worked on a team, you have probably made the other complaint too. Most teams list their
work in a ticket tracker, a tool that holds one entry for each task. The tracker is confusing, it
takes longer to update than the work takes to do, and the reason behind anything sits three links
away, when anyone wrote it down at all.

## They are one problem

Builder treats those two complaints as one problem: the context a piece of work needs lives
somewhere the worker cannot reach. Context here means everything a worker has to know to do the
work well.

A model does good work when it has the right context at the moment it works. That means knowing
what the project is for, what has been decided and why, what was tried and failed, and what counts
as done. When that context is missing, the model fills the gap with a plausible guess, and much of
what gets called hallucination is that. When the model never saw a decision, it reopens it, and that
is what going in circles looks like from the outside.

The tools most teams use scatter that context across three places.

- **The plan lives in a ticket tracker.**
- **The reasoning behind a change lives in a pull request description.** A pull request is a
  proposed change to a project, and its description is the note explaining the change.
- **The decision lives in a chat thread.**

All of it was written down, and none of it is where a model can retrieve it when it matters. People
pay for the same scatter in their own way, in time spent hunting for things and in decisions that
get made twice.

## Everything is memory, except canonical knowledge

Builder rests on one idea: **everything is memory, except canonical knowledge, and memory is where
all project structure happens.**

Those two terms carry the whole design, so here is what each means.

**Canonical knowledge is what your project holds to be true.** It covers the project's goal, its
decisions, how it is built and how to work on it.

**Everything else is memory, a record of something that happened.** A plan is memory, and so is a
work item, a review, a conversation or an attempt that failed. A design proposal is memory while it
is a draft and becomes canonical knowledge once it is accepted.

Builder keeps all of it in one place, called the Library, and routes each thing by one rule.

- **Canonical knowledge goes to the Reference Room**, which many systems call the knowledge base.
  A change there lands one of two ways: a decision you state yourself and approve in the session,
  or a pull request that is reviewed before it merges, which is how the steward's own edits land
  too. A session is a conversation with Claude, and the steward is the first one you will meet.
- **Most memory goes to the Archives, written once and kept.** Each kind of memory gets three
  separate answers: whether it is kept, whether it goes into the index that search reads by
  meaning, and whether it sits in fast or slow storage. Search by meaning finds a record because
  it is about what you asked, even when it shares no words with your question. Most of the routine
  records a project generates as it runs are kept but left out of that index. They can still be
  looked up directly, and a search for what matters is not buried under them. A kind of memory is
  discarded only when it stops being useful, never for being old.
- **Memory that every session needs all the time goes into a store kept close at hand.** The first
  is the Chart House, which holds each project's plan and the state of its work. When another kind
  of memory turns out to be needed constantly, it gets a store of its own.

The consequence is the point. A project's plan, its work items and who is working on what are all
memory, kept in the same system as everything else, where every agent can reach them. An agent is
an AI model given a role and the tools it may use, and Builder puts many of them to work on your
project.

## Why the plan has to live inside the system

A plan kept outside the system is a plan the models do not have. A work item in a separate tracker
cannot change what an agent does, because the agent cannot see it at the moment it would matter. In
the Chart House, the same work item is available to every agent whenever it turns out to be
relevant.

So when Builder puts an agent to work on a task, it hands the agent what that task needs: the work
item, what counts as done, the decisions that bear on it and the history worth knowing, and little
else. Narrow, specific context is what makes a model effective. It also makes the model cheaper to
run, because an agent handed what it needs spends nothing looking for it.

## What it is like to work this way

**A project starts from where it is going.** Before anything is built, a project writes down its
destination in a few hundred words, called its bead, and every piece of work is measured against
it.

**Decisions stay made.** A decision is recorded as canonical knowledge, and agents read it before
they act, so nobody argues the same point twice, the agents included.

**You can see everything in flight.** Builder shows you what you are working on. Work on one thing
and that is what you see. Start five and you see all five, which is as messy as it sounds, and it
is how you notice you have stopped finishing things.

**Work is checked before it is reported.** A change to what your project holds to be true lands only
once it is reviewed or, for a decision you state yourself, once you approve it. An agent reports the
check it ran along with what the check returned, so "done" arrives with its evidence.

**You learn it by using it.** Your first session is with the steward, which asks what you want to
build and gets the smallest real version of it running with you. It explains the system when a
question comes up, in the middle of the work that raised it.

**It has opinions.** Builder's way of working comes from building real products with it, so you
start with the results of that trial and error and do not pay for it yourself.

## Who it is for

Builder is for builders. Software is the leading case, and engineers are the readers best placed to
judge whether these claims hold, so please judge them. It is equally for someone who has never
written a program and builds tools for their own work.

What is at stake for both is the same. Many people feel precarious about what their work becomes
when a model can do much of it. We think the people who do well will be the ones who get good at
directing that work, and directing it well takes tools built around what a model needs.

## Where the field is

There are plenty of ideas about building with AI, and less progress than the ideas suggest. Most
environments for agent-driven development still look like code editors with a chat panel, and the
ones aimed at people who do not write code look like note-taking apps. Builder is arranged around
two needs instead: the model's need for context at the moment it works, and the person's need to
know where the work stands. We would rather it moved the field toward that than won a category.

## What we are sure of

Some of this will not survive contact with the world. We are confident in the direction: context
belongs where the work can reach it, and project structure is memory. We are less sure of every
part built on that, and Builder will change as people use it.

## Where to go next

- **[The glossary](glossary.md)** explains each word Builder uses.
- **[How Builder works](how-builder-works.md)** shows how the parts fit together.
