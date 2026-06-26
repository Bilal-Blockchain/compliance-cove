# Compliance Cove

**Interactive Chainalysis compliance demo hub, built for Solutions Architecture.**

Each "cove" is a self-contained, browser-based prototype showing how Chainalysis products (Address Screening, KYT, Reactor, Hexagate, Data Solutions) integrate into a real customer product. Use them during prospect calls to show exactly how our products fit into their user experience. Many demos make real Chainalysis API calls live.

> **Internal use only.** Do not share the demos outside Chainalysis.

## Live demos

| Demo | File | Example brand | Products |
|---|---|---|---|
| Exchange Onboarding | `exchange-demo.html` | VaultX | Address Screening, KYT, VASP Risking |
| DeFi Trading | `demochain.html` | ArcSwap | Address Screening, KYT, Reactor |
| Banking | `banking-demo.html` | (neutral) | VASP Risking, Entity Monitoring, KYT, Data Solutions, Alterya |
| Merchant Services | `merchant-demo.html` | Basecamp | KYT, Address Screening |
| Crypto ATM | `atm-demo.html` | CoinVault | KYT, Address Screening |
| Remittance | `remittance-demo.html` | SwiftBridge | KYT, Address Screening |
| Trading Firm / Market Maker | `trading-firm-demo.html` | QuantDesk | Hexagate, Data Solutions, KYT, Address Screening |
| Stablecoin Issuer | `stablecoin-demo.html` | Meridian | Data Solutions, KYT, Address Screening, Reactor |
| Protocol & Wallet Security | `hexagate-demo.html` | ShieldFi | Hexagate, Address Screening |
| Gaming / Creator Economy | `gaming-demo.html` | NexusArena | Address Screening, KYT |
| Prediction Markets | `prediction-demo.html` | ForecastX | Data Solutions |
| Digital Marketplace | `nft-demo.html` | NovaMint | Address Screening |
| P2P Marketplace | `p2p-marketplace-demo.html` | Peerly | Address Screening, KYT, Reactor |
| Insurance Claims Investigation | `insurance-demo.html` | ChainGuard | Reactor, Address Screening |
| Tokenized Securities / RWA | `rwa-demo.html` | EquiChain | Data Solutions, Address Screening, KYT, Entity Monitoring, Reactor |

**SA tools:** `screener.html` (Live Address Screener), `screening-explainer.html` and `kyt-explainer.html` (API walkthroughs), `analytics.html` (usage dashboard, admin-only).

## How to view it

The Cove is shared company-wide from a dedicated Chain "Holder Session" and linked from a Confluence page. See **`PUBLISH.md`** for the full distribution and update runbook.

To work on it yourself, start a new Chain chat and say:

> Pull the `Bilal-Blockchain/compliance-cove` repo into my workspace and display `compliance-cove.html`.

Live results (real screening, real Reactor graphs) require being a logged-in Chainalysis user; otherwise demos render with validated sample data.

## Branding a demo for a prospect

Every demo has a **Branding Studio**. Type a prospect's name or domain and it auto-detects their logo and brand color (35-company lookup, with manual overrides). The brand, color, and logo carry across every screen. You can also pass them in the URL:

```
?brand=Chase+Digital&color=%230052FF&domain=chase.com&logo=https://...
```

## Adding a new demo

1. Create `{name}-demo.html` following the existing patterns.
2. Pin theme tokens (force-dark or force-light) right after the `/assets/pages-theme.css` link.
3. Add `?brand=` support, `renderAddressPicker()` for inputs, and a popup-safe `reactorLinkHtml()` for address displays.
4. In `compliance-cove.html`, set the card's `status` to `'active'` and its `url`/`defaultBrand`.
5. If a new workflow is involved, deploy it and run `set_org_public(slug, True)`.
6. Push to GitHub.

See `ROADMAP.md` for architecture details and key learnings, and `COMPONENTS.md` for the per-demo component matrix.

## Technical notes

- Standalone HTML files using the Chain Dialog design system (`/assets/pages-theme.css`).
- `/assets/pages-theme.css` flips colors with the viewer's OS light/dark setting, so each page pins its scheme with a force-dark or force-light `<style>` override.
- The hub's `buildPageUrl()` resolves demo links within Chain's session-scoped page system.
- Demos invoke backend workflows via `/api/workflow/{slug}/invoke/sync`. All eight backing workflows are org-public.
- No em-dashes in any copy.
