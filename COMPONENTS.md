# 🧩 Compliance Cove — Component Tracking Matrix

> **Purpose:** Quick reference for which components are included in each demo. Check this before making sweeping changes.
>
> **Last updated:** June 22, 2026

## Component Matrix

| Demo | File | Disclaimer | Pre-screened Addresses | Branding Studio | Reactor Link | Analytics | MetaMask Icon |
|---|---|---|---|---|---|---|---|
| **ArcSwap** (DeFi) | `demochain.html` | ✅ Screening + Deposit KYT + Withdrawal KYT | ✅ walletAddr + withdrawAddr | ✅ ArcSwap | ✅ Workflow | ✅ | ✅ Full fox |
| **Banking** | `banking-demo.html` | ⬜ N/A (narrative demo) | ⬜ N/A | ⬜ No brand | ✅ Hardcoded | ✅ | ⬜ N/A |
| **Merchant** | `merchant-demo.html` | ✅ Payment results | ✅ paymentAddr | ✅ Basecamp | ✅ | ✅ | ⬜ N/A |
| **Exchange** | `exchange-demo.html` | ✅ Wallet screening + First Deposit KYT | ✅ walletAddr (attaches on Step 3) | ✅ VaultX | ✅ | ✅ | ✅ Full (6 providers) |
| **NFT** | `nft-demo.html` | ✅ Screening results | ✅ addressInput | ✅ NovaMint | ✅ | ✅ | ✅ Fixed (full fox) |
| **ATM** | `atm-demo.html` | ✅ Withdrawal KYT | ⬜ Not added | ✅ CoinVault | ⬜ None | ✅ | ⬜ N/A |
| **Gaming** | `gaming-demo.html` | ✅ Screening + Withdrawal KYT | ✅ walletAddress | ✅ NexusArena | ✅ | ✅ | ✅ Fixed (full fox) |
| **Remittance** | `remittance-demo.html` | ✅ Compliance checks | ✅ recipientWallet | ✅ SwiftBridge | ✅ | ✅ | ⬜ N/A |
| **Hexagate** | `hexagate-demo.html` | ✅ CSS ready | ✅ analyzeAddr | ✅ ShieldFi | ⬜ N/A | ✅ | ⬜ N/A |
| **Prediction** | `prediction-demo.html` | ⬜ N/A | ⬜ N/A | ✅ ForecastX | ⬜ N/A | ✅ | ⬜ N/A |
| **Screener** | `screener.html` | ✅ Dashboard results | ✅ addrInput | ⬜ Tool | ✅ Workflow | ✅ | ⬜ N/A |
| **KYT Explainer** | `kyt-explainer.html` | ⬜ N/A (educational) | ⬜ N/A | ⬜ N/A | ⬜ N/A | ✅ | ⬜ N/A |
| **Screening Explainer** | `screening-explainer.html` | ⬜ N/A (educational) | ⬜ N/A | ⬜ N/A | ⬜ N/A | ✅ | ⬜ N/A |

## Disclaimer Placement Details

| Demo | Where the disclaimer appears |
|---|---|
| ArcSwap | Above risk gauge in screening results · Above "KYT Workflow" label in deposit form · Above "KYT Withdrawal Workflow" label in withdrawal form · Inside dynamic deposit/withdrawal result blocks |
| Exchange | Above risk gauge in wallet screening results · Above KYT workflow steps in First Deposit |
| Gaming | Above risk gauge in screening results · Above withdrawal KYT workflow steps |
| Merchant | Inside dynamic payment screening result blocks |
| NFT | Above risk gauge in screening results |
| ATM | Above withdrawal KYT workflow steps |
| Remittance | Above compliance check KYT workflow steps |
| Screener | Top of every screening dashboard result |

## Shared Components Reference

| Component | File/Pattern | How to add |
|---|---|---|
| **Disclaimer** | `.cove-disclaimer` CSS class + HTML snippet | Add CSS to `<style>`, add HTML before KYT workflow steps or screening results |
| **Pre-screened Addresses** | `DEMO_ADDRESSES[]` + `renderAddressPicker(inputId)` | Add inline `<script>` block, call `setTimeout(()=>renderAddressPicker('inputId'),100)` |
| **Brand Color Swap** | `defaults[]` array — 13 hex codes | Include in brand-swap `<script>` at end of file |
| **Analytics Tracker** | `coveTrack()` inline script | Add `<script>` block before `</body>` |
| **MetaMask Icon** | Full 30-path SVG | Replace any 3-path abbreviated version with the full fox |
| **Chainalysis Logo** | Full SVG path including `M16.6823 25.339...` | Replace abbreviated paths that only have the top portion |

## Sweeping Change Checklist

When making a change that affects all demos:
1. Check this matrix to see which demos have the component
2. List the files that need changes
3. Update each file
4. Update this matrix after changes
5. Test at least ArcSwap + one light-theme demo (Exchange or NFT)
