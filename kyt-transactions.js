// ============================================================
// COMPLIANCE COVE — Pre-screened KYT Transaction Library
// ============================================================
// Curated, REAL transactions/addresses with KNOWN live-KYT
// outcomes, for transaction-monitoring demos. Each entry has
// been validated against the shared Chainalysis KYT org via the
// `cove-kyt-screen` workflow.
//
// Two shapes (see workflow/kyt_screen.py):
//   - mode:"transfer"   monitor a real on-chain deposit (txhash:address)
//   - mode:"withdrawal" pre-screen an outgoing address (address only)
//
// Usage in a demo:
//   const r = await fetch('/api/workflow/cove-kyt-screen/invoke/sync',
//       {method:'POST',headers:{'Content-Type':'application/json'},
//        body:JSON.stringify({input: scenario.input})});
// ============================================================

const KYT_WORKFLOW_SLUG = 'cove-kyt-screen';

const KYT_DEPOSITS = [
  {
    id: 'clean',
    label: '🟢 Clean deposit (self-custody wallet)',
    asset: 'ETH',
    amount: '2.5',
    story: 'Funds from a normal DeFi/self-custody wallet. No alert generated — source of funds are clean.',
    expected: 'CLEARED',
    input: { mode: 'withdrawal', network: 'ETHEREUM', asset: 'ETH', assetAmount: 2.5,
             address: '0x5b5bC1Cc56508eE85353E2483B496746fB3fC2b0' },
  },
  {
    id: 'atm',
    label: '🟡 Crypto ATM source (RockItCoin)',
    asset: 'BTC',
    amount: '0.13',
    source: 'RockItCoin.com',
    sourceCat: 'Crypto ATM',
    // KYT registers/monitors the transfer (real), and Chainalysis attributes the
    // source as a crypto ATM (real, via Data Solutions). This org's KYT rules don't
    // hard-alert on ATMs, so the demo frames it as policy-based Enhanced Due
    // Diligence on a high-risk cash-in category — distinct from a sanctioned hard alert.
    story: 'Deposit traced to a crypto ATM — a high-risk cash-in category (FATF/FinCEN). No sanctions alert, but routed to enhanced due diligence under policy.',
    expected: 'EDD',
    input: { mode: 'transfer', network: 'BITCOIN', asset: 'BTC', direction: 'received',
             transferReference: 'cc8011ecf88258fe0bc69784a667e82e66fc73d18e0dd68ee4930732b51b080b:bc1qfkneq4q4msqhxwhjhrv2pmwcmq3w4etyhazz8w' },
  },
  {
    id: 'sanctioned',
    label: '🔴 Sanctioned source (Swapster.fi)',
    asset: 'USDT',
    amount: '4,840',
    story: 'Stablecoin received from an OFAC/EU-sanctioned service — severe KYT alert, funds frozen pending review.',
    expected: 'SEVERE',
    input: { mode: 'transfer', network: 'ETHEREUM', asset: 'USDT', direction: 'received',
             transferReference: '0x0f9e200d58a92d1eca9d120340a4ed18ec927055230baad3cfbc58ea5943e680:0x0c82f1b5e5acb1a63cb7aecddf389b342fb15e35' },
  },
  {
    id: 'sanctioned2',
    label: '🔴 Sanctioned source (Heleket.com)',
    asset: 'USDT',
    amount: '9,989',
    story: 'Stablecoin received from an OFAC/EU-sanctioned service — severe KYT alert.',
    expected: 'SEVERE',
    input: { mode: 'transfer', network: 'ETHEREUM', asset: 'USDT', direction: 'received',
             transferReference: '0xf15bfc35757484912e9782f84414a9290d2d50744870e841dc76ce76e7566771:0xdc7955346c29c2a3452496897b5f9a63c6ee20a1' },
  },
];

// ---- WITHDRAWAL scenarios (outgoing sends) ----
// For demos with a "send / withdraw" flow. Includes the continuous-monitoring
// case: a destination that screened clean at send, but whose funds later reached
// a sanctioned entity (indirect exposure) — caught by ongoing KYT monitoring.
const KYT_WITHDRAWALS = [
  {
    id: 'wd-clean',
    label: '🟢 Clean destination',
    asset: 'BTC', amount: '0.05', expected: 'CLEARED',
    story: 'A normal external wallet — pre-screen clears it and the withdrawal proceeds.',
    input: { mode: 'withdrawal', network: 'BITCOIN', asset: 'BTC', assetAmount: 0.05,
             address: 'bc1qakvuk920fcal063mpvz6gym0nsse0auuz9ny0u' },
  },
  {
    id: 'wd-sanctioned',
    label: '🔴 Sanctioned destination (blocked)',
    asset: 'BTC', amount: '0.05', expected: 'SEVERE',
    story: 'Destination is OFAC-sanctioned (Chatex.com). The withdrawal is blocked before any funds leave.',
    input: { mode: 'withdrawal', network: 'BITCOIN', asset: 'BTC', assetAmount: 0.05,
             address: '3JaAYDPJkwdSYtBDML3QUtaSJjB6eebd2R' },
  },
  {
    id: 'wd-indirect',
    label: '🟡 Indirect exposure — continuous monitoring',
    asset: 'BTC', amount: '0.0423', expected: 'INDIRECT',
    source: 'Chatex.com', sourceCat: 'OFAC SDN (sanctioned entity)',
    // The destination screened clean at send. KYT keeps monitoring the registered
    // transfer and later raises a SEVERE indirect alert when the funds reach the
    // sanctioned entity — the point-in-time screen alone would have missed this.
    story: 'Destination screened clean at the time of send. KYT continuous monitoring later detected the funds reaching OFAC-sanctioned Chatex.com — a SEVERE indirect-exposure alert on the completed transfer.',
    input: { mode: 'transfer', network: 'BITCOIN', asset: 'BTC', direction: 'sent',
             transferReference: '6dd7ede9526c3bb8b670696b96a6edf6d39d445f02b8496da3335d69c6640c47:bc1q68k9yatpytxurh94gk6ulk764lc37vxa54y4ar' },
  },
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { KYT_WORKFLOW_SLUG, KYT_DEPOSITS, KYT_WITHDRAWALS };
}
