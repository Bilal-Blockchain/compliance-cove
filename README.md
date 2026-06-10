# 🌊 Compliance Cove

**Interactive Chainalysis compliance demo hub** — built for Solutions Architecture.

Each "cove" is a fully functional prototype demonstrating how Chainalysis products integrate into real-world platforms.

## Live Demos

| Demo | File | Status | Products |
|---|---|---|---|
| **DeFi Trading** | `demochain.html` | ✅ Live | Address Screening, KYT |
| **Banking** | `banking-demo.html` | 🔜 Coming Soon | KYT, Kryptos |
| **Merchant Services** | `merchant-demo.html` | 🔜 Coming Soon | KYT, Address Screening |
| **P2P Marketplace** | `p2p-demo.html` | 🔜 Coming Soon | Address Screening, KYT |
| **NFT Platform** | `nft-demo.html` | 🔜 Coming Soon | Address Screening |
| **Crypto ATM** | `atm-demo.html` | 🔜 Coming Soon | KYT, Address Screening |

## How to Use in Chain

1. Start a new chat session
2. Tell Chain:

> Clone the repo `Bilal-Blockchain/compliance-cove` into my workspace and display `compliance-cove.html`

3. To build a new demo, say:

> I have the Compliance Cove project in my workspace. Read `compliance-cove.html` to see the existing demos. Build the [Banking] cove and plug it into the hub.

## Adding a New Demo

1. Create your demo HTML file (e.g., `banking-demo.html`)
2. Open `compliance-cove.html`, find the `demos` array in the `<script>` section
3. Change your entry's `status` to `'active'` and set `url` to the filename
4. The card automatically gets the Live badge and becomes clickable

## Project Structure
```
compliance-cove.html    # Landing page / demo hub
demochain.html          # DeFi Trading demo (live)
workflow/workflow.py    # Address screening backend
```
