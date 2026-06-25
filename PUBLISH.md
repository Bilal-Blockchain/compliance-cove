# Compliance Cove - Publishing & Update Runbook

How the Cove is shared company-wide and kept up to date. Read this before touching the public site.

---

## The model in one picture

```
GitHub (source of truth)
        |  pull + render
        v
[ HOLDER SESSION ]  <-- one dedicated Chain chat, Shared once.
        |  its Share URL never changes while the session lives
        v
Confluence pointer page  -->  the URL most people use
AEs may also deep-link the Holder URL directly (so treat the URL as semi-permanent)
```

- **Holder Session** = ONE Chain chat that renders the hub and is set to **Share**. Its Share URL is the official Compliance Cove link.
- The Confluence page links to that URL. Some AEs will copy the URL and paste it into their own decks/emails, so **changing the URL is expensive** (it strands those deep-links).
- Therefore: **keep the Holder Session alive as long as possible, update it in place, and only mint a new URL when you truly have to.**

---

## Rules for the Holder Session

1. **Make it fresh and keep it pristine.** Start a brand-new chat. Do NOT do development, debugging, or experiments in it. The only things that ever happen in the Holder Session are: pull latest, render the hub, (rarely) re-render. A quiet session keeps its context window from filling, which is what keeps the URL alive.
2. **Do all real work elsewhere.** Build/fix demos in a separate working session, push to GitHub, THEN update the Holder Session.
3. **One Holder Session at a time.** If you ever start a new one, retire the old one and update the Confluence URL the same day.

---

## A. First-time publish (establish the Holder Session)

Run once. In a **new, empty chat**, paste:

> Pull the latest `Bilal-Blockchain/compliance-cove` repo via the GitHub API (Python requests, not curl). Render `compliance-cove.html` as an HTML artifact. Do nothing else in this session.

Then:
1. Open the rendered hub, confirm it looks right.
2. Click **Share** at the top of the chat and make it public.
3. Copy the Share URL. This is the **official Compliance Cove URL**.
4. Put that URL on the Confluence page (see the runbook there).

---

## B. Routine update (PREFERRED - keeps the same URL)

Use this whenever you push new demo content to GitHub and want the public site refreshed. **This does NOT change the URL, so deep-links and the Confluence link keep working.**

In the **existing Holder Session**, paste:

> Pull the latest `Bilal-Blockchain/compliance-cove` repo again and re-render `compliance-cove.html` as an HTML artifact.

That is it. Viewers opening the Share URL now see the latest version. Do not change anything on Confluence.

> Keep these updates lean: one line in, one render out. The fewer/cleaner the turns, the longer the session (and its URL) survives.

---

## C. Full respawn (LAST RESORT - the URL changes)

Only when the Holder Session is dead, reset, or its context window is exhausted and it can no longer render.

1. Start a new chat and run section **A** again to get a NEW Share URL.
2. **Update the Confluence pointer URL** to the new link (and bump the "Last updated" stamp).
3. Post a quick heads-up to the team channel so anyone who deep-linked the old URL re-grabs it from Confluence.
4. Retire the old session.

Because step 2/3 are disruptive, exhaust section **B** first.

---

## Requirements for the live site to work for everyone

- Every workflow a demo calls must be **org-public**. (As of the latest release all 7 are: `demochain-address-screen`, `cove-kyt-screen`, `arcswap-reactor-graph`, `cove-hexagate`, `cove-token-intel`, `cove-insurance-graph`, `compliance-cove-analytics`.) When you add a new workflow, run `WorkflowsClient().set_org_public(slug, True)` before release.
- Viewers must be **logged-in Chainalysis users** for live workflow calls to authorize. This is also what keeps the site internal-only.
- **Analytics is admin-only:** the dashboard reads the usage Google Sheet using the caller's own Google connection, so it only works for admins who have Google connected in Chain and access to the sheet. Non-admins see a friendly "admin-only" message.

---

## Quick reference

| I want to... | Do this | URL changes? |
|---|---|---|
| Launch the public site | Section A | New URL (first time) |
| Push new demo content live | Section B | No |
| Recover a dead Holder Session | Section C | Yes (update Confluence) |
