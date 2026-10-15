# Choosing a tool

This page helps you choose among the tools for building software with AI agents, Builder among them,
by where you are and what you want to do. It describes each kind of tool fairly, says what Builder
asks of you, and names the cases where another tool will serve you better.

An agent is an AI model, such as Claude, given a task and the tools to carry it out. It reads files,
runs commands and changes code. Every tool on this page runs agents, and they differ in what they
arrange around them.

The details of the other tools come from their own websites and repositories, read in October 2026.
These products change quickly, so check a tool's own pages before you choose it. The
[sources](#sources) are listed at the end.

## Four questions that sort the options

1. **Do you want your projects' decisions, plans and history kept where an agent can reach them,
   across several projects, over months?** Builder is built around that problem. Gas Town, the tool
   closest to it, tracks the tasks a large group of agents works through.
2. **Do you want more agents working at once on code you already direct?** A workbench that runs
   several agents side by side may be all you need.
3. **Do you want another company to run your agents for you?** A hosted agent service runs them on
   its own infrastructure and connects them to your team's tools.
4. **How much do you want to run yourself?** Some of these tools are an app you open, and others are
   a service another company runs. Builder is a small system that runs on a machine of yours.

## Orchestrators that track the work

**[Gas Town](https://github.com/gastownhall/gastown) is the tool closest to Builder.** It is an
open-source system that runs on your own machine, on macOS or Linux or on Windows through WSL, and
coordinates many coding agents at once. Its author describes it working with twenty to thirty agents concurrently. You talk to a
coordinating agent called the Mayor, which groups work into batches called convoys and hands each
task to an agent. Other agents watch the workers, and a merge queue keeps workers from changing the
main line of the code directly. It drives Claude Code by default, and can drive Codex, Gemini,
Cursor, GitHub Copilot and several others.

Gas Town keeps its work in [Beads](https://github.com/gastownhall/beads), a tracker built for
agents. Beads stores tasks as a graph of items and the dependencies between them, in a database kept
under version control, so an agent can ask what is ready to work on and pick up where another left
off after a restart.

**Gas Town and Builder start from the same observation.** Agents lose context between sessions, so
the work has to be recorded where they can reach it. Each is built for a different end.

- **Gas Town is built for throughput.** It keeps many agents busy on a project's code, and it
  records the tasks and the dependencies between them.
- **Builder is built to keep you and your agents aware of where each project stands, across many
  long-lived projects at once.** It keeps each project's goal, decisions and history along with its
  tasks, and gives each session the part it needs, so every piece of work starts from the
  project's current state and heads for its objective. Each project has its own crew, a small team
  of agents with one session you talk to, and a session called the steward starts new crews for
  you. You can leave a project for weeks, and when you come back, you and its crew both know where
  it stands. That matters most to someone who works on many projects at once, whether they write
  code or not.

**Builder aims to be methodical at pace.** It keeps each piece of work on track toward the
project's objective, and a project that stays on track finishes sooner than one whose work drifts
from the goal, reopens settled decisions, or has to be done again.

**Choose Gas Town if** you are an experienced developer who already runs several agents, and you
want more of them working at once on code, with the tasks between them tracked.

**Choose Builder if** you run several long-lived projects and want each to move steadily toward its
goal, with you and its agents working from the same picture of where it stands.

## Agent workbenches

**These tools run several coding agents in parallel on one project and let you compare what they
produce.** Most give each agent its own git worktree, a separate working copy of the project, so the
agents do not overwrite each other's changes. You stay at the keyboard, choose the tasks, and pick
which result to keep. Most of them drive agent programs you already use, such as Claude Code or
Codex, under your own subscriptions.

Warp, which makes one of them, calls this kind of tool an agentic development environment, or ADE,
and defines it as a development tool built around agents as first-class participants.

- **[Orca](https://github.com/stablyai/orca)** is an open-source desktop app for macOS, Windows and
  Linux that runs many command-line agents in parallel worktrees and helps you compare and merge
  their results.
- **[Conductor](https://www.conductor.build/)** is a Mac app that runs Claude Code, Codex and Cursor
  agents in parallel, each in its own worktree. Its paid plans add workspaces in the cloud.
- **[Claude Squad](https://github.com/smtg-ai/claude-squad)** is an open-source terminal app that
  manages several agent sessions at once.
- **[Sculptor](https://imbue.com/sculptor)** is a desktop app that runs each agent in its own
  container, an isolated environment on your machine.
- **[Warp](https://www.warp.dev/)** is a terminal rebuilt around agents, and it can run agent
  programs such as Claude Code inside it.

**Choose one of these if** you are a developer who wants more done in an afternoon on code you
understand, and your plan and decisions already live somewhere you are happy with. They are quick to
start, and you can stop using one without moving anything.

**They leave everything outside the code to you**: why a change was made, what was decided last
week, and what comes next. That stays in your head, your tracker and your notes, and an agent sees it
only when you paste it in.

## Hosted agent services

**These services run agents on their own infrastructure and connect them to the tools your team
already uses.** You assign work from a tracker, a chat channel or a web page, and an agent returns a
pull request, a proposed change for someone to review and merge.

- **[Factory](https://factory.com/)** offers agents it calls Droids, for coding and for the work
  around it, such as triaging incidents and reviewing pull requests. It connects to GitHub, Jira,
  Linear, Slack and many other services, and offers single sign-on and administrator controls for
  companies. Its agents can run in Factory's cloud, on your own infrastructure, or a mix of the two.
- **[Devin](https://devin.ai/)**, from Cognition, is an agent that runs in the cloud or on your
  machine, tests its work in its own browser, and hands back a pull request.
- **[Cursor's cloud agents](https://cursor.com/help/ai-features/background-agents)** each work on
  their own virtual machine and hand back a pull request.
- **[Codex](https://developers.openai.com/codex)**, from OpenAI, runs as a program on your machine
  and in OpenAI's cloud.

**Choose one of these if** you want another company to run your agents, and your company needs the
controls a business service offers. They are paid services, so compare their pricing with what
running agents yourself would cost.

**Your team's tracker can stay where it is with Builder.** Builder keeps each project's plan inside
the system, where the project's agents can reach it when they need it. A tracker such as Jira can
go on holding your organisation's work beside it.

## Between the two

**[OpenHands](https://github.com/OpenHands/OpenHands)**, whose control centre is called Agent
Canvas, is open source and runs on your own machine or infrastructure, and it also has a hosted
version. It runs its own agent or others, such
as Claude Code, Codex and Gemini, several at once, and can give each its own container. It suits a
team that wants the kind of agent a hosted service offers, kept on machines the team controls.

## Where Builder fits

**Builder is for someone who wants each project's goal, decisions and plan kept where the agents can
reach them**, and who expects to run several projects that way over months. You talk to a crew's
session in plain language, and it keeps the project's records as it works. Builder is written for
engineers and for people who have never written a program, and an engineer can check every claim it
makes. Its sessions run in Claude Code today, on Anthropic's models or, through a model gateway
Builder installs, on models from other companies. [Why Builder](why-builder.md) gives the full case.

Builder asks for more setup than a workbench:

- **You need a server and a Mac.** The server, a Linux machine or a Mac that stays on, runs Builder's
  backend and every session. Deck, the app you work from, runs on a Mac.
- **You need some patience.** Builder is early. Its first public release came out in October 2026,
  and parts of it will change as people use it. [What works and what does not
  yet](install-status.md) lists what has been seen working.

**Another tool will probably suit you better if:**

- you want to speed up work on one repository this afternoon, which a workbench does;
- you want another company to run your agents, which a hosted service does;
- you need the server to run Windows, or need single sign-on and administrator controls.

**Builder may fit if:**

- you have explained the same decision to an agent more than once;
- you lose track of why something was done, and so do your agents;
- you want to start several projects, each with its own agents, without holding all of them in your head.

[What you need](what-you-need.md) covers the hardware and accounts in full, and [Installing
Builder](installing.md) covers the install.

## Sources

Each source was read in October 2026.

- Orca: [github.com/stablyai/orca](https://github.com/stablyai/orca)
- Conductor: [conductor.build](https://www.conductor.build/) and its
  [pricing](https://www.conductor.build/pricing)
- Claude Squad: [github.com/smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)
- Sculptor: [imbue.com/sculptor](https://imbue.com/sculptor)
- Warp and the term ADE: [What is an agentic development
  environment?](https://www.warp.dev/articles/what-is-an-agentic-development-environment)
- Gas Town: [github.com/gastownhall/gastown](https://github.com/gastownhall/gastown)
- Beads: [github.com/gastownhall/beads](https://github.com/gastownhall/beads)
- Factory: [its connectors](https://factory.com/product/connectors), [its page for software
  companies](https://factory.com/industries/saas) and [its launch
  announcement](https://factory.com/news/ga)
- Devin: [devin.ai](https://devin.ai/)
- Cursor's cloud agents:
  [cursor.com/help/ai-features/background-agents](https://cursor.com/help/ai-features/background-agents)
- Codex: [developers.openai.com/codex](https://developers.openai.com/codex)
- OpenHands: [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)
