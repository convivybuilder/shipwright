# Connecting GitHub on the single-account install

On the single-account install, Builder runs as your own account, and its agents still reach GitHub
under an identity of their own: a GitHub App you create, which is an identity on GitHub that belongs
to a program instead of a person. Every pull request an agent opens, every push and every review
comment then shows the App's name rather than yours. You keep your own GitHub account on your phone
or another computer, and merge by hand from there after reading the change and the reviewers'
findings. Like the rest of this site, this page describes Builder as it is designed to work.

## Why the agents need their own identity

On the single-account install, every agent session can read everything your account holds. If your
GitHub login is on the machine, an agent can act on GitHub as you: approve a pull request, or merge
one. GitHub cannot tell that agent from you, so no rule on GitHub can stop it.

Move the agents to an App, take your own credential off the machine, and that changes. The App has
only the permissions you gave it when you created it. It can push branches, open pull requests and
comment, and it cannot change the rules on your repositories. GitHub knows the App is not you, so a
rule on GitHub can let you merge and refuse the App.

## The two merge modes

You choose how firmly the rule that only you merge is held.

**Deterministic.** GitHub holds it. Each repository's `main`, the project's current version, carries
two rules. The first requires a pull request and the automated checks you name, and refuses deleting
`main` or rewriting its history, for everyone. The second restricts every change to `main` to you
alone, merging through a pull request. The agents' App can push branches, open pull requests, review
and comment, and GitHub refuses its merge. You merge by hand on github.com, from a phone or another
computer, at the change you read; no review is required, so you merge each pull request yourself
rather than setting it to merge on its own when its checks pass. If this machine is your only
computer, that means merging on github.com from your phone, since your own GitHub login must never
be on a machine where agents run.

**Instruction only.** The agents' App can merge, and the instruction every agent carries is what
stops it. The rule on `main` requires a pull request and the automated checks you name, and nothing
more, so the agents' App could press merge and GitHub would admit it. Choosing this mode is choosing
to let the App merge, and leave the rest to the agents' instructions and to you merging by hand after
reading the change and the reviewers' findings. You still gain an identity for the agents' work, and
credentials that last an hour and reach only the repositories you installed the App on.

Deterministic is the recommended mode. Its setup steps join this page when it ships, once GitHub has
been shown to refuse every way the App could reach `main`; the steps below set up Instruction only.

## Before you start

You need the install from [Installing Builder](installing.md), a GitHub account of your own,
the repositories your crews work in, and the GitHub CLI, the `gh` command agents open pull requests
with. Install it with `brew install gh` on a Mac or `sudo apt-get install gh` on Debian or Ubuntu,
and don't sign in to it: step 2 gives it the App's identity. Run every command below in a terminal on the machine
Builder runs on, as your own account.

## 1. Create the App

**The one-command server install already did this**, as its last step, pausing there for you to
click **Create GitHub App** in a browser. If you installed with `curl | sh` or `bin/builder-install`
on the server, skip to **Install the App on your repositories**, below.

Run the command yourself when you installed step by step rather than with the one command, when
the install skipped this step (`--no-github-app`), when you want the
App under a GitHub organisation rather than your own account, or to create it later. It never
replaces an existing key.

```bash
python3 ~/src/shipwright/bin/create-github-app
```

It prints the address of a page on this machine. Open it in a browser signed in to your GitHub
account and click **Create GitHub App**. The page fixes the App's permissions before GitHub shows
them, so you only confirm: it can read and write repository contents and pull requests, read checks
and Actions, and never change a repository's settings or rules. Add `--org <name>` to create it
under a GitHub organisation rather than your own account.

GitHub then sends the browser back to this machine with a one-time code, and the command stores the
App's id and private key in the `github-app` folder of Builder's configuration directory, the key
readable by you alone. It never replaces a key that is already there.

This App cannot change your workflow files: GitHub refuses any push from it that touches
`.github/workflows`, so you edit those yourself. That does not put your checks out of the agents'
reach. A CI job that runs a script from your repository runs the copy in the pull request, so an
agent can change what that job does, and any secret the job passes to that script reaches the
changed copy before anyone reviews it. On the single-account install a passing required check
therefore says less than it seems to: when a pull request changes a script a check runs, read that
change yourself before you merge.

You can give the App the **Workflows** permission on GitHub, and agents will then be able to change
your workflow files too. That adds two costs:

- An agent can rewrite a required check itself, and change when a job runs and what it may do.
- A changed workflow can reach every Actions secret in your repository as soon as its pull request
  opens, before anyone reviews it and whether or not it ever merges. The merge rule does not stop
  this.

**Working over SSH?** The browser is on another computer. Either forward the port first,
`ssh -L <port>:127.0.0.1:<port> <machine>`, and pass the same `--port <port>` to the command, or run

```bash
python3 ~/src/shipwright/bin/create-github-app --code-from-tty
```

and paste the whole address at the terminal: once the browser shows GitHub's redirect failing,
copy the whole address from its bar (`http://127.0.0.1:<port>/callback?code=...&state=...`) and
paste it at the prompt, then press enter. A bare code with no address is refused. If you have
already left the terminal, run the command again with `--code <code>`, the value after `code=` in
that same address.

**Install the App on your repositories** at the address the command printed, choosing the
repositories your crews work in. The App can reach only those.

**A second, read-only App is optional.** For a repository agents should read and never write, run
the command again with `--read-only`. That App can read contents and nothing else. Install it on
those repositories, and leave them out of the first App's installation: while the first App can
reach one of them, Builder refuses to hand out its token, since that token could write there. In
step 2, name each of those repositories to `connect-github` with `--read-only <owner>/<name>`. The
list holds names, and `--read-only` replaces the whole list, so if you rename or transfer one of
those repositories, run `connect-github` again with a `--read-only` for every read-only repository,
the moved one under its new name.

## 2. Connect the install

```bash
python3 ~/src/shipwright/bin/connect-github --mode instruction
```

It does five things, and running it again changes nothing that is already right.

- It places `github-app-token`, which prints a current token for the App, and links it in
  `~/.local/bin`, along with a `gh` that runs the real GitHub command line with that token.
- It makes that token git's only credential for `https://github.com`.
- It changes every project remote that uses SSH to HTTPS, since an SSH remote signs in with a key and
  never asks for the token. It stops and names any remote it cannot change.
- It records the mode.
- It looks for any GitHub credential of yours still on the account, as hygiene: a login the `gh`
  command holds, an SSH key GitHub accepts, a token variable in your environment or a shell profile,
  an entry for github.com in `~/.netrc`, a credential git would fall back to such as one in the Mac's
  keychain, a credential helper set for one project, and a rule that rewrites GitHub addresses. It
  names each one it finds and carries on without failing: a credential of yours left on the machine is
  something an agent could act on GitHub with instead of the App, held off only by the agents'
  instructions, so it is worth removing and signing out of any GitHub session in a browser on this
  machine too.

## 3. Import the rule

```bash
python3 ~/src/shipwright/bin/github-gate --ruleset --shape single --mode instruction \
  --require-check <check>
```

Name each of the repository's automated checks with `--require-check`, as GitHub shows them on a
pull request.

It prints the rule as a file's worth of JSON, followed by where to import it. Save the JSON to a
file. In the repository on GitHub, open **Settings**, then **Rules**, **Rulesets**, **New ruleset**
and **Import a ruleset**, and choose the file. Under a GitHub organisation, add `--org <name>` and
import it once in the organisation's settings to cover every repository.

While you're in the repository's **Settings**, under **General**, **Pull Requests**, also turn on
**Automatically delete head branches**. Without it, a pull request stacked on another lands on
main by itself only when GitHub deletes the base branch as part of merging it.

## 4. Check it

```bash
GH_TOKEN=$(github-app-token) python3 ~/src/shipwright/bin/github-gate --check --shape single \
  --mode instruction --repo <owner>/<name> --require-check <check>
```

It reads each repository's rules with the App's own token and says, for each, whether they match,
naming any setting that differs. GitHub does not show the App who else may bypass the rule, so for
that the check confirms only that the App cannot.

## Keeping it true

Run the connect step's check after you install or sign in to any GitHub tool on this machine:

```bash
python3 ~/src/shipwright/bin/connect-github --check
```

It changes nothing, and it names any credential of yours that has appeared since you connected, the
same hygiene report as step 2: worth removing, since it is something an agent could act on GitHub
with instead of the App, held off only by the agents' instructions.
