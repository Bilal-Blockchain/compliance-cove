# 🌊 Compliance Cove

**Interactive Chainalysis compliance demo hub** — built for Solutions Architecture.

Each "cove" is a fully functional prototype demonstrating how Chainalysis products integrate into real-world platforms. Use them during customer calls to show exactly how our products fit into their user experience.

## Live Demos

| Demo | File | Status | Products |
|---|---|---|---|
| **DeFi Trading** | `demochain.html` | ✅ Live | Address Screening, KYT |
| **Banking** | `banking-demo.html` | ✅ Live | VASP Risking, Entity Monitoring, KYT, Data Solutions, Alterya |
| **Merchant Services** | `merchant-demo.html` | ✅ Live | KYT, Address Screening |
| **Exchange Onboarding** | `exchange-demo.html` | ✅ Live | Address Screening, KYT, VASP Risking |
| **NFT Platform** | `nft-demo.html` | ✅ Live | Address Screening |
| **Crypto ATM** | `atm-demo.html` | ✅ Live | KYT, Address Screening |
| **Gaming / Creator Economy** | `gaming-demo.html` | ✅ Live | Address Screening, KYT |
| **Remittance / Money Transfer** | `remittance-demo.html` | ✅ Live | KYT, Address Screening |
| Smart Contract Security | — | 🔜 Coming Soon | Hexagate |
| Insurance Claim Verification | — | 🔜 Coming Soon | Reactor, KYT, Address Screening |
| P2P Marketplace | — | 🔜 Coming Soon | Address Screening, KYT |
| Stablecoin Issuer | — | 🔜 Coming Soon | KYT, Entity Monitoring, Address Screening |
| Prediction Markets | — | 🔜 Coming Soon | Data Solutions |

## How to Use in Chain

1. Start a new Chain chat session
2. Tell Chain:

> Clone the repo `Bilal-Blockchain/compliance-cove` into my workspace and display `compliance-cove.html`

3. The hub page will display with all demo cards. Click any **Live** demo to open it in a new tab.

4. To modify an existing demo or build a new one:

> I have the Compliance Cove project in my workspace. Read the existing files and let's update the [Banking] cove.

5. When you're done making changes, tell Chain to push back to GitHub:

> Push the changes back to GitHub

## Demo Highlights

### 🏦 Banking — The Crypto Readiness Journey
A 5-stage scrolling journey showing how banks adopt crypto compliance:
1. **Training & Enablement** — Chainalysis Academy certifications (CDAF, CCCA) and compliance courses
2. **Know Your VASP** — VASP Risking scorecard with exposure categories and off-chain data
3. **Know Your Asset** — KYT Entity Monitoring asset profiles + Data Solutions Ecosystem Monitoring dashboards
4. **KYT + Reactor** — Interactive 6-step walkthrough: customer withdrawal → KYT screening → alert → Reactor trace → analyst review → resolution
5. **Fraud Prevention** — Alterya scam intercept alerts and protection dashboard

### 🎮 Gaming — NexusArena
Full gaming platform with wallet connect, compliance screening, a 10-second "Risk Blitz" mini-game, marketplace with purchasable skins (that change your player avatar), and crypto withdrawal with KYT monitoring.

### 💸 Remittance — SwiftBridge
Cross-border payment app with animated globe background showing transfer corridors, country selection, real-time compliance screening, and travel rule enforcement.

## Adding a New Demo

1. Create your demo HTML file (e.g., `insurance-demo.html`)
2. Open `compliance-cove.html`, find the `demos` array in the `<script>` section
3. Change your entry's `status` to `'active'` and set `url` to the filename
4. The card automatically gets the Live badge and becomes clickable
5. Push changes to GitHub

## Project Structure

```
compliance-cove.html      # Landing page / demo hub
banking-demo.html         # Banking — Crypto Readiness Journey
demochain.html            # DeFi Trading demo
merchant-demo.html        # Merchant Services demo
exchange-demo.html        # Exchange Onboarding demo
nft-demo.html             # NFT Platform demo
atm-demo.html             # Crypto ATM demo
gaming-demo.html          # Gaming / Creator Economy demo
remittance-demo.html      # Remittance / Money Transfer demo
workflow/workflow.py       # Address screening backend (workflow)
```

## Technical Notes

- All demos are standalone HTML files using the Chain Dialog design system (`/assets/pages-theme.css`)
- Demos that need dark-mode override use explicit CSS variable overrides at `:root` level
- The hub page's `buildPageUrl()` function resolves demo links relative to the current file's directory
- Interactive demos use multi-screen architecture with `showScreen()` toggling `.screen` divs
- The Banking demo's Stage 4 has a self-contained step-through with `showS4Step()` for the KYT+Reactor walkthrough
