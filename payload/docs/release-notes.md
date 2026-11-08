# Release notes

This page says what changed in each release of Builder, newest first, for anyone deciding whether to
install it or move an existing install to a later release. [After the install](after-installing.md#moving-to-a-later-release)
shows how to move.

## 0.7.0, 2026-11-02

### Installing

- **The one command now installs what it can, rather than only naming it missing.** It installs
  `git`, Python 3.11, Claude Code and, on a Mac, `tmux` — with `apt-get` on Linux given `sudo`, with
  Homebrew on a Mac, bootstrapping Homebrew itself when an administrator is at the keyboard — and
  still names whatever it has no route to install: an account with no administrator rights and no
  Homebrew already there, and signing in to Claude Code, which stays a person's own act.
- **`~/.local/bin` is now on PATH for a bare command run over ssh, not only for a session at a
  prompt.** The install adds a line to `~/.bashrc` (bash) or `~/.zshenv` (zsh), the file each reads
  for a non-login command, since `~/.profile` and `~/.zprofile` only run for a login shell. Without
  it, a tool that runs a Builder command by bare name over plain, non-login ssh could not find it. The line also ends with `/opt/homebrew/bin`, so on a Mac that same command finds Homebrew's `tmux`.
- **The install now creates Deck's credential**, `~/.orient-control/deck-library-token`, which Deck
  approves, declines and sets a model with. Without it those three failed on a fresh install. This
  form of the credential is temporary: a later release takes those three acts away from it, and each
  will need its own Touch ID press in Deck.
- **Orient's Writing Desk now finds draft posts on a fresh install.** The Library shows a draft
  only to a credential holding `signal.post_draft`, and the install now grants it to Orient's
  approved-client credential, `~/.orient-control/library-client-token`. An update grants it to an
  existing install's credential too, by replacing that credential once.
- **Builder's releases are signed, starting with this one.** `release-signers` now carries the key
  that signs each release's manifest, held in a Secure Enclave that cannot export it and confirmed
  for every signature. Run `builder-install --verify 0.7.0` to check a release yourself: it checks
  the manifest's signature against that key, each of the six clones' commit against what the
  manifest names, and the published archive's sha256, fetching the manifest and signature itself
  when you point it at nothing. The one-line install from the site now runs the same check before
  any installer, including when it installs 0.7.0. The Homebrew copy is the installer packed in the
  0.7.0 archive, which predates that check, so after a Homebrew install run `--verify` yourself.
- **An install can now add a crew.** The install had no credential that could write the crew
  registry, so `agentctl crew register` and the steward's `new-crew` refused on every install. The
  Library now mints `agent-platform-registry-writer-token`, which can do that and nothing else, on
  a fresh install and on an update.
- **Builder gets an updater.** `builder-update --shape single` reports what moving to a later
  release would do, asks you to confirm, then stops every job, snapshots the database, installs the
  release, starts everything again and checks itself before it exits, putting everything back on any
  failure; `--rollback` finishes an update that stopped partway. It checks the target release the
  same way `--verify` does, using the trust list already on the machine, so an install made before
  this release still has no key to check against. `--shape two` and `--shape three` both refuse for
  now; only the single-account shape moves.
- **`install-jobs` can report, stop and start jobs by hand** (`--running`, `--stop [LABEL...]`,
  `--start LABEL...`), the piece the updater above uses to stop everything before it moves a release
  and start it again after.
- **The installers take a release explicitly.** Pass `--release vX.Y.Z` to `install-backend` or
  `stand-up-backend`, or a release tag to `install-payload`, and each resolves and checks out exactly
  that tag rather than always tracking `main` or `stable`.
- **Builder gets an uninstaller for every account shape.** `bin/uninstall-builder` already removed a
  single-account install; this release teaches it to remove the two-account and three-account shapes
  too, each fully and unit-tested, including the knowledge index the `agents` account's own
  `knowledge-autopull` job writes into that account's home on both shapes. `stand-up-backend --shape
  two` itself still refuses until that shape is finished, so there is no complete two-account install
  yet to remove.
- **What was called the two-account install is now the three-account install**, since the count now
  includes you, the operator. The name that takes its place — a plain `agents` account with no
  separate reviewers — is real in the account and root-install tools, but `stand-up-backend --shape
  two` still refuses until the rest of it is built.
- **`builder-install --shape three` runs every step of the three-account install in order**, tested
  against throwaway roots and stub account tools; nobody has yet run it on a real machine. It checks for
  administrator rights and a supported server platform (Debian 12, Ubuntu 22.04 or macOS 26) before
  changing anything, then runs `provision-accounts` and `install-privileged` as root, from a
  root-owned copy of the release extracted to `/opt/builder/src/shipwright@<sha>`. It then clones the
  release again, as the `agents` account into its own home, and re-verifies that clone against the
  same signed manifest before anything reads it: `install-payload` and `stand-up-backend --shape
  three`'s own placement step both need a real git checkout to resolve their source from, which the
  root-owned tree does not carry, so both run from the `agents` clone instead. `--shape two` still
  refuses.
- **The one-command server install creates your GitHub App itself**, as its last step, rather than
  leaving that for afterward: open the address it prints and click **Create GitHub App**, or paste
  the redirect's address at the terminal over SSH. `--no-github-app` skips it.
- **The single-account install's Enforced merge mode is gone.** Instruction only remains, where your
  agents' own instructions are what stops them merging; Deterministic, where GitHub itself refuses an
  agent's merge, is designed and documented but still waits on a rehearsal.
- **Every service's Python dependencies install from a hash-locked lockfile.** `install-backend`
  installs each repository's dependencies with `pip install --require-hashes --no-deps --only-binary :all:`
  against that lockfile, rather than its plain `requirements.txt`, so an install never puts in place
  a package whose hash doesn't match the one the lockfile pins.
- **`install-payload` refuses a local branch that's behind its own origin.** Pointed at a `--ref`
  naming a local branch, it now fetches and compares first, rather than installing whatever that
  branch last happened to hold.
- **Each install now has its own configuration repository.** Setting up the backend creates
  `install` inside the Builder root, a git repository with no remote, separate from the clones an
  update replaces, for an install's other non-secret configuration.
- **A crew, product or person an install registers is user data.** It lives only in that install's
  own configuration and knowledge base, never in a Builder release, so the release build carries no
  scan for those names.
- **The laptop install sets up the ssh config Deck's crew sidebar reads**, using the tool in the
  `agent-platform` tree it fetches beside Deck, so the sidebar is no longer empty after a laptop
  install. The tool needs three things set up on the laptop first: the server's private-network
  address in the laptop's operator config, an ssh host alias for the server, and a mounted share
  of the account that runs your crews. When one is missing, Deck is installed anyway, the install
  finishes and names what is left, and running it again is safe.
- **The knowledge index is no longer silently empty after a fresh install.** `agentctl kb sync` asks
  the Library for the project registry over HTTP, so running it before the Library was serving
  refused every document and left the index at 0 docs, with no retry. `stand-up-backend` and
  `builder-update` now run it once the Library is answering, with `bin/sync-knowledge-index`.
- **`provision-backend` also installs `bubblewrap` and `socat` on Linux**, which a dispatched
  session's sandbox needs; without them a session refused to start with `sandbox required but
  unavailable`. The three-account install now runs it too.
- **Each crew gets its own work-queue credentials.** The work-queue tools now present the crew's
  own credential and have no shared one to fall back on. The install and every update mint a pair
  for each registered crew, `new-crew` mints one for a new crew, and `mint-crew-ops-credentials`
  does it by hand.
- **A dispatch now starts on an install with no GitHub.** It used to stop asking for a GitHub App
  that install never had, and for a Library credential at a path the install does not use.

### The Bosun

- **A usage hold now follows an account switch.** It used to keep reading the account you switched
  away from, holding every dispatch until that account's own usage window reset. Each run now records
  which account it bills, and a held run re-checks every five minutes, so a switch releases it within
  one interval.
- **Codex's own ChatGPT-subscription usage gets its own ledger lane**, so it is never summed with
  Claude's subscription usage into one spending figure.
- **The daily run digest also flags** a run whose reservation was reaped while it was held, and one
  whose GitHub token failed to re-mint after a hold; both used to pass through unflagged.
- **A run's cost now always reaches the spend ledger when it finishes, dated to the day it actually
  finished.** It used to sometimes go missing.

### Agents

- **A killed run's work-item lease is released too.** Only a run that finished on its own used to
  release the lease it held; a run that was killed left its work item stuck checked out.
- **GitHub tokens are minted from one place for every verb**, with a log of every mint that only you
  can read. The same change fixed a detached `agentctl spawn` segfaulting while minting its token, and
  `pr-ready`/`auto-ready` losing the grant they need partway through an outage.
- **A dispatched run's sandbox is tighter.**
- **Reviewers run under their own allow-list**, separate from a coder's.
- **`agentctl spawn --trial` keeps a trial run's own commits and pull-request text out of the context
  its own model reads.**
- **`kb_update` and `kb_create` now write when the Library has no index row yet for the document**,
  rather than refusing; the Library can also reclaim a checkout a dead session left behind instead of
  refusing on it.
- **The model gateway pins LiteLLM and DeepSeek's billing rate**, so a reasoning reply's thinking
  block shows again and DeepSeek is billed at its real peak rate; each model also reports its real
  Claude Code context window.
- **Claude Sonnet 5.5's cached token reads are now billed at their real rate**, $0.10 per million
  tokens.
- **A coder can be dispatched on Claude Haiku 5.5**, with `agentctl spawn --model haiku-5-5`.
- **A dispatched run can build a Swift package.**
- **`agentctl close-orphaned-runs` closes only the runs you name, and records why each one died**,
  rather than closing runs beyond the ones you gave it.
- **A run that died before its process id was recorded now reads as dead**, instead of stuck.
- **A run's own record stays in place while the dispatch that started it is still finishing**,
  instead of appearing to vanish for a moment.
- **A declined work item no longer counts toward the issues still waiting.**
- **A run's facts include the review verdict that was posted, and which pull request it went to.**
- **A reviewer's verdict posts to the pull request from your own GitHub App**, rather than from
  whichever token happened to run the review.
- **`agentctl spawn --pr N --review-sha S` pins a review to one specific commit of the pull
  request**, rather than always its latest.
- **`new-crew`'s registration step now tells the agent to pass a crew's home directory relative to
  the Builder root**, rather than an absolute path the projects registry would refuse.
- **Builder no longer creates child sessions under a crew.** `new-subcrew` now refuses and sends the
  request to `new-crew` instead; `new-crew` leaves a new crew's session list empty. Grouping related
  crews is now a Deck feature, unrelated to session names.
- **A crew's session now starts on a Linux server where tmux is not yet running.** `session-agent
  start` starts tmux itself there. It called macOS's `launchctl` before, so a session could not
  start on a fresh Debian install. macOS is unchanged.
- **`rollover`, `handoff-pickup` and `handoff-leave` ship as installed skills.** `install-payload`
  links all three, so a session handing work off always finds its counterpart installed.
- **`handoff-leave`, `handoff-pickup` and `write-bead` stop describing queue drains.** Scheduled
  autonomous crews are retired permanently, so nothing drains the work queue; the skills now say a
  released claimed item returns to `open`, where any session can take it, and `write-bead` describes
  the interrupt lane without an autonomous crew draining it.
- **`apps_crew` is a new, optional operator-config key**, documented in `agent-platform`'s
  `config/operator.example.json`. `knowledge.py` reads it with `operator_config.get_optional()`,
  which returns `None` when the key is absent, so an install with no apps crew leaves it out.

### The Library

- **The projects registry is now one table in the Library, never a file on any machine.** The
  install seeds that table once, carrying forward any crews an earlier release registered in its
  registry file. After that, a crew registers over `POST /registry/crews` and every reader asks the
  Library for `GET /registry` instead of reading a local copy. Reading it needs a `registry.read`
  credential: a new `agent-platform-registry-reader` token, and Orient's own agent token now
  carries the grant too.
  An install updated from before this release had an Orient token minted without that grant, since
  the mint that adds it only ever ran once; the update now re-grants it, and mints the missing
  reader token, the first time it runs on such an install.
- **`kb apply` checks with the Library's admission endpoint before committing a document write, and
  a brand-new document needs no checkout to create.**
- **An agent joins the Library's roster automatically once its definition is served from the
  knowledge tree**, with no separate registration step.
- **`root-ca enroll <host>` pulls a new machine's certificate request over SSH, signs it once you
  confirm, and registers the machine**, instead of a manual certificate exchange.
- **The Library's mutual-TLS listener can bind a remote address as well as loopback**, for a server
  reached from another machine; its plain listener now refuses to bind anywhere but loopback.
- **A draft Writing Desk post is readable only by an identity Orient has granted a draft-reading
  capability to**, rather than by anyone who can already read posts in that product.

### Orient

- **A known limit: a fresh install has no way to log in to Orient's pages.** Orient learns who a
  visitor is from Cloudflare Access or from its tailnet listener, and the install sets up neither, so
  it refuses every page. The command that will set this up is not built yet.
- **A project's page now shows its live Course and epics**, its changelog and release notes, and its
  recent knowledge-document commits, each scoped to who may see it.
- **Two pages are new: a project list and past runs**, both reachable from navigation, and
  **/model-comparison**, finished runs grouped by agent and model.
- **/tech-debt is rebuilt on the Library's own corrections queue.**
- **A page served from a saved copy now says so**, with a visible banner, rather than looking
  current.
- **Project tables show the display name and aliases from your own install's registry**, rather
  than a fixed list.
- **A proposed epic can be declined or re-proposed.**
- **Writing Desk posts and their revisions copy into the Archives**, including a post with no
  recorded author.
- **A ledger shows its subscription lane beside its gateway total**, instead of just one of the
  two.

### Deck

- **The cockpit lists a project's sessions alongside its dispatched runs**, each with its own
  working-on line, falling back to its last dispatch when there is nothing newer — and that line no
  longer names a bare work-item id.
- **Each epic shows its reference key beside its title.**
- **The right column's tabs are now ordered Cockpit, Slate, Shell, Local.**
- **The pre-install check and the installer both run through your login shell**, and Deck no longer
  trusts a stale SSH connection that only looks alive.
- **The cockpit can decline a proposed epic directly.**
- **The cockpit's Sessions panel shows who is attached to each session.**
- **Closing anything opened from the cockpit returns you to what opened it.**
- **Served crews now list in the same order on the rail and in Settings**, instead of two
  different orders.
- **Unpinning a served crew keeps it unpinned**, and a running crew that isn't pinned stays listed
  under START rather than moving to Other Sessions.
- **The START picker's popover now draws on Builder's own background.**

### This site

- **[An install checklist](install-checklist.md)** lists every step a person does by hand, across the
  whole install, as one page of checkboxes.
- **[Supported setups](supported-setups.md)** lists the operating systems, processors and account
  shapes Builder installs on.

## 0.6.3, 2026-10-16

### The Library

- **The cold-tier mover waits out a busy Library rather than failing.** The mover is the job that
  moves old signals out of the Library's main database into its cold one. When the Library was
  writing at the moment the mover tried to start a batch, the mover's pass could end with a
  "database is locked" error. It now retries for a bounded time, so a pass that meets a busy
  Library finishes once the write is done.

### Jobs

- **The `ci-result-fetch` job is gone.** It ran a script the Library no longer has, so a machine
  that turned it on would see it fail on every run. A fresh install never started it. Moving to
  this release does not remove a copy you turned on yourself, so turn that copy off.

## 0.6.2, 2026-10-15

### Installing

- **A Mac can install with Homebrew.** `brew install convivybuilder/tap/builder` installs Builder's
  installer, pinned to this release, along with Python 3.11 and `tmux`. Then run `builder-install`,
  or `builder-install --role laptop` on the laptop you work from. Each release now updates the
  Homebrew formula, so `brew upgrade` brings the installer to the newest release.
  [Installing Builder](installing.md) gives both the Homebrew and the one-line `curl` install.
- **The laptop install asks only for what Deck needs**: `git`, Python 3.11, and `swift` from Apple's
  Command Line Tools. It used to refuse a laptop without Claude Code or `tmux`, which only the server
  runs.

### Spending limits

- **The Bosun now enforces both of a project's spending limits.** The Library decides what each
  project may spend. When a project crosses its soft limit, the Bosun refuses to start an agent for
  any of that project's work items and records why, so `agentctl status` says the limit stopped it rather than
  something else. When a project crosses its hard limit, each agent already running on that project
  ends its run once it notices. A running agent checks no more often than once every 20 seconds,
  and only between steps, so it can take several more steps, or finish a long command such as a build, before it
  stops.

### Work items and the Course

- **A work item filed under the wrong project can move**, with everything under it and all of its
  history. Before this release it had to be closed and filed again.
- **A re-approved epic returns to its old place on the Course** rather than the end, when nothing but
  new epics has moved since it was demoted.
- **A work item can carry a short description**, of up to 25 characters, for places with no room for
  a title, such as Deck's compact view of the Course.

### Orient

- **Each page shows only the projects its viewer may see**, and a viewer who may see none gets a page
  that says so.
- **A table in a Reference Room document can be edited as it appears**, cell by cell, the way a paragraph
  can. The Reference Room holds your project's canonical knowledge; many systems call it the
  knowledge base.
- **Build-plan documents in the Reference Room can be browsed.**

### Agents

- **A run ends with every process its agent started**, so nothing an agent left running in the
  background outlives the run.
- **A crew's repository can live under a GitHub owner other than your main one.** An agent working
  in it gets its GitHub token from your GitHub App's installation on that owner.

### This site

- **[Choosing a tool](choosing-a-tool.md)** is new. It compares the tools for building software with
  AI agents, Builder among them, and is linked from the top of every page.

## 0.6.1, 2026-10-13

These notes begin with 0.6.2. GitHub shows every change 0.6.1 made to the installer and the
documentation in [a comparison of the two releases](https://github.com/convivybuilder/shipwright/compare/v0.6.0...v0.6.1).

## 0.6.0, 2026-10-10

The first public release.
