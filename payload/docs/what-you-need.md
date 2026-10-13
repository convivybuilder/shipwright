# What you need

This page covers the hardware, accounts and network Builder runs on, from the least you need to
start to what you add as you go. Like a bead, which is a project's short description of where it is
going, the page describes Builder as it is designed to work. [Installing Builder
today](installing.md) covers the install itself, as Builder's first public release runs it.

You can start with very little. The first section lists everything a first project needs. Each
section after it adds one thing, and says what that thing is for, so you can stop reading at the
point where your needs stop.

## The least you need

- **Two machines.** This release needs both.
  - **A server**, which runs Builder's backend and every session. It is a machine that stays on and
    stays awake: a Linux machine, a virtual machine in the cloud, or a Mac left plugged in.
  - **A Mac laptop**, which runs Deck, the app you work from. Deck reaches the server over SSH, a
    standard way to open a terminal on another machine.
- **A terminal you are comfortable opening** on each machine. A terminal is a window where you type
  commands, and on a Mac the application is called Terminal.
- **An account of your own on each machine.** Builder installs on the server in one of two shapes,
  and the shape counts only the server's accounts. This release installs only the single-account
  shape, which runs Builder on the server as one account, yours. Deck runs on the laptop as your
  account there, whichever shape the server has. The two-account install comes in a later release.
  It runs Builder on the server under two accounts of its own, separate from yours, and it needs
  the server's administrator password to create them, and again whenever Builder's privileged half
  is installed or updated. [One account vs. multiple accounts on the
  server](accounts-on-the-server.md)
  explains both shapes and what the single-account one gives up.
- **Claude Code, signed in to your Claude account.** Claude Code is the program that lets you talk
  with Claude, an AI model, in a terminal. Every Builder session is a conversation with Claude in a
  terminal. On the two-account install, Builder's two accounts sign in to Claude as well as your
  own, so check that your plan allows three sign-ins, or have a seat for each.
- **A GitHub account, for the two-account install** and for any project you want reviewed. GitHub
  is a website that stores a project's files and their history. The GitHub section below says why
  Builder uses it, and when the single-account install can start without one.

On the two-account install, Homebrew installs anything else Builder needs, and that list is the
whole of it. Homebrew is a free program for the Mac that installs other programs. The single-account
install installs no program itself: it checks each one and names any you need to install.

The next two sections describe the machines as Builder is designed to use them, starting from one.
This release needs both from the start, as listed above. The sections after them cover what you add
when you want to share something you have built. An agent is an AI model given a role and the tools
it may use, and Builder puts agents to work on tasks in your project.

## A laptop on its own

This release does not install this way; it needs the two machines listed above. As designed, a
laptop runs the whole of Builder. Three things run there: the Library, which is where Builder
keeps everything a project knows, your sessions, and the agents they put to work. Deck, the desktop
application where you pilot each project, is on the same machine.

The limit is that your sessions live as long as your laptop is awake. Close the lid and the agents
stop mid-run. That is fine while you are building in bursts and sitting in front of it, and it
stops being fine the first time you want an overnight run.

## An always-on machine, once you want work to continue without you

This release needs this machine from the start; it is the server listed above.

A second machine that stays on and stays awake takes over running the sessions, and your laptop
becomes the thing you drive them from. Work carries on while the laptop is shut, in a coffee shop,
or being restarted.

**A Mac mini is the usual choice.** It is the least expensive Mac Apple sells, it is quiet, and it
is built to sit on a shelf. **An old Mac laptop you do not mind leaving plugged in works as well.**
Set it never to sleep on mains power, close the lid if you like, and it will keep running sessions
with the screen off.

What the machine needs is that it stays awake, stays on the network, and lets you in over SSH. SSH
is a standard way to open a terminal on another machine. How much memory the machine wants depends
on how many agents you intend to run at once.

## Tailscale, to join your machines together

Your laptop has to reach the always-on machine, and you want that without opening a port on your
router to the internet. Opening a port lets anyone on the internet attempt a connection to that
machine, which is a risk you can avoid.

Tailscale is a private network across your own devices. Install it on each machine, sign in with
the same account, and every machine gets a stable address the others can reach, wherever any of them
happens to be. Nothing is published to anyone else.

Builder reaches another machine over SSH, so any working SSH address will do. Tailscale is the one
to use if you do not have such an address already, because the alternatives ask you to open a port
to the internet or to keep both machines on the same network. Deck also reads your local list of
Tailscale machines when you add a host, so the address becomes one you pick from a list. A host
here is a machine Deck connects to.

## A GitHub account

GitHub holds three things for Builder: the review of each change, a copy of your work, and the
identities Builder acts under. This section takes them in turn. Two words come up throughout. A
pull request is a proposed change, packaged so it can be read and checked before it is accepted,
and to merge it is to accept it.

**The two-account install needs a GitHub account, whatever you are building.** The gate that
decides whether a change merges is GitHub's, and the part of Builder that runs reviews installs only
from GitHub.

**The single-account install can start without one**, for work that is not software. You get a
Reference Room, Builder's store of what a project holds to be true, which many systems call a
knowledge base. You also get projects, and you meet no pull request. Adding a GitHub account
later turns on reviews without a reinstall.

**What GitHub holds is review.** A change that someone should look at before it counts becomes a
pull request. Two agents review it, a reviewer and a security reviewer, and checks run against it to
catch a document that has gone malformed. Each reviewer posts its verdict as a GitHub check, a pass
or fail mark on the pull request, and a passing one is called green. A rule on `main`, the project's
current version, lets the pull request merge only when both checks are green. [How Builder
works](how-builder-works.md#review-what-decides-a-merge) says why no agent can post those checks for
itself. On the single-account install the reviewers post their findings on the pull request instead,
and the rule on `main` that you set in the repository's settings on GitHub can require a pull
request and the repository's own automated checks, such as the one that catches a malformed
document. In the merge mode called Enforced it also requires your own approval, which [Connecting
GitHub](connecting-github.md) explains.

**It is also your copy.** GitHub keeps your work off your own disk at no cost, so a failed disk or a
lost laptop takes nothing you cannot restore, and handing someone a link is the same act as keeping
it.

### The three apps

**Builder acts on GitHub as itself, through three GitHub Apps you create on your own account.** A
GitHub App is an identity on GitHub that belongs to a program instead of a person. One belongs to
the Library, one belongs to the Bosun, which is the part of Builder that governs agents, and one,
the approver, posts the review checks. The single-account install has no approver; its agents act
through an App of their own, which [Connecting GitHub](connecting-github.md) creates. A fourth App,
configured in `docs-merge-app.json`, is needed only if you let agents merge documentation, and no
install step creates it yet.

A separate identity buys two things.

- **Work is attributed to whoever did it.** A pull request the Library merged says the Library
  merged it, and on the two-account install, work an agent pushed is attributable to the agent and
  not to you. On the single-account install, sessions push as the agents' App once GitHub is
  connected, so their pushes carry the App's name rather than yours.
- **Each App holds its own narrow permissions.** That is what lets the Library merge into the
  knowledge repository, the repository that holds the Reference Room, without that permission
  reaching anything else. The Library merges there only through `agentctl kb merge`, which permits
  only what your agent policy names, and out of the box that is nothing. The agent policy is a file
  you own that lists what agents may do without you. `agentctl kb merge`, the command the Library
  merges through, reads the policy and refuses anything it does not permit. A merge you start from
  Deck or Orient takes a separate path, through a merge check in the Library, and that check
  approves every merge it is asked about for now, as [What works and what does not yet](install-status.md) says. The
  App's identity is also how `agentctl kb merge` tells a pull request the Library opened from one
  anything else opened.

**The approver's key is the one no agent can read.** It is kept by the Mac's administrator account
and read only by the program that runs a review, so a check from the approver means a review ran.
You create the approver App and give the install its key before the first review; until you do,
Builder refuses to run reviews and says what is missing. The rule that requires its two checks on
`main` is one you add to your GitHub organisation in the browser, because creating it needs an
organisation administrator. As that administrator you are exempt from it, as you are from GitHub's
other rules on `main`.

GitHub calls these **GitHub Apps**, which are a different thing from what it calls OAuth apps. You
create them under your account's developer settings, and Builder's install tells you the
permissions each one needs.

## Somewhere to put the apps you build

Once a crew has built you an app, the app has to run somewhere people can open it. Which of the two
answers you want depends on who has to see the app.

**For anything only you and the people on your own network use, your own machine is the host.** The
app runs on the always-on machine and you reach it over Tailscale from your laptop or your phone.
Nothing is published, and there is nothing to pay for or configure.

**For an app you want to share with people outside that, Cloudflare is the way in.** Cloudflare is a
company whose service stands between the internet and your app. A Cloudflare account and a domain of
your own, which is an address such as `example.com`, will let Builder put an app at its own address,
with a list of who may see it, while the app itself keeps running on your machine. The command that
does this is not built yet. [Your own Cloudflare account](your-cloudflare-account.md) sets that up.

## Where to go next

- **[Getting started](getting-started.md)** takes you from installing Builder to your first crew.
- **[How many machines Builder runs on](where-everything-runs.md)** covers one machine or
  several, and what a second machine buys you.
