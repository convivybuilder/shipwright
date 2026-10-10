# Your own Cloudflare account

Builder will share an app with a few people you name, through Cloudflare Access, from a Cloudflare
account and a domain that belong to you. This page takes you from having no Cloudflare account to a
domain Cloudflare serves, ready to share from. Like a bead, which is a project's short description
of where it is going, the page describes Builder as it is designed to work, and the system is still
catching up to that design.

Cloudflare is a company whose network stands between the internet and a website, and Cloudflare
Access is its service that decides who may open one. A domain is an address you own, such as
`example.com`. You need this page only when you want someone outside your own network to open an
app you built. Until then, your apps run on your own machine and you can skip it.

There are four steps. You create the account, you move your domain to Cloudflare, you give the
program that connects your machine a certificate, and you create a token Builder can act with. Step
2 is the long one, because moving a domain can interrupt its website and email if it is done in the
wrong order, and the page gives the order that avoids that.

**Wait to do steps 2 to 4 until Builder's sharing command ships.** Nothing in Builder uses a
Cloudflare domain yet, and step 2 moves your domain's DNS and email. Creating the account in step 1
changes nothing else and can be done at any time.

## How sharing works

A shared app has its own address on your domain, such as `plans.example.com`, and Cloudflare stands
in front of it. A viewer opens the link and enters their email address. If the app's list allows
that address, Cloudflare emails them a one-time code, which expires after ten minutes. Nobody needs
a password or an account to see the app. You can let one person in or out without affecting anyone
else, and Cloudflare records every login.

Builder's sharing command, which is not built yet, will set this up for each app. It will create the
app's address and the Access application in front of it, and keep the lists of people allowed in. An
Access application is Cloudflare's name for one protected address and its rules. Several apps can
share one list, such as a client's staff.

## Why the account is yours

The people you share with join your account's list of users and nobody else's.

**Access counts seats per account.** A seat is one person's place on the account. The free plan
covers 50 people. A person takes one seat the first time they log in, however many of your apps they
can reach. Sharing with a client's staff spends your seats, so count them before you share with a
large client.

## 1. Create the account

Sign up at `dash.cloudflare.com` with an email address you intend to keep. The free plan covers
everything on this page. Turn on two-factor authentication, which asks for a second proof, such
as a code from your phone, as well as your password, because this account decides who can see every app you share.

## 2. Add your domain

This step hands the job of answering for your domain to Cloudflare. A few terms make it easier to
follow.

- **DNS** is the internet's address book. It turns a name such as `example.com` into the location
  of the machine that serves it.
- **A DNS record** is one entry in that book, such as where the website lives or where email goes.
- **A registrar** is the company you bought the domain from.
- **Nameservers** are the machines that hold a domain's DNS records. The registrar says which
  nameservers speak for your domain.

Cloudflare serves your domain once the domain's registrar points it at Cloudflare's nameservers.
Add the domain in the dashboard, and Cloudflare will scan your current DNS records and copy them.
Compare its list with the records at your current DNS provider before you go further. A record the
scan missed stops working when the nameservers change.

The parts below follow the order of the work: DNSSEC first, then the nameservers, then email.

### Turn off DNSSEC before you switch

DNSSEC is an optional protection in which a domain's DNS answers are signed, so that a resolver can
tell a forged answer from a real one. If you never turned it on, check that it is off at your registrar and go on to the next
part.

If DNSSEC is on at your registrar, turn it off first, and wait for the change to reach the registry
before you touch the nameservers. The registry is the organisation that runs your domain's ending,
such as `.com`. With DNSSEC on, the registry holds a DS record vouching for your old provider's
signing keys. Cloudflare signs with different keys, so every resolver that checks DNSSEC rejects
Cloudflare's answers, and the whole domain stops resolving, website and email alike. A resolver is
the service that looks names up on behalf of a browser or a mail server.

After you turn DNSSEC off at the registrar, the DS record can take up to 24 hours to clear. Check
it by typing this in a terminal, with your own domain in place of `example.com`:

```
dig +short DS example.com
```

When that prints nothing, you can switch. Once the domain is active on Cloudflare, turn DNSSEC
back on from the domain's DNS settings, so the domain regains the protection it had. Cloudflare
gives you a new DS record, which you add at your registrar.

### Switch the nameservers

Cloudflare gives you two nameservers. At your registrar, replace the domain's nameservers with
those two. Cloudflare marks the domain Active once it sees the change, and emails you. That email
is how you know this part worked.

### Move your email forwarding

This part applies only if your registrar forwards mail sent to your domain on to another inbox.
That forwarding stops when the nameservers change. Cloudflare Email Routing replaces it. Set it up
as soon as the domain is active:

1. In the domain's DNS records, delete the MX records Cloudflare copied from your registrar. MX
   records are the DNS records that say where a domain's email is delivered. Email Routing refuses
   to onboard a domain while they remain.
2. Open Email Routing at the account level: **Compute → Email Service → Email Routing → Onboard
   Domain**. The Email menu inside the domain is a different page.
3. Add the address mail should go to. Cloudflare sends it a verification link, and the address
   shows as **Verified** once you follow it.
4. Create a rule for each address you receive mail at, or one catch-all rule, which forwards mail
   sent to any address at the domain. Set its action to **Send to an email**, and make sure it is
   **Active**.

For a few minutes after the switch, some senders still deliver to your old mail servers, because
their resolvers keep the old MX records for that long.

If a message bounces with `550 5.1.1 Address does not exist` from a server named
`route*.mx.cloudflare.net`, the mail reached Cloudflare and no rule forwarded it. Check that the
destination shows Verified, and that a rule matching the address, or the catch-all, is Active with
the action **Send to an email**.

### Set GitHub Pages records to DNS only

This part applies only if you host a website on GitHub Pages, GitHub's free hosting for simple
sites. If any record points at a site hosted there, set that record to **DNS only**, which shows as
a grey cloud. Left **Proxied**, it can stop GitHub renewing the site's certificate.

## 3. One certificate per domain for cloudflared

An app served from your own machine reaches its viewers through a Cloudflare Tunnel, which the
`cloudflared` program runs. A tunnel is a connection your machine opens outward to Cloudflare, and
viewers come in through it. The app itself listens only on your machine, so the tunnel is the only
way in.

`cloudflared tunnel login` asks you to choose one domain, and writes a certificate for that domain
alone to `~/.cloudflared/cert.pem`. The certificate is a file that proves to Cloudflare that
`cloudflared` may act for that domain, and `~` stands for your home folder. `cloudflared` uses that
certificate whenever it creates a DNS record.

There is one trap to know about. **Given a hostname in another domain, `cloudflared tunnel route
dns` reports no error**. It creates the record inside the certificate's domain instead, so asking
for `app.example.org` with a certificate for `example.com` creates `app.example.org.example.com`.

Whoever holds one of these certificates can change DNS records in its domain, so keep the files
private, as you would a password.

If you have more than one domain, keep a certificate for each. After each login, rename `cert.pem`
after its domain, then log in again for the next one:

```
cloudflared tunnel login
mv ~/.cloudflared/cert.pem ~/.cloudflared/example-com-cert.pem
```

Pass the matching certificate every time `cloudflared` creates a record. The `--origincert` option
goes after `tunnel` and before the command, and `cloudflared` rejects it anywhere else:

```
cloudflared tunnel --origincert ~/.cloudflared/example-com-cert.pem route dns my-tunnel app.example.com
```

Setting `TUNNEL_ORIGIN_CERT` to the certificate's path does the same.

## 4. The API token

**Wait to create this token until Builder's sharing command ships.** A token that nothing uses can
only leak, and this one can change Access on every app in the account.

An API token is a long secret string that lets a program act on your account, within limits you set.
Builder's sharing command works on your account through an API token you create, limited to your
account's domains and to Access. Create it under **My Profile → API Tokens → Create Token**, as a
custom token. Under **Zone Resources**, include only the domains you share from, so the token cannot
change DNS on any other domain in the account. It needs permission to edit DNS records, Cloudflare
Tunnels, and Access applications and policies. Cloudflare grants the Tunnel and Access permissions
across the whole account, so the token can change who may reach every app the account protects, and
it is worth guarding as closely as your password. Where the sharing command keeps the token on your
machine is not settled yet, and this page will say once it is.

Use a token, and leave your Global API Key unused. The key can do anything your login can, in every
account you belong to, and a token can do only what you gave it.

Handle the token as a password. Keep it out of repositories, chats and shared documents, and if it
is ever exposed, revoke it on the API Tokens page and create a new one.
