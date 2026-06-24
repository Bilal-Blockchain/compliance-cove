# 🗺️ Compliance Cove — Roadmap

> **Purpose:** Track all planned work for the Compliance Cove project. Future Chain sessions should read this file to understand what's next, what's in progress, and what's done.
>
> **How to use:** Tell Chain: _"Read ROADMAP.md and let's work on the next priority."_
>
> **Last updated:** June 23, 2026

---

## Status Legend

| Icon | Meaning |
|------|---------|
| ⬜ | Not started |
| 🟡 | In progress |
| ✅ | Complete |
| 🔴 | Blocked / needs input |

---

## 🔥 Top Priority — API Explainer Pages

Interactive reference pages that make Chainalysis APIs **dead simple** for CSMs, AEs, and SAs to explain to prospects. Each page walks through the API workflow step-by-step with visuals and code snippets. Non-technical teammates should be able to open these and talk through the integration story without any coding knowledge.

### E1. 📘 KYT API Explainer `kyt-explainer.html`
**Priority:** 🔥 TOP — Most-asked-about product, needs a simple visual walkthrough  
**Effort:** ~3–4 hours  
**Status:** ⬜ Not started  
**Goal:** Interactive page showing how KYT works end-to-end. Each section is a step in the workflow with a diagram, plain-English explanation, and collapsible code snippet.

| # | Section / Step | What it shows | Code snippet |
|---|---|---|---|
| E1.1 | **What is KYT?** | One-paragraph overview + product positioning. Hero visual. | — |
| E1.2 | **Step 1: Create a User** | Every customer on the platform gets a KYT user ID. This is how you tie transactions back to a person. | `POST /v2/users` with `userId`, response showing `createdAt` |
| E1.3 | **Step 2: Register a Transfer** | When a customer deposits or sends crypto, register the transaction with KYT. Explain `direction: received` vs `sent`. | `POST /v2/users/{userId}/transfers` with `network`, `asset`, `transferReference`, `direction` |
| E1.4 | **Step 3: KYT Monitors & Scores** | KYT analyzes on-chain exposure in real-time. Visual showing the transfer being traced through the blockchain. Explain what happens behind the scenes. | `GET /v2/transfers/{externalId}` — poll until `updatedAt` is non-null |
| E1.5 | **Step 4: Check Exposure** | Show the exposure breakdown — which categories of counterparties the funds touched. | `GET /v2/transfers/{externalId}/exposures` — response with categories + values |
| E1.6 | **Step 5: Alerts** | If risk thresholds are exceeded, KYT generates an alert. Show alert levels and what triggers them. | `GET /v2/transfers/{externalId}/alerts` — alert with `level`, `categoryId` |
| E1.7 | **Step 6: Pre-Screen Withdrawals** | Before sending funds OUT, pre-screen the destination address. This is the compliance gate before releasing money. | `POST /v2/users/{userId}/withdrawal-attempts` with `address`, `network`, `asset` |
| E1.8 | **Step 7: Review & Resolve** | Analyst workflow — review alerts, investigate in Reactor, make a disposition decision. | `PATCH /v1/alerts/{alertId}` — update status to `RESOLVED` |
| E1.9 | **Full Flow Diagram** | End-to-end visual: Customer action → API call → KYT response → Decision → Next step | Mermaid or SVG diagram |

**Design:** White background, Chainalysis branding (like the screener). Each step is a card with:
- Step number + title
- Plain-English explanation (2-3 sentences a CSM could read aloud)
- Visual diagram or animation showing what's happening
- Collapsible "View Code" section with the API request/response
- "What this means for the customer" callout

**Integration with hub:** Add to SA Tools section alongside the Address Screener.

---

### E2. 🔍 Address Screening API Explainer `screening-explainer.html`
**Priority:** 🔥 TOP  
**Effort:** ~2–3 hours  
**Status:** ⬜ Not started  
**Goal:** Same format as KYT explainer but for Address Screening. Simpler flow (single API call), but rich explanation of what comes back.

| # | Section / Step | What it shows | Code snippet |
|---|---|---|---|
| E2.1 | **What is Address Screening?** | Overview — screen any blockchain address for risk before allowing it on your platform. | — |
| E2.2 | **Step 1: Screen an Address** | Single API call with the address. That's it. | `GET /v2/entities/{address}` |
| E2.3 | **Understanding the Response** | Break down every field: risk level, risk reason, address type, cluster info | Response JSON with annotations |
| E2.4 | **Identifications** | What are identifications? Sanctions lists, known entities, named services. | `addressIdentifications[]` with examples |
| E2.5 | **Exposure Analysis** | Direct vs indirect exposure. What each category means. Why percentages matter. | `exposures[]` with visual bars |
| E2.6 | **Triggered Rules** | How rule-based alerting works. Custom thresholds. | `triggers[]` with threshold explanation |
| E2.7 | **Decision Matrix** | What to do with each risk level: Low → allow, Medium → review, High/Severe → block | Visual decision tree |
| E2.8 | **Live Demo** | Link to the Address Screener tool — "Try it yourself" | Link to `screener.html` |

---

*E3 (Withdrawal Pre-Screening Explainer) — removed, fully covered by E1's interactive Withdrawal tab.*

---

## 📌 Current Sprint — Completed Work

### 1. ✨ Polish the DeFi Trading Demo — Renamed to **ArcSwap** `demochain.html`
**Priority:** 🔥 HIGH — This is the flagship demo every SA uses first  
**Effort:** ~2–3 hours total  
**Goal:** ~~Bring DemoChain up to the same polish level as Banking and Gaming demos~~ **DONE**  
**Renamed:** DemoChain → **ArcSwap** (throughout file + hub page)

| # | Task | Status | Effort | Notes |
|---|------|--------|--------|-------|
| 1.1 | ~~Force light mode~~ Keep dark mode | ✅ | — | User preferred dark mode — fits DeFi aesthetic. Added forced `color-scheme: dark` with custom DeFi-dark palette (`--arc-bg`, `--arc-card`, `--arc-border`, `--arc-glow`). |
| 1.2 | Add animated background | ✅ | 45 min | Canvas particle network with floating nodes + connection lines. Mouse-reactive glow. Subtle radial gradient ambient lighting in indigo/cyan. |
| 1.3 | Improve wallet connect flow | ✅ | — | Already had wallet provider selection (MetaMask, Coinbase, WalletConnect, Phantom, Trust, Rabby). Enhanced with glass-morphism styling, hover glow effects, and subtle lift animations. |
| 1.4 | Add "View in Reactor →" links | ✅ | 15 min | Reactor links now appear in screening results next to the address. Updated `reactorLinkHtml()` with better glass styling and glow hover. URL pattern: `reactor.chainalysis.com/graphs/reactor/{NET}/{ADDR}`. KYT alert API reference documented in code. |
| 1.5 | Speed up compliance workflow | ✅ | 10 min | Deposit steps: 300→450→600→300ms (was 600→900→1200→600). Withdraw steps: 250→300→400→250ms (was 500→400→800→500). KYT step states now have glow `box-shadow`. |
| 1.6 | Upgrade token swap UI | ✅ | 30 min | Added: slippage tolerance popover (0.1%/0.5%/1.0%/3.0%), visual route path visualization (ETH→WETH→Pool 0.3%→USDT), MAX button on from-balance, swap card glow border, glow button with sweep animation. |
| 1.7 | Glass-morphism overhaul | ✅ | 30 min | Nav: backdrop-blur with gradient underline. Cards: glass background with border glow on hover. Modals: blur overlay + scale entrance. All using `--arc-*` custom properties. |
| 1.8 | GSAP entrance animations | ✅ | 10 min | Cards stagger-in on page load with `arc-entrance` class. |
| 1.9 | Chainalysis footer | ✅ | 10 min | "Powered by Chainalysis" badge + product callouts (Address Screening · KYT · Reactor). |
| 1.10 | Rename to ArcSwap | ✅ | 5 min | Global rename throughout file. Hub page `defaultBrand` updated. Brand swap script updated. |

**Files modified:** `demochain.html`, `compliance-cove.html` (hub entry)  
**Products featured:** Address Screening, KYT, Reactor  
**Integration points:** Reactor deep links in screening results, Address Screening workflow, KYT deposit/withdraw monitoring

---

### 2. 🏗️ Hexagate — Protocol & Wallet Security `hexagate-demo.html`
**Priority:** 🔥 HIGH — Only cove covering a unique product (Hexagate)  
**Status:** ✅ Built, then **reworked to live per Hexagate team feedback (ShieldFi)**.  
**Goal:** A protocol and wallet security console showing live Hexagate Monitoring + Gate DSL, with Chainalysis Address Screening.  
**Why:** Hexagate is a newer acquisition with growing sales motion. No other cove covers protocol/wallet *security*.

**v2 rework (live Hexagate, per Hexagate team feedback):**
- **New `cove-hexagate` workflow** (`workflow/hexagate.py`, deployed to $LATEST, org-public). Modes: `gate_validate`, `create_monitor` (auto-cleans prior demo monitors), `list_monitors`, `list_events`, `analyze_transaction`. Requires Hexagate connected in Chainalysis Connections (now connected).
- **Removed Hexagate address analysis**; replaced with a live **Address Screening** tab (`demochain-address-screen`).
- **De-emphasized Gate Signer / approvals** (removed). **Monitoring is the centerpiece.**
- **Monitoring panel (live Monitor API):** Protocol/Stablecoin and Exchange use cases. **Create a real monitor** on a contract or hot wallet, and see it join the org's live monitors (`list_monitors`).
- **Gate DSL panel (live):** edit contract + threshold, see the gate code, **Run on live chain data** → real `validate_gate` returns the block, transfer count, and computed volume, then the comparison and PASS/breach result. Lower the threshold to trigger a real alert. This is the customizable "input → query on-chain data → comparison → result" story.
- Sandbox-safe fallbacks; brand-swap + analytics; em-dash free.
- **Use cases:** Protocol/Stablecoin (monitor contracts), Exchange (monitor hot wallets).

| # | Task | Status | Effort | Notes |
|---|------|--------|--------|-------|
| 2.1 | Design the dashboard layout | ⬜ | 30 min | Protocol admin dashboard: TVL card, active contracts list, aggregate risk score, alert feed. Reference banking demo's multi-section approach. |
| 2.2 | Build TVL & contract overview | ⬜ | 45 min | Hero stats (TVL, active contracts, monitored wallets), contract cards with risk scores, deployment info, and audit status. |
| 2.3 | Transaction simulation panel | ⬜ | 60 min | "What happens if this tx executes?" — input a transaction, show simulated state changes, balance diffs, token approvals, potential risks. This is Hexagate's signature feature. |
| 2.4 | Real-time alert feed | ⬜ | 45 min | Animated alert stream showing detected threats: reentrancy attempts, price oracle manipulation, suspicious unlimited approvals, flash loan attacks. Auto-populates with realistic mock data. |
| 2.5 | Wallet risk classification | ⬜ | 30 min | Address lookup that classifies wallets interacting with the protocol — shows behavioral patterns, risk tier, interaction history. |
| 2.6 | Integrate with addresses.js | ⬜ | 15 min | Add Hexagate-relevant addresses to the shared address library. Add `renderAddressPicker()` to the wallet classification input. |
| 2.7 | Add to hub page | ⬜ | 10 min | Update `compliance-cove.html` → change Hexagate entry `status` to `'active'`, set `url` to `'hexagate-demo.html'`, add `defaultBrand`. |
| 2.8 | Add brand customization | ⬜ | 15 min | Support `?brand=` URL param for prospect customization (e.g., `?brand=Aave` or `?brand=Uniswap`). Default brand: "ShieldFi" or similar. |

**Files to create:** `hexagate-demo.html`  
**Files to modify:** `compliance-cove.html` (hub registry), `addresses.js` (new addresses)  
**Products featured:** Hexagate (address risk scoring, transaction simulation, real-time monitoring, wallet classification)  
**Integration points:**
- Hexagate API (via Chain skill) for live address risk scoring
- Reactor deep links for flagged addresses
- Address Screening cross-reference for wallet classification

---

## 🔗 Cross-Cutting — Reactor Links

**Priority:** 🔥 HIGH — Applies to all demos  
**Effort:** ~45 min across all demos  
**Goal:** Add consistent "Open in Reactor →" links next to every displayed address

### Reactor URL Pattern

**Confirmed URL patterns (from ADR - KYT Graph Service - Deep Link):**

| Pattern | Usage |
|---------|-------|
| `https://reactor.chainalysis.com/graph-v2/{graphId}` | Opens a saved/pre-created investigation graph |
| `https://api.chainalysis.com/api/kyt/v2/graphs/alerts/{alertId}` | KYT API — creates a Reactor graph for a KYT alert |
| `https://kyt.chainalysis.com/alerts/graph-v2?alertIds={alertId}` | KYT deep link — lazily creates a graph on click |
| `https://reactor.chainalysis.com` | Reactor app home — used for demo "Investigate in Reactor" links |

> **⚠️ No address-based search URL exists in Reactor's routing.** The old pattern `/graphs/reactor/{NETWORK}/{ADDRESS}` was invalid.
>
> ✅ **RESOLVED (v3): every Reactor button now creates a REAL graph.** All decorative homepage links removed. Each demo's `openInReactor(address, network, btn)` calls the `arcswap-reactor-graph` workflow, which builds an actual investigation graph and opens its live `graph-v2/{id}` URL. On sandbox/preview failure it shows an inline tooltip (NO homepage fallback). Applied across: demochain, exchange, gaming, merchant, nft, remittance, banking, screener, stablecoin. (atm, hexagate, prediction, trading-firm have no address-display surfaces / no Reactor links.)

### Shared Helper Function

Create a unified `reactorLink(address, network)` function. Currently duplicated across 3 files — should be either:
- Added to `addresses.js` (already a shared script) so all demos get it, OR
- Duplicated consistently in each standalone HTML file (current pattern)

The link renders as a small purple pill/button:
```
[🔮 Open in Reactor →]
```
Style: `color: #a855f7`, subtle background, hover effect. Already implemented in `demochain.html`, `gaming-demo.html`, and `exchange-demo.html`.

### Placement Per Demo

| # | Demo | File | Where the link appears | Status |
|---|------|------|----------------------|--------|
| R.1 | DeFi Trading (ArcSwap) | `demochain.html` | Screening results (next to address) | ✅ Fixed — links to reactor.chainalysis.com |
| R.2 | Banking | `banking-demo.html` | Stage 4: Reactor trace panel link | ✅ Fixed — was hardcoded to invalid path |
| R.3 | Gaming | `gaming-demo.html` | Connected wallet in dashboard + screening results | ✅ Fixed URL |
| R.4 | Exchange | `exchange-demo.html` | Linked wallet in onboarding Step 3 | ✅ Fixed URL |
| R.5 | ATM | `atm-demo.html` | Withdrawal destination address | ⬜ No Reactor link yet |
| R.6 | Remittance | `remittance-demo.html` | Recipient wallet address | ✅ Fixed URL |
| R.7 | Merchant | `merchant-demo.html` | Customer payment address | ⬜ No Reactor link yet |
| R.8 | NFT / Marketplace | `nft-demo.html` | Connected wallet on profile | ⬜ No Reactor link yet |
| R.9 | Hexagate (new) | `hexagate-demo.html` | Wallet classification results | ⬜ Build with new demo |

---

## 🔗 Cross-Cutting — Live KYT Integration

**Status:** 🟢 Live on Exchange (VaultX) deposit, ATM (CoinVault) withdraw, Remittance (SwiftBridge) send, ArcSwap (DeFi) withdraw, and Gaming (NexusArena) cash-out.
**Workflow:** `cove-kyt-screen` (`workflow/kyt_screen.py`, deployed to $LATEST). Uses `REACTOR_API_KEY`. Two shapes:
- `mode:"transfer"` — monitor a real deposit (`transferReference="txhash:address"`, `direction`). Returns real alerts + exposure.
- `mode:"withdrawal"` — pre-screen an outgoing address (address only). Returns exposure + fraud + alerts.

Writes are namespaced under the `compliance-cove-demo` user in the shared KYT org (idempotent identifiers). Poll until `updatedAt`; the `/alerts` endpoint is the reliable data source (level/service/exposureType/categoryId + alert `externalId` → KYT deep link). The `/exposures/direct` endpoint 404s — render from alerts.

**Required-field gotchas:** withdrawal-attempts also need `assetAmount` + `attemptTimestamp`; network is the enum (`ETHEREUM`); token transfers must register with the correct `asset` (USDT/USDC), not ETH.

**Curated library:** `kyt-transactions.js` — validated against live KYT:
| Scenario | Shape | Live outcome |
|---|---|---|
| Clean (self-custody) | withdrawal | CLEARED — "no alert, source clean" |
| Crypto ATM (RockItCoin, BTC) | transfer | No hard alert → policy-based **Enhanced Due Diligence** (high-risk category) |
| Sanctioned (Swapster.fi, USDT) | transfer | SEVERE |
| Sanctioned (Heleket.com, USDT) | transfer | SEVERE |

> **Org alert-rule reality:** this shared KYT org only hard-alerts on exchanges (LOW/MED), mixing/sanctioned/illicit (MED/SEVERE). Gambling & ATM do NOT alert, and KYT doesn't return source attribution for non-alerting transfers. So the ATM "middle" tier is built as an authentic **EDD** scenario: KYT monitors the transfer (real usd/processing) + Chainalysis attributes the source as a crypto ATM (real, via Data Solutions) → policy routes high-risk categories to EDD. Distinct from a sanctioned hard alert. (Tornado was dropped — it's sanctioned, which contradicted a mid-risk story.)
>
> **Deep links:** result shows BOTH the Reactor alert graph (`graphLink` = `/alerts/graph-v2?alertIds={id}`, alert-specific, opens the alert in Reactor) and the KYT alert (`alertLink` = `/alerts/{alertId}`, opens the alert detail directly).

**Sourcing tx hashes:** Data Solutions `cross_chain.transfers_clustered` (filter by risky `sender_name`/`sender_category`) → register candidates → keep validated outcomes. Note: avoid `asset_symbol='ETH'` as a sole broad predicate (non-selective → 400); keep `sender_name IS NULL` style filters selective.

**Withdrawal scenarios** (`KYT_WITHDRAWALS` in `kyt-transactions.js`, all validated):
| Scenario | Shape | Outcome |
|---|---|---|
| Clean destination (BTC) | withdrawal | CLEARED |
| Sanctioned destination — Chatex (BTC) | withdrawal | SEVERE → blocked before send |
| **Indirect — continuous monitoring** (BTC tx → Chatex) | transfer (sent) | clean at send → **KYT later raises SEVERE/INDIRECT** post-send |

✅ **ATM (CoinVault) rolled out:** withdraw flow has a sample-destination picker. Clean → Address-Screening approved → sent. Sanctioned → blocked. Indirect → screens clean at send, then `confirmSend` calls `cove-kyt-screen` (transfer/sent) and the "KYT Monitoring Active" box flips to a **post-send continuous-monitoring alert** (funds reached OFAC-sanctioned Chatex.com) with Reactor-graph + KYT-alert links. The continuous-monitoring tx hash was provided by the user.

✅ **Remittance (SwiftBridge) rolled out:** the **send** flow now has a "Sample recipient (KYT scenarios)" picker reusing `KYT_WITHDRAWALS`. Clean → Address Screening clears → delivered. Sanctioned (Chatex) → Address Screening blocks before funds leave the corridor. Indirect → screens clean at send (Low), the success card shows a green **"KYT Continuous Monitoring Active"** box, then a **⏱ 5 WEEKS LATER — ONGOING CORRIDOR MONITORING** divider with steps 5–6 calls `cove-kyt-screen` (transfer/sent) and flips the box to a red **continuous-monitoring alert** (OFAC-sanctioned Chatex.com, SEVERE/indirect) with Reactor-graph + KYT-alert links. Address Screening remains the point-in-time gate; KYT is additive. Sandbox-safe fallback (validated SEVERE) when the API can't be reached from preview.

✅ **ArcSwap (DeFi, `demochain.html`) rolled out:** the **Withdraw** modal's old mock "Safe/Risky" buttons were replaced with a "Sample destination (KYT scenarios)" picker + a single **Pre-Screen & Withdraw** action. Clean → live Address Screening clears → broadcast. Sanctioned (Chatex) → blocked. Indirect → screens clean at send (Low), an approved result shows a green **"KYT Continuous Monitoring Active"** box, then a **⏱ 6 WEEKS LATER** divider (steps 5–6) calls `cove-kyt-screen` (transfer/sent) and flips the box to a red continuous-monitoring alert with Reactor-graph + KYT-alert links. Sandbox-safe: live Address Screening failures fall back to each scenario's validated outcome (clean/Severe) with an inline sandbox note. Redundant generic `withdrawAddress` picker removed (KYT dropdown covers it); `addressInput` picker kept.

✅ **Gaming (NexusArena, `gaming-demo.html`) rolled out:** the **cash-out** flow gained a "Cash-out destination (KYT scenarios)" picker that overrides the destination wallet. Step 2 ("Re-screen destination") is now a live Address Screening gate; a sanctioned destination routes to a new **Withdrawal Blocked** screen (funds never leave). Indirect → cash-out completes with a green monitoring box, then the **⏱ 6 WEEKS LATER** continuation calls `cove-kyt-screen` and flips it to a red continuous-monitoring alert with Reactor + KYT links. Sandbox-safe validated fallbacks. Address Screening remains the point-in-time gate; KYT is additive.

**Next:** standalone Live KYT Screener SA tool + make the KYT Explainer interactive. Optionally add KYT to the Stablecoin mint gate (additive to Address Screening). (Address Screening is NOT replaced anywhere — KYT is additive.)

---

## 📋 Coming Soon Demos — Full Backlog

### 3. 🔍 Insurance Claim Verification `insurance-demo.html`
**Priority:** Medium — Unique use case (investigations, not monitoring)  
**Effort:** ~4–5 hours  
**Products:** Reactor, KYT, Address Screening  
**Industry:** Insurance / Investigations

**Concept:** An insurance investigations console for crypto-related claims. An adjuster receives a claim, traces the crypto assets, verifies fund origins, and identifies fraud patterns.

| # | Task | Effort | Notes |
|---|------|--------|-------|
| 3.1 | Claims intake screen | 45 min | Claim form with policy number, claimant info, wallet addresses involved |
| 3.2 | Reactor-style fund tracing view | 60 min | Simplified graph visualization showing fund flow from claimant's wallet |
| 3.3 | KYT screening of claim addresses | 30 min | Screen all addresses in the claim, show risk exposure |
| 3.4 | Fraud pattern detection panel | 45 min | Flag suspicious patterns: rapid movement, mixer usage, round-trip transactions |
| 3.5 | Adjuster decision + report | 30 min | Disposition screen with approve/deny/escalate + exportable report |

**Integration points:**
- Reactor deep links (investigate flagged addresses)
- Address Screening API (via workflow) for live screening
- KYT for transaction monitoring on claim addresses
- Could link to Data Solutions for broader exposure analysis

---

### 4. 👥 P2P Marketplace `p2p-marketplace-demo.html`
**Priority:** Medium — Common prospect type, but Address Screening + KYT overlap with other demos  
**Effort:** ~3–4 hours  
**Status:** ✅ Complete — built as **Peerly** (light theme, green accent). Live on the hub. Now includes a **Buy and Sell side** with **per-offer pre-screen trust badges** and a right-rail live chat.  

**v2 additions:** (a) **Buy/Sell toggle** on the marketplace. Buy mode screens the seller (source of funds) at trade start; **Sell mode screens the buyer wallet (destination) before your crypto is released**, and a sanctioned buyer is blocked so funds never leave escrow. (b) **Per-offer pre-screen trust badges** (Cleared / Enhanced review / Sanctioned) on every listing, the trade setup, and the chat header, so trust is visible before committing funds (a natural compliance talking point). (c) The trade **chat moved to the right rail**; the Compliance Audit Trail and Products cards were removed for a cleaner layout (dispute evidence is still assembled from state).  
**Products:** Address Screening ★, KYT, Reactor  
**Industry:** P2P Exchange

**Concept:** A peer-to-peer trading platform (like Paxful/LocalBitcoins) where buyers and sellers trade directly. Focus on counterparty screening before trade and escrow release.

**Built — the complete compliance journey:** Landing → Marketplace (offer board, asset filter, trader reputation) → Trade flow → About (presenter workflow). Each offer embeds a counterparty wallet with a known outcome. The trade screen runs a real end-to-end journey with a live **Compliance Audit Trail** side panel and a **Products in this journey** card:
1. **Counterparty screening** — live `demochain-address-screen` on the seller wallet (risk gauge + exposure bars + Reactor link). Clean proceeds, Medium proceeds with enhanced monitoring, **Severe/High blocks the trade before any escrow**.
2. **Escrow lock (KYT)** — seller funds escrow; transfer registered + monitored; buyer marks fiat sent.
3. **Release gate (KYT)** — payout pre-screened before release, then escrow released.
4. **Continuous monitoring** — the `clean_exit_88` offer reuses the validated indirect tx: releases clean, then a **6 WEEKS LATER** divider calls `cove-kyt-screen` and flips the monitoring box to a SEVERE indirect alert (Chatex) with Reactor + KYT links.
5. **Dispute flow** — `Raise dispute` modal assembles the Chainalysis evidence already collected and files a report (freeze + return + SAR when flagged).

Sandbox-safe validated fallbacks throughout; brand-swap (?brand=&color=&domain=) + analytics wired; em-dash free copy. **Wired into the hub** (`compliance-cove.html`): status `active`, `defaultBrand: 'Peerly'`, products Address Screening / KYT / Reactor.

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1 | Trade listing board | ✅ | Offer rows with price, margin, limits, payment method, trader reputation, online dot, asset filter |
| 4.2 | Counterparty screening on match | ✅ | Live Address Screening on the seller wallet with risk gauge, identifications, exposure bars, Reactor link |
| 4.3 | Escrow + compliance gate | ✅ | KYT monitors escrow deposit; payout pre-screened before release; sanctioned counterparties blocked pre-escrow |
| 4.4 | Trade chat + dispute flow | ✅ | Live buyer/seller chat on the trade screen with quick-reply chips, seller auto-replies, and a typing indicator. Compliance/system messages post into the thread at key events (blocked trade, post-release alert). Dispute modal auto-assembles Chainalysis evidence (screening, KYT, Reactor, chat transcript) and files a compliance report. |

**Integration points:**
- Address Screening for counterparty wallets
- KYT for monitoring escrow deposits/releases
- Reactor links for flagged counterparties

---

### 5. 💰 Stablecoin Issuer `stablecoin-demo.html`
**Priority:** Medium-High — Hot topic, unique multi-product integration  
**Effort:** ~4–5 hours  
**Status:** ✅ Complete — built as **Meridian / USDM**, light theme, 6-section console. First demo with **Data Solutions as the headline product**.  
**Products:** Data Solutions ★, KYT, Address Screening, Reactor  
**Industry:** Stablecoins / Treasury

**Concept:** An issuer intelligence console (think Circle/Tether). Built sections: (1) Ecosystem Overview — supply by chain + holder type, (2) In/Out Flows — mint vs burn chart, net flow map, cross-chain bridge & swap attribution, (3) Whale/Top-Holder Surveillance with movement alerts, (4) Market Integrity / Peg Watch, (5) Mint/Burn Compliance Gate — **live** Address Screening call (`demochain-address-screen`) with sandbox fallback, (6) Sanctions & Freeze Workflow with audit log. Brand-swap + analytics tracking wired in.

**Polish pass (v2):** Removed dead Reactor homepage links. Added: (a) **Holder Intelligence drawer** — click any holder/whale for cluster, counterparties, exposure; (b) **real Reactor graph creation** via `arcswap-reactor-graph` workflow (drawer + freeze) instead of homepage links; (c) **"View Data Solutions query"** SQL reveals on Flows + Holders panels; (d) **Supply Exposure by Risk Category** panel (Data Solutions); (e) **KYT Monitoring Rules** card.

| # | Task | Effort | Notes |
|---|------|--------|-------|
| 5.1 | Dashboard overview | 45 min | Supply metrics (total supply, mint/burn 24h, top holders), reserve ratio |
| 5.2 | Mint/burn screening | 45 min | Real-time screening of mint requests — block sanctioned addresses |
| 5.3 | Large holder monitoring | 30 min | Entity Monitoring integration — track wallets holding >$1M |
| 5.4 | Exposure heatmap | 45 min | Visual breakdown of holder exposure categories (exchanges, DeFi, sanctioned, etc.) |
| 5.5 | Freeze/blacklist workflow | 30 min | Compliance action to freeze a flagged address |

**Integration points:**
- KYT for mint/burn transaction monitoring
- Entity Monitoring for large holder surveillance
- Address Screening for mint request gates
- Data Solutions for aggregate exposure analysis
- Reactor links for investigating flagged holders

---

### 6. 📊 Prediction Markets `prediction-markets-demo.html`
**Priority:** Low — Niche vertical, single product (Data Solutions)  
**Effort:** ~3–4 hours  
**Products:** Data Solutions  
**Industry:** Prediction Markets

**Concept:** A prediction market platform (like Polymarket) with on-chain wager tracking. Use Data Solutions to detect insider trading patterns, wash trading, and market manipulation.

| # | Task | Effort | Notes |
|---|------|--------|-------|
| 6.1 | Market listing page | 30 min | Active prediction markets with odds, volume, resolution dates |
| 6.2 | Market detail + order book | 45 min | Individual market view with order book, position tracking |
| 6.3 | Data Solutions analytics panel | 60 min | Wash trading detection, unusual volume alerts, whale position tracking |
| 6.4 | Manipulation alert feed | 30 min | Real-time alerts for suspicious patterns (correlated accounts, timing anomalies) |

**Integration points:**
- Data Solutions (Datasets skill) for on-chain analytics queries
- Address Screening for participant wallets
- Reactor links for investigating flagged traders

---

### 7. 📊 Trading Firm / Market Maker `trading-firm-demo.html`
**Priority:** Medium — High-value prospect segment (Cumberland, Jump, Jane Street, Wintermute)  
**Effort:** ~5–6 hours  
**Products:** Hexagate, Data Solutions, KYT, Address Screening  
**Industry:** Trading / Market Making

**Concept:** An institutional crypto trading desk dashboard. Market makers need to monitor smart contract risk on protocols they provide liquidity to, understand token exposure across venues, track counterparty risk, and stay compliant across DeFi and CeFi simultaneously.

| # | Task | Effort | Notes |
|---|------|--------|-------|
| 7.1 | Trading desk dashboard | 60 min | Portfolio overview: positions across venues, PnL, exposure heatmap by token/protocol. Dark theme to match Bloomberg-style trading UIs. |
| 7.2 | Smart contract risk monitor (Hexagate) | 45 min | Real-time monitoring of protocols the firm provides liquidity to. Reentrancy detection, price oracle manipulation, exploit alerts. Show how Hexagate protects LP positions. |
| 7.3 | Token exposure analytics (Data Solutions) | 60 min | Per-token risk profiles: what % of a token's volume touches sanctioned entities, mixers, or darknet markets? Useful for deciding which tokens to make markets in. |
| 7.4 | Cross-venue surveillance | 45 min | Monitor the firm's activity across DEXs and CEXs. KYT tracks transfers between venues. Flag unusual patterns (potential wash trading by counterparties). |
| 7.5 | Counterparty screening | 30 min | Address Screening for every new counterparty wallet the firm interacts with on-chain. Auto-screen LP pool participants. |
| 7.6 | Compliance reporting | 30 min | Exportable compliance summary: screened addresses, flagged transactions, alert history. What the compliance officer shows to regulators. |

**Integration points:**
- **Hexagate** — Smart contract monitoring for protocols the firm LPs into. Transaction simulation before large trades.
- **Data Solutions** — Token-level analytics, on-chain volume attribution, exposure by category across the firm's trading universe.
- **KYT** — Transfer monitoring across all venues. Alert on suspicious counterparty activity.
- **Address Screening** — Screen every new on-chain counterparty. Gate new protocol integrations.
- **Reactor** — Deep investigation when alerts fire. Trace fund flows from flagged counterparties.

**Why this matters:** Market makers are high-value, multi-product prospects. They touch every Chainalysis product. A single demo that shows the full platform story for their use case is more compelling than showing 4 separate product demos.

---

## 🛠️ Infrastructure & Polish Backlog

### Shared Components

| # | Task | Priority | Effort | Status | Notes |
|---|------|----------|--------|--------|-------|
| I.1 | Consolidate `reactorLinkHtml()` into `addresses.js` | High | 20 min | ⬜ | Currently duplicated in 3 files. Add to shared script. |
| I.2 | Add more addresses to `addresses.js` | Medium | 15 min | ⬜ | Add BTC addresses (currently ETH-only), add Hexagate-relevant addresses |
| I.3 | Add `addresses.js` script tag to all demos | Medium | 10 min | ⬜ | Currently no demos load it via `<script src>` — they use inline address lists |
| I.4 | Standardize branding customization | Low | 30 min | ⬜ | Some demos handle `?brand=` differently. Create a shared `applyBranding()` helper. |
| I.5 | Add usage tracking to new demos | Low | 10 min | ⬜ | See `tracking/apps-script.js` and `tracking/setup.md` for the Google Sheets tracking setup |

### Quality & Consistency

| # | Task | Priority | Effort | Status | Notes |
|---|------|----------|--------|--------|-------|
| Q.1 | Audit all demos for light/dark mode | Medium | 30 min | ⬜ | Banking = forced light ✅, Remittance = forced light ✅, ArcSwap = forced dark ✅ (intentional), others = check |
| Q.2 | Responsive audit (mobile) | Low | 45 min | ⬜ | Most demos are desktop-focused. Basic mobile breakpoints exist but haven't been tested. |
| Q.3 | Add loading/skeleton states | Low | 30 min | ⬜ | Some demos jump between screens abruptly. Add skeleton loaders for polish. |
| Q.4 | Standardize nav bar pattern | Low | 20 min | ⬜ | Each demo has slightly different nav implementation. Consider a shared pattern. |

---

## 🔧 SA Power Tools — Demo Enhancement Suite

Tools that make **every existing demo** more powerful during live customer calls.

### T1. 🎨 Prospect Branding Studio `branding-studio`
**Priority:** 🔥 HIGH — Replaces the basic ⚙️ gear prompt  
**Effort:** ~3–4 hours  
**Status:** 🟡 In progress  
**Goal:** A rich branding panel where SAs input company name, pick a brand color, and optionally add a logo URL. The demo regenerates with full custom branding — nav, cards, footer, chart accents.

| # | Task | Status | Effort | Notes |
|---|------|--------|--------|-------|
| T1.1 | Build branding overlay panel on hub page | ✅ | 1.5 hr | Paint palette icon on each card footer → opens modal with company name, color picker (6 presets + custom hex + native picker), logo URL field. Live preview. Apply & Launch / Reset / Cancel actions. Keyboard: Enter=apply, Esc=close. |
| T1.2 | Extend `?brand=` params to include `&color=` and `&logo=` | ✅ | 30 min | Hub page card onclick now passes `?brand=X&color=%23hex&logo=URL`. ArcSwap's brand-swap script updated to handle all three — swaps text, overrides `--primary` CSS var, replaces nav logo SVG with img. |
| T1.3 | Shared `applyBranding()` helper | ⬜ | 30 min | ArcSwap has the full brand-swap logic. Other demos still use name-only swap. Need to propagate the color+logo handling to all demos. |
| T1.4 | Preview in hub card | ✅ | 20 min | After applying branding, card footer shows a colored dot + company name. Card banner gradient tints to the brand color. Reset restores defaults. |

---

### T2. 📋 SA Presenter Mode + Guided Tour `tour.js`
**Priority:** 🔥 HIGH — Turns every demo into a guided pitch  
**Effort:** ~4–5 hours  
**Status:** 🟡 Hub landing tour shipped. Per-demo tours not started (placeholder saved at `tracking/tour.js`)  
**Goal:** React Joyride-style guided walkthrough in vanilla JS. SAs/CSMs/AEs can practice the demo flow before customer calls. A "?" button in the nav triggers the tour.

✅ **Hub guided tour shipped (`compliance-cove.html`):** the top-right "Solutions Architecture" text was replaced with an **(i) "How to use"** info button that launches a JoyRide-style tour (native JS/CSS, no deps). Spotlight cutout via a single `box-shadow: 0 0 0 9999px` element, a floating tooltip that auto-positions (top/right/bottom/left with viewport clamping), step dots + counter, Next/Back/Skip/Finish, and keyboard nav (→ ← Esc). Five steps walk the flow: welcome → filter the coves → pick a cove → brand it (Branding Studio icon) → launch in a new tab. The bottom "How to Use These Demos" boxes were removed and that copy was folded into the landing hero. Fires `tour_started` / `tour_ended` analytics. The engine is a good basis for the per-demo `tour.js` below.

> **Copy convention:** No em-dashes in any cove copy. A sweep removed all `—` across every demo HTML + `addresses.js` + `kyt-transactions.js` (inline em-dashes → commas, decorative option placeholders stripped, value placeholders → `-`, analytics `title.split` updated). Keep new copy em-dash free.

**Architecture (vanilla JS, no React needed):**
- `tourSteps[]` array per demo — each step defines `target` (CSS selector), `title`, `text`, `position`
- Floating tooltip div that positions itself next to the target element
- Backdrop overlay with a CSS cutout/spotlight around the highlighted element
- Next / Back / Skip / Finish buttons + step counter (1/6, 2/6...)
- Keyboard navigation: → next, ← back, Esc skip
- Spotlight effect: darken everything except the target element

| # | Task | Status | Effort | Notes |
|---|------|--------|--------|-------|
| T2.1 | Build `tour.js` engine | ⬜ | 2 hr | ~200 lines vanilla JS. Tooltip positioning, backdrop with cutout, keyboard nav, step counter. Inspired by React Joyride (https://react-joyride.com/). |
| T2.2 | Add "?" tour button to nav | ⬜ | 15 min | Small help icon in each demo's nav bar. Calls `startTour(steps)`. |
| T2.3 | Write tour steps for ArcSwap | ⬜ | 30 min | Steps: Connect Wallet → Address Picker → Screening Results → Swap Card → Deposit → Withdraw. |
| T2.4 | Write tour steps for Banking | ⬜ | 30 min | Steps for the 5-stage journey. |
| T2.5 | Write tour steps for Exchange | ⬜ | 30 min | Steps: Create Account → KYC → Link Wallet → First Deposit. |
| T2.6 | Propagate to remaining demos | ⬜ | 1 hr | Gaming, Merchant, ATM, Remittance, NFT, Hexagate, Prediction Markets. |

---

### T3. 🔍 Live Address Screener `screener.html`
**Priority:** 🔥 HIGH — Quick win, reuses existing code  
**Effort:** ~2 hours  
**Status:** ✅ Complete  
**Goal:** ~~Standalone utility page where SAs paste any address during a call and get polished Chainalysis screening results.~~ **DONE**

| # | Task | Status | Effort | Notes |
|---|------|--------|--------|-------|
| T3.1 | Build screener page | ✅ | 1.5 hr | Clean dark UI with animated particle background. Shows: animated risk gauge, risk badge + reason, address details (type, cluster, category), identifications with severity cards, exposure breakdown with colored bars + direct/indirect tags, triggered rules with severity pills. Reactor graph link via workflow. Skeleton loading state. Sandbox detection. |
| T3.2 | Add to hub page | ✅ | 15 min | "SA Tools" section added below demo grid with screener card. Gradient banner (indigo→cyan). |
| T3.3 | History panel | ✅ | 30 min | Shows last 8 screened addresses in session with risk dots, cluster names, and click-to-re-screen. |

---

### T4. 🎯 Scenario Presets
**Priority:** Medium — Enhances demo storytelling  
**Effort:** ~2 hours  
**Status:** ⬜ Not started  
**Goal:** Named compliance scenarios that tell a story, not just "safe vs risky." Each pre-fills an address and sets narrative context.

Scenarios: Clean Exchange User, Unnamed Service (enhanced review), OFAC Sanctioned Entity, Ransomware Proceeds, Stolen NFT, Dust Attack Victim.

---

### T5. 📈 Demo Analytics Dashboard `analytics.html`
**Priority:** 🔥 HIGH — Understand what's working  
**Effort:** ~3–4 hours  
**Status:** ⬜ Not started  
**Goal:** Replace the basic Slack webhook with a proper analytics page. Track which demos are opened, how long SAs spend, which scenarios/addresses are used, and branding customizations.

| # | Task | Status | Effort | Notes |
|---|------|--------|--------|-------|
| T5.1 | Design analytics dashboard | ⬜ | 1 hr | Chart.js charts: demo usage over time, most popular demos, avg session duration, top customized brands. |
| T5.2 | Event collection | ⬜ | 1 hr | Lightweight JS tracker in each demo. Posts events (page view, screen change, address screened, brand customized) to a backend. |
| T5.3 | Storage backend | ⬜ | 1 hr | Options: MongoDB collection via workflow endpoint, or a simple Chain workflow that appends to a Google Sheet. MongoDB preferred for query flexibility. |
| T5.4 | Add analytics page to hub | ⬜ | 30 min | "📈 Analytics" link in hub footer. Only visible to internal users. |

**Storage options considered:**
- **MongoDB** (preferred) — flexible queries, time-series aggregation, scales well. Connect via a workflow that proxies writes/reads.
- **Google Sheets** — zero infra, already have tracking setup for Slack. Limited query capability.
- **Workflow + JSON file** — simplest, but no concurrent write safety.

---

### T6. 🏛️ Compliance Command Center (meta-demo)
**Priority:** Medium — Platform story, not industry-specific  
**Effort:** ~5–6 hours  
**Status:** ⬜ Not started  
**Goal:** Single dashboard showing ALL Chainalysis products working together. For prospects that don't fit one industry vertical. Shows the platform story.

---

### T7. 🤖 AI Demo Narrator
**Priority:** Low — Impressive but complex  
**Effort:** ~5–6 hours  
**Status:** ⬜ Not started  
**Goal:** AI sidebar that generates real-time commentary adapted to the prospect's industry and regulatory context. Uses the AI skill with prospect context.

---

### T8. 💳 Crypto Payroll / Treasury Demo
**Priority:** Low — Growing use case  
**Effort:** ~4 hours  
**Status:** ⬜ Not started  
**Goal:** Batch withdrawal screening, payroll address monitoring, VASP identification for exchange-bound payments. Products: KYT, Address Screening, VASP Risking.

---

### T9. ⚖️ Travel Rule Compliance Demo
**Priority:** Low — Major pain point, niche audience  
**Effort:** ~4 hours  
**Status:** ⬜ Not started  
**Goal:** VASP-to-VASP transfer flow with originator/beneficiary data, counterparty risk scoring, regulatory filing.

---

## 🎯 Prioritization Summary

### Short-Term (Next 1–2 Sessions)
1. ~~**📘 KYT API Explainer** (E1)~~ ✅ · ~~**🔍 Screening Explainer** (E2)~~ ✅ · ~~**📈 Analytics** (T5)~~ ✅
2. ~~**ArcSwap Polish** (Task 1)~~ ✅ · ~~**Branding Studio** (T1)~~ ✅ · ~~**Address Screener** (T3)~~ ✅
3. **🏗️ Hexagate Demo** (Task 2) — ~4–6 hrs — 🟡 In development — DeFi protocol security dashboard

### Medium-Term (Next 3–5 Sessions)
5. **📋 SA Presenter Mode** (T2) — ~4–5 hrs — Guided pitch for every demo
6. **🎯 Scenario Presets** (T4) — ~2 hrs — Named compliance stories
7. **🏗️ Hexagate Demo** (Task 2) — ~4–6 hrs — New product coverage
8. **📊 Trading Firm / Market Maker** (Task 7) — ~5–6 hrs — Multi-product, high-value prospect segment
9. **🏛️ Compliance Command Center** (T6) — ~5–6 hrs — Platform story demo
10. **Infrastructure cleanup** (I.1–I.5) — ~1.5 hrs — Tech debt

### Long-Term (Backlog)
10. ~~**Stablecoin Issuer** (Task 5)~~ ✅ Built (Meridian/USDM) — Data Solutions headline demo
11. **Insurance Claims** (Task 3) — ~4–5 hrs
12. **🤖 AI Demo Narrator** (T7) — ~5–6 hrs
13. **💳 Crypto Payroll** (T8) — ~4 hrs
14. **⚖️ Travel Rule** (T9) — ~4 hrs
15. ~~**P2P Marketplace** (Task 4)~~ ✅ Built (Peerly) — counterparty screening + escrow + continuous monitoring
16. **Prediction Markets** (Task 6) — ~3–4 hrs

---

## 📐 Architecture Reference

### File Structure
```
compliance-cove.html      # Hub page — demo card grid (data-driven from `demos[]` array)
demochain.html            # DeFi Trading (ArcSwap) — page-view architecture, forced dark, canvas particle bg
banking-demo.html         # Banking — 5-stage scroll journey (forced light mode)
merchant-demo.html        # Merchant Services (Basecamp) — page-view architecture
exchange-demo.html        # Exchange Onboarding (VaultX) — screen architecture
nft-demo.html             # Digital Marketplace (NovaMint) — page-view architecture
atm-demo.html             # Crypto ATM (CoinVault) — screen architecture
gaming-demo.html          # Gaming (NexusArena) — screen architecture
remittance-demo.html      # Remittance (SwiftBridge) — screen architecture
screener.html             # Live Address Screener — SA tool for ad-hoc address risk assessment
addresses.js              # Shared address library + picker UI component
workflow/workflow.py       # Address Screening backend (Chainalysis Workflow)
workflow/reactor-graph.py  # Reactor graph creation (creates graph-v2 URL on demand)
tracking/apps-script.js   # Google Sheets usage tracking
tracking/setup.md          # Tracking setup instructions
ROADMAP.md                # ← This file
```

### Design Patterns
- **Styling:** `/assets/pages-theme.css` (Dialog) + Google Font `Inter`
- **Animations:** `/assets/gsap.min.js` (GSAP) for entrances, counters, particles
- **Charts:** `/assets/chart.min.js` (Chart.js) where needed
- **Navigation:** Multi-screen (`showScreen()`) or multi-page (`showPage()`) within single HTML files
- **Hub linking:** `buildPageUrl(filePath)` resolves demo URLs within Chain's session-scoped page system
- **Branding:** `?brand=CompanyName` URL param swaps brand name throughout on load
- **Address picker:** `renderAddressPicker('inputId')` from `addresses.js` — categorized dropdown

### Adding a New Demo (Checklist)
1. Create `{name}-demo.html` following existing patterns
2. Include `/assets/pages-theme.css`, Inter font, GSAP
3. Add `?brand=` support with a default brand name
4. Add `renderAddressPicker()` for address inputs
5. Add `reactorLinkHtml()` for address displays
6. Update `compliance-cove.html` → `demos[]` array: set `status: 'active'`, add `url`, `defaultBrand`
7. Update `addresses.js` if new curated addresses are needed
8. Update this `ROADMAP.md` to mark tasks complete
9. Push to GitHub: `Bilal-Blockchain/compliance-cove`
