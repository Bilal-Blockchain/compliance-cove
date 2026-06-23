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
    id: 'exchange',
    label: '🟡 Exchange-sourced deposit (Bitget)',
    asset: 'USDT',
    amount: '15,982',
    story: 'Funds received directly from a third-party exchange. KYT logs the counterparty for Travel Rule / source-of-funds — LOW severity, cleared with a record. (Non-sanctioned, so it reads as a clean "needs a note" tier — unlike a mixer/sanctioned source.)',
    expected: 'LOW',
    input: { mode: 'transfer', network: 'ETHEREUM', asset: 'USDT', direction: 'received',
             transferReference: '0x92d7be10a97025f32928748a3e2415f3fa321dfc5b0f2027b0cdec5f606ca905:0xbc0235c2052844a887ab5c896018f788148e7782' },
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
