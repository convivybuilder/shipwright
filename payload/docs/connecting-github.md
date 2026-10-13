# Connecting GitHub on the single-account install

On the single-account install, Builder runs as your own account, and its agents still reach GitHub
under an identity of their own: a GitHub App you create, which is an identity on GitHub that belongs
to a program instead of a person. Every pull request an agent opens, every push and every review
comment then shows the App's name rather than yours. You keep your own GitHub account on your phone
or another computer, and approve and merge from there. Like the rest of this site, this page
describes Builder as it is designed to work.

You also choose how firmly GitHub holds the rule that a person merges. **Enforced** makes GitHub
refuse to merge a pull request an agent opened until you approve it. On a pull request you opened
and only you pushed to, GitHub would also count an agent's approval, and only the instruction every
agent carries stops it approving; once an agent pushes to it, it cannot merge at all. **Instruction only** leaves that rule to the instruction
every agent carries, as it was before the App. This page recommends Enforced, and says what each
one holds.

## Why the agents need their own identity

On the single-account install, every agent session can read everything your account holds. If your
GitHub login is on the machine, an agent can act on GitHub as you: approve a pull request, or merge
one. GitHub cannot tell that agent from you, so no rule on GitHub can stop it.

Move the agents to an App, take your own credential off the machine, and that changes. The App has
only the permissions you gave it when you created it. It can push branches, open pull requests and
comment, and it cannot change the rules on your repositories. GitHub knows the App is not you, so a
rule can require something only you can give.

## The two merge modes

**Enforced.** A rule on `main`, the project's current version, requires a pull request, the
automated checks you name, and an approving review of the latest push from a code owner. A code
owner is a person a file named `CODEOWNERS` lists as owning part of the repository, and yours lists
you alone, for every path. GitHub never counts an App as a code owner, so on a pull request an
agent opened, a review the agents' App submits never satisfies the rule. A later push to the pull
request clears your approval, and no one is exempt from the rule, an administrator included.

**Instruction only.** The rule on `main` requires a pull request and the checks you name, and no
approval. That no agent merges is held by the instruction every agent carries. You still gain an
identity for the agents' work, and credentials that last an hour and reach only the repositories
you installed the App on.

### What Enforced still allows

- **An agent can press merge on a pull request you have approved.** GitHub admits the merge once
  your approval and the checks are there, whoever presses the button. The instruction that no agent
  merges still forbids it.
- **An agent can push to any branch other than `main`**, including the branch of an open pull
  request. Your approval is cleared by that push, so the change needs approving again.
- **An agent can review and comment.** On a pull request an agent opened or pushed to, its
  approval counts for nothing toward the merge.
- **An agent's approval counts on a pull request you opened, for what you pushed.** GitHub does not
  ask for a code owner's review when the pull request's author is a code owner, so on your own pull
  request any approval from an account that can write to the repository satisfies the rule, the
  agents' App included. Once an agent pushes to that pull request, the latest push needs approving
  by someone other than the agent, and you cannot approve your own pull request, so it stays blocked.
  The instruction every agent carries forbids it to approve a pull request at all.

### What Enforced cannot see

**Enforced holds only while no GitHub credential of yours is on the machine.** The connect step
below looks for every kind it can find, and does not report Enforced as active while one remains.
Two kinds it cannot catch:

- **A GitHub session signed in through a web browser on the machine.** An agent driving that
  browser could approve as you. Do not stay signed in to GitHub in a browser on this machine.
- **A credential added after you connect.** The check runs when you run it. After you set up any
  GitHub tool on this machine, run the check again, as the last section says.

**The check cannot see who else may bypass the rule.** GitHub shows a rule's bypass list only to
someone who can administer the repository, and the agents' App deliberately cannot, so the check
confirms only that the App itself cannot bypass it. Keep the rule's **Bypass list** empty in its
settings on GitHub; the rule this guide prints has none.

## Before you start

You need the install from [Installing Builder](installing.md), a GitHub account of your own,
and the repositories your crews work in. Run every command below in a terminal on the machine
Builder runs on, as your own account.

## 1. Create the App

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

**Working over SSH?** The browser is on another computer, so forward the port first:
`ssh -L <port>:127.0.0.1:<port> <machine>`, and pass the same `--port <port>` to the command. If the
redirect cannot reach this machine, the browser's address bar still holds `?code=...`; run the
command again with `--code <code>`.

**Install the App on your repositories** at the address the command prints, choosing the repositories
your crews work in. The App can reach only those.

**A second, read-only App is optional.** For a repository agents should read and never write, run
the command again with `--read-only`. That App can read contents and nothing else. Install it on
those repositories, and leave them out of the first App's installation: while the first App can
reach one of them, Builder refuses to hand out its token, since that token could write there. In
step 2, name each of those repositories to `connect-github` with `--read-only <owner>/<name>`. The
list holds names, and `--read-only` replaces the whole list, so if you rename or transfer one of
those repositories, run `connect-github` again with a `--read-only` for every read-only repository,
the moved one under its new name.

## 2. Connect the install

Choose the mode, then run:

```bash
python3 ~/src/shipwright/bin/connect-github --mode enforced
```

or `--mode instruction`. It does five things, and running it again changes nothing that is already
right.

- It places `github-app-token`, which prints a current token for the App, and links it in
  `~/.local/bin`, along with a `gh` that runs the real GitHub command line with that token.
- It makes that token git's only credential for `https://github.com`.
- It changes every project remote that uses SSH to HTTPS, since an SSH remote signs in with a key and
  never asks for the token. It stops and names any remote it cannot change.
- It records the mode you chose.
- It looks for any GitHub credential of yours still on the account.

**In Enforced mode it reports Enforced as active only when it finds none.** It looks for a login the
`gh` command holds, an SSH key GitHub accepts, a token variable in your environment or a shell
profile, an entry for github.com in `~/.netrc`, a credential git would fall back to such as one in
the Mac's keychain, a credential helper set for one project, and a rule that rewrites GitHub
addresses. It names each one it finds, and you remove it and run the command again. In
Instruction-only mode it names them too and carries on.

## 3. Name yourself as code owner (Enforced only)

In each repository, push a file `.github/CODEOWNERS` to `main` that holds exactly this line, with
your GitHub login:

```
* @your-login
```

Push it before the next step. The rule you import there refuses a direct push to `main`, so after
that this file can only change through a pull request.

## 4. Import the rule

```bash
python3 ~/src/shipwright/bin/github-gate --ruleset --shape single --mode enforced \
  --operator your-login --require-check <check>
```

Name each of the repository's automated checks with `--require-check`, as GitHub shows them on a
pull request. For Instruction only, use `--mode instruction` and leave out `--operator`.

It prints the rule as a file's worth of JSON, followed by where to import it. Save the JSON to a
file. In the repository on GitHub, open **Settings**, then **Rules**, **Rulesets**, **New ruleset**
and **Import a ruleset**, and choose the file. Under a GitHub organisation, add `--org <name>` and
import it once in the organisation's settings to cover every repository.

While you're in the repository's **Settings**, under **General**, **Pull Requests**, also turn on
**Automatically delete head branches**. Without it, a pull request stacked on another lands on
main by itself only when GitHub deletes the base branch as part of merging it.

## 5. Check it

```bash
GH_TOKEN=$(github-app-token) python3 ~/src/shipwright/bin/github-gate --check --shape single \
  --mode enforced --operator your-login --repo <owner>/<name> --require-check <check>
```

It reads each repository's rules with the App's own token and says, for each, whether they match the
mode you chose, naming any setting that differs. In Enforced mode it also reads `CODEOWNERS` on
`main` and fails unless every path ends up owned by you alone, and it fails on any line GitHub itself
reports as broken, such as one naming a login that does not exist. GitHub does not show the App
who else may bypass the rule, so for that the check confirms only that the App cannot.

## Keeping it true

Run the connect step's check after you install or sign in to any GitHub tool on this machine:

```bash
python3 ~/src/shipwright/bin/connect-github --check
```

It changes nothing, and it names any credential that has appeared since you connected. In Enforced
mode a credential it finds means GitHub's rule no longer holds on its own until you remove it.

To change the mode later, run the connect step with the other `--mode`, then import that mode's rule
in place of the old one.
