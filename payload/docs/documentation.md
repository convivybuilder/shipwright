# Documentation

These pages cover installing Builder and doing particular jobs with it. Like the rest of this site,
they describe Builder as it is designed to work.

Every page assumes you are new to Builder and explains its terms as it goes. If a word stops you,
[the glossary](glossary.md) has it. If you want the reasons behind Builder before the steps,
[Why Builder](why-builder.md) is the place to begin.

## Getting started

Start with the first two.

- **[What you need](what-you-need.md)** covers the hardware, accounts and network Builder runs on.
- **[Getting started](getting-started.md)** takes you from installing Builder to your first crew.

## Installing

Start with the first page. It sends you to one of the next three, and each of those ends at the
fifth.

- **[Installing Builder](installing.md)** explains the server-and-laptop layout Builder is built for
  and the words the install uses, shows how to clone Builder's repositories, and says what to do
  when a step refuses.
- **[Installing on Linux, with administrator access](install-linux.md)** is the install for a Linux account that can install software
  for the whole machine.
- **[Installing on Linux, without administrator access](install-linux-without-sudo.md)** is the install for a Linux account someone
  else administers.
- **[Installing on a Mac](install-mac.md)** is the install for any Mac.
- **[After the install](after-installing.md)** shows what the install put where, how to move to a
  later release, and how to meet the steward, and covers backups.
- **[What works and what does not yet](install-status.md)** lists what release 0.6.0 has been seen
  doing on each test machine, and what it cannot do yet.

## Guides

Each guide covers one job, and you can read any of them on its own once Builder is installed.

- **[Customizing Builder](customizing.md)** names each document that decides what your agents do,
  and walks through one change to each.
- **[Forking Builder](forking.md)** covers installing from your own copy of Builder's repositories,
  and choosing which of Builder's later changes to take.
- **[Connecting GitHub on the single-account install](connecting-github.md)** gives your agents a
  GitHub identity of their own, and lets GitHub refuse to merge a pull request an agent opened
  until you approve it.
- **[The Slate](the-slate.md)** is where a crew leaves the questions it needs you to answer, and
  where you keep notes to send it at a break point.
- **[Your own Cloudflare account](your-cloudflare-account.md)** prepares a Cloudflare account and
  domain of your own, so you can share an app with the people you name.

## Reference

These pages explain how Builder is put together, for when you want to understand a part of it.

- **[How Builder works](how-builder-works.md)** shows how the parts fit together.
- **[How many machines Builder runs on](where-everything-runs.md)** covers one machine or several,
  and what a second machine buys you.
- **[One account vs. multiple accounts on the server](accounts-on-the-server.md)** covers which
  account Builder runs as on the machine that hosts it, and what each choice gives up.
- **[The glossary](glossary.md)** explains each word Builder uses.

## From the author

Builder's author writes these pages by hand.

- **[Tips from Builder's author](jays-tips.md)** collects advice on working with Builder day to day.
- **[On the horizon](on-the-horizon.md)** describes what Builder will do next.
