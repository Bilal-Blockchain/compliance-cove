# Compliance Cove — Analytics

## How it works

```
Demo pages  --track-->  compliance-cove-analytics workflow  -->  Google Sheet
analytics.html  --query-->  same workflow  -->  aggregated dashboard
```

- Every demo fires a lightweight `track` event to the `compliance-cove-analytics` workflow (`workflow/analytics.py`).
- The workflow appends the event as a row to a Google Sheet (`SHEET_ID` in `workflow/analytics.py`).
- `analytics.html` calls the same workflow with `action: "query"`, which reads the sheet and returns aggregates.

## Important: it runs as the caller's Google identity

The workflow uses `GoogleDriveClient()`, which authenticates with **the invoking user's** Google connection (there are no shared service credentials stored on the workflow). Consequences:

- **Reads/writes only work for users who have Google connected in Chain and access to the sheet.** In practice that is the project admins.
- `analytics.html` is therefore **admin-only**. Non-admins see a friendly "Analytics is admin-only" message instead of an error.
- Because tracking writes also use the caller's identity, captured events are mostly admin sessions, not every viewer.

To broaden analytics to all users you would need a shared service identity (e.g. a service account or a stored refresh token the workflow uses instead of the caller's). That is a future enhancement, not currently implemented.

## Event shape

`track` events send these fields (appended as columns A:J):

```
timestamp, event, demo, screen, brand, color, domain, address, filter, viewport
```

Common `event` values: `demo_launched`, `address_screened`, `brand_customized`, `filter_used`, `tour_started`, `tour_ended`.

## Tracking snippet (already in every page)

```javascript
// Fire-and-forget
fetch('/api/workflow/compliance-cove-analytics/invoke/sync', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ input: {
    action: 'track', event: 'demo_launched', demo: 'arcswap',
    brand: new URLSearchParams(location.search).get('brand') || '',
    timestamp: new Date().toISOString(),
    viewport: innerWidth + 'x' + innerHeight,
  }})
}).catch(() => {});
```

## Apps Script

`tracking/apps-script.js` is the Google Apps Script bound to the sheet (used for any sheet-side automation / formatting). The workflow itself appends via the Sheets API and does not require it.
