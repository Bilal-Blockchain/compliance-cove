// ============================================================
// COMPLIANCE COVE — Analytics Tracker
// ============================================================
// Fire-and-forget event tracking. Sends events to the
// compliance-cove-analytics workflow which writes to Google Sheets.
// Works across all Dialog sessions — any SA, AE, or CSM.
//
// Usage: include this script, then call:
//   coveTrack('demo_view', { demo: 'arcswap' })
// ============================================================

(function() {
  var SLUG = 'compliance-cove-analytics';
  var _demoName = document.title.split('—')[0].trim() || 'unknown';

  // Detect demo name from page
  var metaDemo = document.querySelector('meta[name="cove-demo"]');
  if (metaDemo) _demoName = metaDemo.getAttribute('content');

  // Get branding params
  var params = new URLSearchParams(window.location.search);

  // Track page view on load
  window.addEventListener('load', function() {
    coveTrack('demo_view', {});
  });

  // Global tracking function
  window.coveTrack = function(event, data) {
    var payload = {
      action: 'track',
      event: event,
      demo: data.demo || _demoName,
      screen: data.screen || '',
      brand: data.brand || params.get('brand') || '',
      color: data.color || params.get('color') || '',
      domain: data.domain || params.get('domain') || '',
      address: data.address || '',
      filter: data.filter || '',
      viewport: innerWidth + 'x' + innerHeight,
      timestamp: new Date().toISOString(),
    };

    // Fire and forget — never block the UI
    fetch('/api/workflow/' + SLUG + '/invoke/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: payload }),
    }).catch(function() { /* silent fail — tracking should never break the demo */ });
  };
})();
