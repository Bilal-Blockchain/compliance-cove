// ============================================================
// COMPLIANCE COVE — Pre-seeded Address Library
// ============================================================
// Curated addresses with known screening results for demos.
// Each address tells a story that resonates during customer calls.
//
// Usage in any demo:
//   <script src="addresses.js"></script>
//   Then call: renderAddressPicker('addressInput')
// ============================================================

const DEMO_ADDRESSES = [
  // ---- LOW RISK ----
  {
    id: 'defi-user',
    label: '🟢 Typical DeFi User',
    address: '0x5b5bC1Cc56508eE85353E2483B496746fB3fC2b0',
    risk: 'Low',
    network: 'ETH',
    story: 'A normal DeFi user — bridge activity, DEX swaps, exchange deposits. Clean profile.',
    category: 'low',
  },
  {
    id: 'binance-hot',
    label: '🟢 Binance Hot Wallet',
    address: '0x28C6c06298d514Db089934071355E5743bf21d60',
    risk: 'Low',
    network: 'ETH',
    story: 'Major exchange hot wallet — identified as Binance.com. Low risk, fully attributed.',
    category: 'low',
  },
  {
    id: 'ftx-hot',
    label: '🟢 FTX Hot Wallet',
    address: '0x2FAF487A4414Fe77e2327F0bf4AE2a264a776AD2',
    risk: 'Low',
    network: 'ETH',
    story: 'FTX.com exchange wallet — still shows Low risk. Great for discussing how risk scores reflect on-chain data, not headlines.',
    category: 'low',
  },

  // ---- MEDIUM RISK ----
  {
    id: 'unnamed-svc',
    label: '🟡 Unnamed Service',
    address: '0x0038AC785dfB6C82b2c9A7B3B6854e08a10cb9f1',
    risk: 'Medium',
    network: 'ETH',
    story: 'Categorized as an unnamed service — $4M+ exposure. Medium risk because the service isn\'t identified. Common in real-world screening.',
    category: 'medium',
  },
  {
    id: 'bayc-theft',
    label: '🟡 Stolen BAYC NFT',
    address: '0x8ae0E03AF14AC64918c48D858a4F9400Ca5A2a73',
    risk: 'Medium',
    network: 'ETH',
    story: 'Private wallet with 0.14% direct stolen funds exposure — connected to a Bored Ape Yacht Club NFT theft. Small exposure, but the rule triggers.',
    category: 'medium',
  },
  {
    id: 'justin-sun',
    label: '🟡 Justin Sun (Tron Founder)',
    address: '0x3DdfA8eC3052539b6C9549F12cEA2C295cfF5296',
    risk: 'Medium',
    network: 'ETH',
    story: 'Tron founder\'s wallet — $46B+ total volume, Medium risk from indirect sanctioned jurisdiction exposure. Shows how even public figures trigger compliance rules.',
    category: 'medium',
  },
  {
    id: 'wintermute',
    label: '🟡 Wintermute (Market Maker)',
    address: '0x0000000fe6a514a32abdcdfcc076c85243de899b',
    risk: 'Medium',
    network: 'ETH',
    story: 'Major crypto market maker — Medium risk due to >2% direct stolen funds exposure from their $160M hack in 2022.',
    category: 'medium',
  },

  // ---- SEVERE RISK ----
  {
    id: 'lazarus',
    label: '🔴 Lazarus Group (OFAC Sanctioned)',
    address: '0x098B716B8Aaf21512996dC57EB0615e2383E2f96',
    risk: 'Severe',
    network: 'ETH',
    story: 'OFAC SDN-listed North Korean state hacking group — Ronin Bridge exploiter ($625M). Blocked by Circle, Tether, and Binance. The textbook Severe case.',
    category: 'severe',
  },
  {
    id: 'tornado',
    label: '🔴 Tornado Cash (Sanctioned Mixer)',
    address: '0xd90e2f925DA726b50C4Ed8D0Fb90Ad053324F31b',
    risk: 'Severe',
    network: 'ETH',
    story: 'OFAC-sanctioned mixing service — $10B+ total volume. Sanctioned in Aug 2022. Shows how an entire protocol can be designated.',
    category: 'severe',
  },
  {
    id: 'vitalik',
    label: '🔴 Vitalik Buterin (Ethereum Creator)',
    address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',
    risk: 'Severe',
    network: 'ETH',
    story: 'Surprise! Vitalik\'s wallet shows Severe — because anyone can send tokens to a public address, including sanctioned entities. Perfect for discussing "dust attacks" and why context matters.',
    category: 'severe',
  },
];

// ============================================================
// ADDRESS PICKER UI
// ============================================================
// Renders a compact dropdown next to a target input field.
// Call: renderAddressPicker('inputElementId')
//
// It injects a small "Try an address" button below the input
// that opens a categorized dropdown. Selecting an address fills
// the input and closes the dropdown.
// ============================================================

function renderAddressPicker(inputId, options = {}) {
  const input = document.getElementById(inputId);
  if (!input) return;

  const filter = options.filter || null; // e.g. ['low','medium'] to show only those
  const addrs = filter
    ? DEMO_ADDRESSES.filter(a => filter.includes(a.category))
    : DEMO_ADDRESSES;

  // Create container
  const wrapper = document.createElement('div');
  wrapper.style.cssText = 'position:relative;margin-top:6px;';

  // Toggle button
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.style.cssText = 'display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border-radius:6px;border:1px solid var(--border);background:var(--background);color:var(--muted-foreground);font-size:11px;font-weight:600;cursor:pointer;transition:all .15s;';
  btn.innerHTML = '🎯 Try a pre-screened address <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>';
  btn.onmouseover = () => { btn.style.borderColor = 'var(--primary)'; btn.style.color = 'var(--foreground)'; };
  btn.onmouseout = () => { btn.style.borderColor = 'var(--border)'; btn.style.color = 'var(--muted-foreground)'; };

  // Dropdown panel
  const dropdown = document.createElement('div');
  dropdown.style.cssText = 'display:none;position:absolute;left:0;right:0;bottom:100%;margin-bottom:4px;max-height:320px;overflow-y:auto;border-radius:12px;border:1px solid var(--border);background:var(--card);box-shadow:0 12px 40px rgba(0,0,0,.15);z-index:99;padding:6px;';

  // Group by category
  const groups = [
    { key: 'low', label: 'Low Risk', color: '#22c55e' },
    { key: 'medium', label: 'Medium Risk', color: '#eab308' },
    { key: 'severe', label: 'Severe Risk', color: '#ef4444' },
  ];

  groups.forEach(g => {
    const items = addrs.filter(a => a.category === g.key);
    if (!items.length) return;

    const header = document.createElement('div');
    header.style.cssText = `padding:6px 8px 2px;font-size:9px;font-weight:700;color:${g.color};text-transform:uppercase;letter-spacing:1px;`;
    header.textContent = g.label;
    dropdown.appendChild(header);

    items.forEach(a => {
      const row = document.createElement('div');
      row.style.cssText = 'padding:8px 10px;border-radius:8px;cursor:pointer;transition:background .1s;';
      row.onmouseover = () => { row.style.background = 'var(--muted)'; };
      row.onmouseout = () => { row.style.background = 'transparent'; };
      row.innerHTML = `<div style="font-size:12px;font-weight:600;color:var(--foreground);">${a.label}</div><div style="font-size:10px;color:var(--muted-foreground);margin-top:2px;line-height:1.4;">${a.story}</div><div style="font-size:9px;color:var(--muted-foreground);margin-top:3px;font-family:monospace;opacity:.7;">${a.address.slice(0,10)}…${a.address.slice(-8)}</div>`;
      row.onclick = () => {
        input.value = a.address;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        dropdown.style.display = 'none';
        // Flash the input to show it was filled
        input.style.borderColor = g.color;
        input.style.boxShadow = `0 0 0 2px ${g.color}30`;
        setTimeout(() => { input.style.borderColor = ''; input.style.boxShadow = ''; }, 1500);
      };
      dropdown.appendChild(row);
    });
  });

  // Toggle
  btn.onclick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
  };

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!wrapper.contains(e.target)) dropdown.style.display = 'none';
  });

  wrapper.appendChild(dropdown);
  wrapper.appendChild(btn);
  input.parentNode.appendChild(wrapper);
}
