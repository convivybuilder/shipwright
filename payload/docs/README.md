# Convivy Builder

Builder is a way to build software, or any project, with a crew of AI agents that can read what
your project is for, what it has decided and what has happened so far. Your first conversation is
with the steward, which asks what you want to build and sets up a crew to build it with you.

An AI agent is an AI model, such as Claude, given a role and the tools it may use, and put to work
on a task. The steward is the first one you meet, and it explains each part of Builder when your
work reaches it, so you can start without having written a program before.

Builder is free and open source, under the Apache 2.0 licence. Its first public release, 0.6.0, is
out, and [Installing Builder](installing.md) takes you through installing it. The rest of this site
describes Builder as it is designed to work.

## Install Builder

Builder runs its sessions on a server that stays on, and you work from Deck on your laptop.
[Installing Builder](installing.md) explains that layout and how to clone the repositories, then
sends you to the page for your server:

- **[Installing on Linux, with administrator access](install-linux.md)**
- **[Installing on Linux, without administrator access](install-linux-without-sudo.md)**
- **[Installing on a Mac](install-mac.md)**

Builder's source is public, in the [convivybuilder organisation on
GitHub](https://github.com/convivybuilder): [shipwright](https://github.com/convivybuilder/shipwright),
[agent-platform](https://github.com/convivybuilder/agent-platform),
[library](https://github.com/convivybuilder/library),
[convivy-orient](https://github.com/convivybuilder/convivy-orient),
[convivy-deck](https://github.com/convivybuilder/convivy-deck) and
[write-better](https://github.com/convivybuilder/write-better).

## Start here

These pages assume you have never seen Builder. Read them in this order if you are new, or go
straight to the one you need.

- **[Why Builder](why-builder.md)** explains what goes wrong when people build with AI today, and
  what Builder does about it.
- **[Choosing a tool](choosing-a-tool.md)** compares the tools for building software with AI
  agents, Builder among them, and names the cases where another tool will serve you better.
- **[Tips from Builder's author](jays-tips.md)** collects advice on working with Builder day to
  day.
- **[Glossary](glossary.md)** explains, one at a time, the words Builder uses.
- **[How Builder works](how-builder-works.md)** shows how the parts fit together.
- **[Documentation](documentation.md)** covers getting started and guides for particular jobs.
- **[Customizing Builder](customizing.md)** shows how to change what your agents are told and
  what they may do.
- **[Forking Builder](forking.md)** shows how to run your own copy of Builder and take its later
  changes by choice.
- **[On the horizon](on-the-horizon.md)** describes what Builder will do next.
