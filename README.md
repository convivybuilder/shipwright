# Convivy Builder

**Builder is a way to build software, or any project, with a crew of AI agents that can read what
your project is for, what it has decided, and what has happened so far.** Your first conversation is
with the steward, which asks what you want to build and sets up a crew to build it with you.

An AI agent is an AI model, such as Claude, given a role and the tools it may use, and put to work
on a task. A crew is one project and the agents working on it. You do not need to know more than
that to begin, because the steward explains each part of Builder when your work reaches it.

Builder is free and open source under the Apache 2.0 licence. [Installing Builder
today](payload/docs/installing.md) covers the install itself, as Builder's first public release runs it.

**This repository holds the payload, the part of Builder an install places on your machine: the
skills, the steward's charter, the documentation, the starting knowledge and a backup command. It
also holds the installers that place it.** It describes Builder as designed. Parts of the system it
describes are still being built, and the documentation says so wherever that is true, so you will
not have to discover it yourself.

## Start here

These pages assume you have never seen Builder, and each one explains its terms as it goes.

- **[Why Builder](payload/docs/why-builder.md)** explains what goes wrong when people build with AI today,
  and what a different shape would have to do about it.
- **[How Builder works](payload/docs/how-builder-works.md)** explains the model, and where things are kept.
- **[Getting started](payload/docs/getting-started.md)** shows what a first session looks like.
- **[What you need](payload/docs/what-you-need.md)** lists what has to exist before you begin.
- **[Glossary](payload/docs/glossary.md)** gives the words this project uses and what they mean.

## The idea in one sentence

**Everything is memory, except canonical knowledge, and memory is where project structure happens.**

That sentence uses two terms. Canonical knowledge is what your project holds to be true, such as its
goal and its decisions. Memory is a record of anything that happened, and that includes the plan, the
list of work and who is doing what.

Most tools split these apart. A ticket tracker, the tool many teams use to list their work, keeps the
plan in one store and the reasoning that produced it in another. A pull request description, the note
attached to a proposed change, keeps that reasoning somewhere an AI model cannot retrieve. Put both
in memory and the context that makes the next piece of work good is reachable when it is needed.

Some of this will not survive contact with the world. The confidence is in the direction, and less
in every part of it.

## What is here

| path | what it is |
|---|---|
| `skills/` | the skills, which are sets of instructions the steward uses to create a crew, a sub-crew, and a project's bead, its short description of where it is going |
| `steward/CHARTER.md` | the role an adopter's first session plays |
| `knowledge-seed/` | the starting knowledge for your knowledge repository, and the machine-wide instructions every session reads |
| `bin/builder-backup` | the command that backs up the Library and the knowledge repository |
| `docs/` | the documentation, including the case for using Builder at all |

## Licence

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Apache-2.0 places obligations on people who redistribute the software, and none on people who use
it. Installing and running Builder puts no licensing burden on you or your employer.
