# Install checklist

This page lists every step you do by hand across the whole install, in the order you meet them:
the accounts to have ready, running the one command on the server, connecting GitHub, and adding
the server to Deck on your laptop. [Installing Builder](installing.md) explains each one; this
page is only the list, with a checkbox beside each step and a link to where it is explained.

Checking a box saves in this browser alone, so it is still ticked if you come back to this page
later, on this machine. It saves nothing anywhere else, and nothing checks it but you.

<p><button type="button" id="checklist-reset">Reset every box</button></p>

## Before you start

<ul class="checklist">
<li><label><input type="checkbox" id="ck-claude-code"> Install Claude Code on the server's account and sign in. On a Mac, or a Linux account with no administrator access, this happens later, as part of that page's own steps. <a href="installing.md#before-you-start">Before you start</a></label></li>
<li><label><input type="checkbox" id="ck-github-account"> Have a GitHub account ready, unless you plan to run the server install with <code>--no-github-app</code> and connect one later. <a href="what-you-need.md#a-github-account">A GitHub account</a></label></li>
<li><label><input type="checkbox" id="ck-tailscale"> Install Tailscale on both machines and sign in with the same account, unless you already have another working SSH address for the laptop to reach the server by. <a href="what-you-need.md#tailscale-to-join-your-machines-together">Tailscale, to join your machines together</a></label></li>
</ul>

## Only if your server is a Mac

<ul class="checklist">
<li><label><input type="checkbox" id="ck-mac-prepare"> If you administer the Mac yourself, prepare it before cloning anything: skip signing in to iCloud, turn off the screen lock, and turn on automatic login. <a href="install-mac.md#preparing-a-mac">Preparing a Mac</a></label></li>
<li><label><input type="checkbox" id="ck-mac-admin"> Have the Mac's administrator set it up once: install Command Line Tools and tmux, give the account a passphrase used nowhere else, then turn on Remote Login and Screen Sharing and confirm who can reach them. <a href="install-mac.md#what-the-macs-administrator-does-once">What the Mac's administrator does once</a></label></li>
<li><label><input type="checkbox" id="ck-mac-owner"> As the account's owner, log in at the desktop, install Claude Code, <code>uv</code> and Python 3.11, and sign in to Claude Code. <a href="install-mac.md#what-the-accounts-owner-does">What the account's owner does</a></label></li>
</ul>

## Only if your Linux account has no administrator access

<ul class="checklist">
<li><label><input type="checkbox" id="ck-linux-nosudo-admin"> Have the machine's administrator install the system packages once and turn on lingering for your account. <a href="install-linux-without-sudo.md#what-the-machines-administrator-does-once">What the machine's administrator does once</a></label></li>
<li><label><input type="checkbox" id="ck-linux-nosudo-owner"> As the account's owner, install Claude Code and sign in. <a href="install-linux-without-sudo.md#what-the-accounts-owner-does">What the account's owner does</a></label></li>
</ul>

## Install Builder on the server

<ul class="checklist">
<li><label><input type="checkbox" id="ck-one-command"> Run the one command on the server. If it names something missing, install that and run it again. <a href="installing.md#the-one-command">The one command</a></label></li>
<li><label><input type="checkbox" id="ck-manual-route"> Or, to run each step yourself instead of the one command: clone the six repositories, then follow the page for your server. <a href="installing.md#which-install-is-yours">Which install is yours</a></label></li>
<li><label><input type="checkbox" id="ck-github-app-click"> When it pauses to create the GitHub App, open the address it prints and click <strong>Create GitHub App</strong>. Over SSH, the browser's redirect fails; copy the whole address from its bar and paste it at the terminal. Skip this with <code>--no-github-app</code> if you have no GitHub account yet. <a href="connecting-github.md#1-create-the-app">1. Create the App</a></label></li>
<li><label><input type="checkbox" id="ck-github-app-manual"> On the step-by-step route, or if you skipped the App with <code>--no-github-app</code>, create it yourself once you have a GitHub account: run <code>python3 ~/src/shipwright/bin/create-github-app</code> on the server, open the address it prints, and click <strong>Create GitHub App</strong>. Over SSH, add <code>--code-from-tty</code> and paste the whole address from the browser's bar at the terminal. <a href="connecting-github.md#1-create-the-app">1. Create the App</a></label></li>
<li><label><input type="checkbox" id="ck-path-check"> Open a new login shell and check that <code>command -v co agentctl</code> prints a path under <code>~/.local/bin</code> for each. <a href="install-linux.md#run-the-install">Run the install</a></label></li>
</ul>

## Connect GitHub

Skip this group if you ran the install with `--no-github-app` and are not connecting one yet.

<ul class="checklist">
<li><label><input type="checkbox" id="ck-install-app-on-repos"> Install the App on the repositories your crews will work in. <a href="connecting-github.md#1-create-the-app">1. Create the App</a></label></li>
<li><label><input type="checkbox" id="ck-connect-install"> Connect the install. <a href="connecting-github.md#2-connect-the-install">2. Connect the install</a></label></li>
<li><label><input type="checkbox" id="ck-import-rule"> Import the rule into each repository's settings on GitHub, and turn on "Automatically delete head branches". <a href="connecting-github.md#3-import-the-rule">3. Import the rule</a></label></li>
<li><label><input type="checkbox" id="ck-check-rule"> Check that the rule matches what you set up. <a href="connecting-github.md#4-check-it">4. Check it</a></label></li>
</ul>

## Set up your laptop

<ul class="checklist">
<li><label><input type="checkbox" id="ck-install-deck"> Install Deck on your laptop. <a href="installing.md#the-one-command">The one command</a></label></li>
<li><label><input type="checkbox" id="ck-deck-add-host"> In Deck, open Settings, click <strong>Hosts</strong>, then <strong>+</strong>, fill in the server's Name, User and Address, and click <strong>Pair this Mac…</strong>. <a href="after-installing.md#meet-the-steward">Meet the steward</a></label></li>
<li><label><input type="checkbox" id="ck-deck-fingerprint"> Check that the host key fingerprint Deck shows matches the one the server's install printed, then click <strong>Trust</strong>. <a href="after-installing.md#meet-the-steward">Meet the steward</a></label></li>
<li><label><input type="checkbox" id="ck-deck-password"> Enter the account's password when Deck asks for it, and click <strong>Install Key</strong>. <a href="after-installing.md#meet-the-steward">Meet the steward</a></label></li>
<li><label><input type="checkbox" id="ck-deck-add"> Click <strong>Add</strong>. <a href="after-installing.md#meet-the-steward">Meet the steward</a></label></li>
</ul>

## Meet the steward

<ul class="checklist">
<li><label><input type="checkbox" id="ck-steward-talk"> Click the steward's row to open it, and tell it what you want to build. <a href="after-installing.md#meet-the-steward">Meet the steward</a></label></li>
<li><label><input type="checkbox" id="ck-first-crew-prompts"> On your first crew, answer whether to trust its folder and whether to accept bypass-permissions mode. <a href="after-installing.md#your-first-crew">Your first crew</a></label></li>
</ul>

<script>
(function () {
  "use strict";
  var STORAGE_KEY = "builder-install-checklist";
  var boxes = document.querySelectorAll(".checklist input[type=checkbox]");

  function load() {
    try {
      return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function save(state) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      // Storage is unavailable; the boxes still work, but they will not be remembered.
    }
  }

  var state = load();
  for (var i = 0; i < boxes.length; i++) {
    var box = boxes[i];
    if (state[box.id]) {
      box.checked = true;
    }
    box.addEventListener("change", function () {
      state[this.id] = this.checked;
      save(state);
    });
  }

  var reset = document.getElementById("checklist-reset");
  if (reset) {
    reset.addEventListener("click", function () {
      for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked = false;
      }
      state = {};
      try {
        window.localStorage.removeItem(STORAGE_KEY);
      } catch (e) {
        // Nothing to clear if storage was never available.
      }
    });
  }
})();
</script>

## Where to go next

- **[Installing Builder](installing.md)** explains the layout and the words these steps use.
- **[After the install](after-installing.md)** shows what the install put where and takes you to
  the steward.
