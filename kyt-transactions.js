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
    story: 'Funds from a normal DeFi/self-custody wallet. No risky exposure — KYT clears it instantly.',
    expected: 'CLEARED',
    input: { mode: 'withdrawal', network: 'ETHEREUM', asset: 'ETH', assetAmount: 2.5,
             address: '0x5b5bC1Cc56508eE85353E2483B496746fB3fC2b0' },
  },
  {
    id: 'mixer',
    label: '🟡 Mixer-exposed deposit (Tornado Cash)',
    asset: 'ETH',
    amount: '7.6',
    story: 'Funds received directly from the OFAC-sanctioned Tornado Cash mixer — triggers a real KYT alert.',
    expected: 'MEDIUM',
    input: { mode: 'transfer', network: 'ETHEREUM', asset: 'ETH', direction: 'received',
             transferReference: '0x6582e5d0b18c05118bf34abe24d2be5729c64d6da466a3da811a2ca45e5fd9e8:0x77ebb90f659461ca82921a2314bd6d06ff036cfa' },
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

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { KYT_WORKFLOW_SLUG, KYT_DEPOSITS };
}
