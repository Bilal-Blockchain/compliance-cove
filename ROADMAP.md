# Compliance Cove - Roadmap

> **Purpose:** Source of truth for the project. New Chain sessions should read this first.
>
> **How to use:** Tell Chain: _"Read ROADMAP.md and let's work on the next priority."_
>
> **Last updated:** June 25, 2026

---

## Current state - shipped

All 15 industry demos and 3 SA tools are **live**. Every hub card is active. All 8 backing workflows are org-public.

| Cove | File | Example brand | Headline products |
|---|---|---|---|
| Exchange Onboarding | `exchange-demo.html` | VaultX | Address Screening, KYT, VASP Risking |
| DeFi Trading | `demochain.html` | ArcSwap | Address Screening, KYT, Reactor |
| Banking | `banking-demo.html` | (neutral) | VASP Risking, Entity Monitoring, KYT, Data Solutions, Alterya |
| Merchant Services | `merchant-demo.html` | Basecamp | KYT, Address Screening |
| Crypto ATM | `atm-demo.html` | CoinVault | KYT, Address Screening |
| Remittance | `remittance-demo.html` | SwiftBridge | KYT, Address Screening |
| Trading Firm | `trading-firm-demo.html` | QuantDesk | Hexagate, Data Solutions, KYT, Address Screening |
| Stablecoin Issuer | `stablecoin-demo.html` | Meridian | Data Solutions, KYT, Address Screening, Reactor |
| Protocol & Wallet Security | `hexagate-demo.html` | ShieldFi | Hexagate, Address Screening |
| Gaming | `gaming-demo.html` | NexusArena | Address Screening, KYT |
| Prediction Markets | `prediction-demo.html` | ForecastX | Data Solutions |
| Digital Marketplace | `nft-demo.html` | NovaMint | Address Screening |
| P2P Marketplace | `p2p-marketplace-demo.html` | Peerly | Address Screening, KYT, Reactor |
| Insurance Claims | `insurance-demo.html` | ChainGuard | Reactor, Address Screening, Data Solutions |
| Tokenized Securities / RWA | `rwa-demo.html` | EquiChain | Data Solutions, Address Screening, KYT, Entity Monitoring, Reactor |

**SA tools:** `screener.html` (Live Address Screener), `screening-explainer.html` and `kyt-explainer.html` (API walkthroughs).

**Workflows (all org-public):** `demochain-address-screen`, `cove-kyt-screen`, `arcswap-reactor-graph`, `cove-insurance-graph`, `cove-hexagate`, `cove-token-intel`, `cove-rwa-landscape`, `compliance-cove-analytics`.

**Distribution:** see `PUBLISH.md` (Holder Session model + Confluence pointer). Public page lives in the Confluence SAT space under the Demo and POV folder.

---

## What's next

| Priority | Item | Notes |
|---|---|---|
| 🔥 | **SA Presenter Mode (T2)** | Guided tours now ship on both API explainer pages (request, run, response walkthrough). A self-contained, additive engine lives in `tracking/tour.js`: define `window.COVE_TOUR_STEPS=[{target,title,text,placement}]` then include the snippet, optional `#coveTourTrigger` element becomes the launch button, else a floating pill is added. Remaining: per-demo tours (wire the trigger into each demo's nav). |
| 🔥 | **Scenario Presets (T4)** | Named compliance stories for the Address Screener (Clean Exchange User, OFAC Sanctioned, Ransomware Proceeds, etc.). |
| Med | **Analytics polish (T5)** | `analytics.html` exists and reads `compliance-cove-analytics`. **Admin-only** by design (reads the usage Google Sheet via the caller's own Google connection). Broadening to all users would need a shared service identity. |
| Med | **More real Reactor investigations** | Apply the `cove-insurance-graph` pattern (attributed stolen-funds clusters + annotation edges) to other demos. |
| Med | **Compliance Command Center (T6)** | Platform-story meta-demo for prospects that do not fit one vertical. |
| Low | **AI Demo Narrator (T7)**, **Crypto Payroll (T8)**, **Travel Rule (T9)** | Backlog verticals/features. |
| Low | **Infra cleanup (I.1-I.3, I.5)** | Consolidate `reactorLinkHtml()` into `addresses.js`; add BTC addresses; load `addresses.js` via `<script src>` instead of inline lists. |

---

## Key learnings (carry these forward)

**Real investigation cases**
- Use either a real tx hash, OR Chainalysis-attributed stolen-funds clusters (`utils.entities WHERE entity_category='stolen funds'` - hundreds: Atomic Wallet, AlphaPo, AscendEX, plus DeFi exploits).
- Do NOT pattern-match "victim → cashout" flows on-chain; that surfaces high-volume laundering services, not clean scammer wallets.

**Reactor graphs**
- `add_cluster` alone does NOT draw edges when funds went through DEXs/mixers/hops (Reactor only auto-draws direct transfers). Always add explicit `add_annotation_edge` arrows.
- Build in two phases: nodes first (`add_cluster` + `execute_commands`), then edges using the node IDs.
- To show a named exchange as the cashout endpoint, add the exchange's **cluster root address** (not the deposit address, which renders unattributed).

**KYT (`cove-kyt-screen`)**
- Modes: `transfer` (monitor a real deposit/send) and `withdrawal` (pre-screen an address). `/alerts` is the reliable data source; `/exposures/direct` 404s.
- This shared org only hard-alerts on exchanges (LOW/MED) and mixing/sanctioned/illicit (MED/SEVERE). Gambling/ATM do not alert, so the ATM tier is built as an Enhanced Due Diligence story.
- Withdrawal-attempts need `assetAmount` + `attemptTimestamp`; register token transfers with the correct `asset` (USDT/USDC), not ETH.

**Data Solutions**
- Call `get_dataset_schema()` before writing SQL. `transfers_clustered` for hop-level tracing; `sending_exposure_aggregation_alltime` for cashout exposure. Backend occasionally 502s - retry. Keep predicates selective.

**UI / platform**
- **No em-dashes** anywhere in copy.
- Live calls fire only in a real browser tab for a logged-in Chainalysis user; the preview sandbox blocks the API, so every demo ships validated fallbacks + a sandbox note.
- **Theming:** demos load `/assets/pages-theme.css`, whose tokens flip with the viewer's OS `prefers-color-scheme`. Any page with a hardcoded background must pin its tokens with a force-dark or force-light `<style>` block right after the stylesheet link. Adaptive pages (`bg-background` class) are fine as-is.
- **Reactor buttons:** open the new tab **synchronously on click** (popup blockers kill `window.open` called after an `await`); navigate it once the workflow returns.
- **Workflows:** run `WorkflowsClient().set_org_public(slug, True)` before release, or live calls fail for everyone but the owner.
- Address Screening is never replaced; products are additive.
- After edits, validate `<div>` open/close balance + run an em-dash check.

---

## Changelog

- **Jun 25, 2026** - Guided tours added to both API explainer pages (Screening, KYT) using a new self-contained, additive tour engine (`tracking/tour.js`). Walks request, run, and response. No change to existing flows.
- **Jun 25, 2026** - New cove: **Tokenized Securities / RWA (EquiChain)**. Eligibility gate (Address Screening before a wallet can hold a security token), secondary-transfer restriction (KYT), and a real Data Solutions landscape across 7 RWA tokens (BUIDL, USDY, OUSG, USYC, USTB, PAXG, XAUT) with counterparty mapping (new `cove-rwa-landscape` workflow, org-public). Built on the stablecoin scaffold.
- **Jun 25, 2026** - Launch hardening: all backing workflows set org-public; light/dark theme pinned per page; popup-safe Reactor open across all demos; analytics shows a graceful admin-only message; public Confluence page published (SAT space); `PUBLISH.md` distribution runbook added.
- **Earlier** - Insurance Claims (ChainGuard) built; Trading Firm Token Intel + `cove-token-intel`; domain-first Branding Studio (35-company auto-detect, logo/color/domain); hub guided tour; all 14 demos brought live.

---

## Architecture reference

### File structure
```
compliance-cove.html       # Hub - demo grid, Branding Studio, guided tour
demochain.html             # DeFi Trading (ArcSwap) - forced dark, canvas particle bg
banking-demo.html          # Banking - 5-stage scroll journey (forced light)
merchant-demo.html         # Merchant Services (Basecamp)
exchange-demo.html         # Exchange Onboarding (VaultX)
nft-demo.html              # Digital Marketplace (NovaMint)
atm-demo.html              # Crypto ATM (CoinVault)
gaming-demo.html           # Gaming (NexusArena)
remittance-demo.html       # Remittance (SwiftBridge) - forced light
hexagate-demo.html         # Protocol & Wallet Security (ShieldFi) - live Hexagate
trading-firm-demo.html     # Trading Firm (QuantDesk) - Token Intel
stablecoin-demo.html       # Stablecoin Issuer (Meridian) - Data Solutions headline
prediction-demo.html       # Prediction Markets (ForecastX)
p2p-marketplace-demo.html  # P2P Marketplace (Peerly)
insurance-demo.html        # Insurance Claims (ChainGuard) - Reactor investigations
rwa-demo.html              # Tokenized Securities / RWA (EquiChain) - real RWA landscape
screener.html              # Live Address Screener (SA tool)
screening-explainer.html   # Address Screening API walkthrough
kyt-explainer.html         # KYT API walkthrough
analytics.html             # Usage dashboard (admin-only)
addresses.js               # Shared address library + picker UI
kyt-transactions.js        # Curated, validated KYT scenarios
workflow/workflow.py        # Address Screening (demochain-address-screen)
workflow/kyt_screen.py      # KYT screening (cove-kyt-screen)
workflow/token_intel.py     # Data Solutions token risk (cove-token-intel)
workflow/hexagate.py        # Hexagate monitoring + Gate DSL (cove-hexagate)
workflow/reactor-graph.py   # Single-node Reactor graph (arcswap-reactor-graph)
workflow/insurance_graph.py # Multi-node Reactor graphs (cove-insurance-graph)
workflow/rwa_landscape.py   # Tokenized RWA landscape (cove-rwa-landscape)
workflow/analytics.py       # Usage tracking (compliance-cove-analytics)
PUBLISH.md                 # Distribution & update runbook
COMPONENTS.md              # Per-demo component matrix
ROADMAP.md                 # This file
```

### Design patterns
- **Styling:** `/assets/pages-theme.css` (Dialog) + Google Font `Inter`. Pin theme tokens per page (see Key learnings).
- **Animations:** `/assets/gsap.min.js`. **Charts:** `/assets/chart.min.js`.
- **Navigation:** multi-screen (`showScreen()`) or multi-page (`showPage()`) within one HTML file.
- **Hub linking:** `buildPageUrl(filePath)` resolves demo URLs within Chain's session-scoped page system.
- **Branding:** `?brand=&color=&domain=&logo=` params; `data-brand-logo` on nav logos; `querySelectorAll` for multi-screen; `BRAND_LOOKUP` auto-detects 35 companies from domain.
- **Deploy a workflow:** build a zip with the one `.py` (copy to a temp dir, `build.add_files(tmpdir)`), then `WorkflowsClient().create_or_deploy(...)` / `.deploy(slug, zip, handler)`. Test locally first: `python -m run_workflow workflow.<module>.handler '<json>'`. Then `set_org_public(slug, True)`.

### Adding a new demo (checklist)
1. Create `{name}-demo.html` following existing patterns; include `/assets/pages-theme.css`, Inter, GSAP.
2. Pin theme tokens (force-dark or force-light) right after the stylesheet link.
3. Add `?brand=` support + a default brand; `renderAddressPicker()` for inputs; `reactorLinkHtml()` (popup-safe) for address displays.
4. Register in `compliance-cove.html` `demos[]`: `status:'active'`, `url`, `defaultBrand`.
5. If a new workflow is involved, deploy it and `set_org_public(slug, True)`.
6. Update `COMPONENTS.md` and this file; push to `Bilal-Blockchain/compliance-cove`.
