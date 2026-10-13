# How many machines Builder runs on

Builder can run on one computer, and it is built so that its parts can sit on different machines as
you add them. This page is about how many machines to install it on, how an install across more than
one machine fits together, and why a second machine lets your sessions keep working while your laptop
is shut. [Installing Builder](installing.md) covers the install itself, as Builder's first public
release runs it. [How Builder works](how-builder-works.md) explains the parts themselves. Which user
account Builder runs as on a machine is a separate choice, which [One account vs. multiple accounts
on the server](accounts-on-the-server.md) covers.

You can use Builder without reading this page. It is here for two moments: when you choose how many
machines to install Builder on, and when you want a second machine to keep work going while your
laptop is shut.

The page names several parts of Builder, so here they are in one place.

- **A session** is a conversation with Claude, an AI model, in a terminal, and it is how work gets
  done.
- **An agent** is a model given a role and the tools it may use, put to work on a task by a session.
- **The Library** is where Builder keeps everything a project knows.
- **The Bosun** is the part of Builder that governs agents.
- **An Individuator** runs on every machine that hosts sessions, and brings agents into being there.
- **Deck** is the desktop application where you pilot each project, and **Orient** is the view of
  the whole system.

## You can put the whole system on one machine

Install Builder on a laptop and everything is there: the Library, the sessions you work in, the
agents they put to work, and Deck. Nothing talks to anything off that machine except Claude and
the services your projects use. For a project you work on while sitting in front of it, one machine
is all you need.

What one machine cannot do is carry on without you. Your sessions live as long as the machine is
awake, so an overnight run wants somewhere that stays on. That is what a second machine is for.

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

**Your terminal crosses.** Deck runs your session over SSH as the account Builder runs as on the
other machine, so what travels is the session's output and your typing. SSH is a standard way to
open a terminal as another account or on another machine. The Slate, where a session leaves you
questions, crosses the same way: Deck reads and writes it over that SSH connection.

**Library requests cross.** A session asks the Library for a document or a work item over the
network, and the Library knows which machine is asking, because each machine holds an identity of
its own that the request proves. The documents an agent needs are fetched by the Individuator on
the agent's machine, so a large document never travels through the session that asked for it.

**Approvals cross, and what they are about stays put.** A tool call is one action an agent takes,
such as running a command or writing a file. An agent's every tool call goes through its local
Individuator, which asks the Bosun whether it is allowed; the answer comes back and the file or the
command never leaves the machine. An agent holds no credential of its own, so cutting one off means
the Individuator declines to act for it, and nothing you are using has to be revoked.

## The three seams

A seam is a place where Builder can be split across machines. There are three, and everything above
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

## Adding more machines

The same three seams answer the larger case without changing shape. One Library on a capable
machine serves many people, the Bosun sits beside it or on its own machine, and every machine that
hosts sessions runs an Individuator, including each person's laptop. Everyone reaches their own
sessions through Deck, and Orient gives whoever wants it a view across all of them.

A team's arrangement is therefore the same Builder as a single laptop's, with the parts spread
further apart, which is what putting the seams in these three places buys.

## Where to go next

- **[One account vs. multiple accounts on the server](accounts-on-the-server.md)** covers which
  account Builder runs as on the machine that hosts it.
- **[What you need](what-you-need.md)** covers the hardware, accounts and network.
- **[How Builder works](how-builder-works.md)** shows how the parts fit together.
- **[The glossary](glossary.md)** explains each word Builder uses.
