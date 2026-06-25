# Compliance Cove - Component Matrix

> **Purpose:** Quick reference for which components each demo includes. Check this before sweeping changes.
>
> **Last updated:** June 25, 2026

## Matrix

| Demo | File | Theme (pinned) | Disclaimer | Address picker | Branding Studio | Reactor (live graph) | Analytics |
|---|---|---|---|---|---|---|---|
| DeFi Trading (ArcSwap) | `demochain.html` | Dark | ✅ | ✅ | ✅ | ✅ | ✅ |
| Banking | `banking-demo.html` | Light | N/A (narrative) | N/A | (neutral) | ✅ | ✅ |
| Merchant (Basecamp) | `merchant-demo.html` | Adaptive | ✅ | ✅ | ✅ | ✅ | ✅ |
| Exchange (VaultX) | `exchange-demo.html` | Adaptive | ✅ | ✅ | ✅ | ✅ | ✅ |
| Digital Marketplace (NovaMint) | `nft-demo.html` | Adaptive | ✅ | ✅ | ✅ | ✅ | ✅ |
| Crypto ATM (CoinVault) | `atm-demo.html` | Adaptive | ✅ | ✅ | ✅ | ⬜ | ✅ |
| Gaming (NexusArena) | `gaming-demo.html` | Adaptive | ✅ | ✅ | ✅ | ✅ | ✅ |
| Remittance (SwiftBridge) | `remittance-demo.html` | Light | ✅ | ✅ | ✅ | ✅ | ✅ |
| Trading Firm (QuantDesk) | `trading-firm-demo.html` | Dark | ✅ | ✅ | ✅ | ✅ | ✅ |
| Stablecoin (Meridian) | `stablecoin-demo.html` | Light | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protocol & Wallet Security (ShieldFi) | `hexagate-demo.html` | Dark | ✅ | ✅ | ✅ | N/A | ✅ |
| Prediction (ForecastX) | `prediction-demo.html` | Light | N/A | N/A | ✅ | N/A | ✅ |
| P2P Marketplace (Peerly) | `p2p-marketplace-demo.html` | Light | ✅ | ✅ | ✅ | ✅ | ✅ |
| Insurance Claims (ChainGuard) | `insurance-demo.html` | Dark | ✅ | ✅ | ✅ | ✅ (multi-node) | ✅ |
| Tokenized Securities / RWA (EquiChain) | `rwa-demo.html` | Light | ✅ | ✅ | ✅ | ✅ | ✅ |
| Address Screener | `screener.html` | Light | ✅ | ✅ | tool | ✅ | ✅ |
| Screening API Walkthrough | `screening-explainer.html` | Light | N/A | N/A | N/A | N/A | ✅ |
| KYT API Walkthrough | `kyt-explainer.html` | Light | N/A | N/A | N/A | N/A | ✅ |
| Analytics dashboard | `analytics.html` | Light | N/A | N/A | N/A | N/A | self |

**Theme column:** "Adaptive" pages use the `bg-background` class and follow the viewer's OS light/dark setting. "Dark" / "Light" pages have a hardcoded background and pin their tokens with a `cove-force-dark` / `cove-force-light` `<style>` block right after the `/assets/pages-theme.css` link. When adding a page, match the pin to the hardcoded background.

## Shared components

| Component | Pattern | How to add |
|---|---|---|
| Disclaimer | `.cove-disclaimer` class + HTML snippet | See `tracking/disclaimer.md`. Place above screening results / KYT workflow steps. |
| Address picker | `DEMO_ADDRESSES[]` + `renderAddressPicker('inputId')` | Inline script; call `setTimeout(()=>renderAddressPicker('inputId'),100)`. |
| Branding | `?brand=&color=&domain=&logo=` params | `data-brand-logo` on nav logos; `querySelectorAll` for multi-screen; `BRAND_LOOKUP` (35 companies). |
| Reactor link | popup-safe `reactorLinkHtml()` / `openInReactor()` | Open the tab synchronously on click, then navigate it after the workflow returns. |
| Analytics | `coveTrack()` inline script | Add a `<script>` block before `</body>`. |
| Theme pin | `cove-force-dark` / `cove-force-light` `<style>` | Insert right after the pages-theme.css link; match the page background. |

## Sweeping-change checklist

1. Check this matrix for which demos have the component.
2. List the files that need changes.
3. Update each file.
4. Validate: `<div>` open/close balance + em-dash check.
5. Test at least one dark, one light, and one adaptive demo.
6. Update this matrix and push.
