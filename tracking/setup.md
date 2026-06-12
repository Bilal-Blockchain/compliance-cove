# Compliance Cove — Analytics Setup

## One-time setup (2 minutes)

The demos track page views by POSTing to a Google Apps Script web app, which appends rows to your Google Sheet.

### Your tracking sheet
📊 **[Compliance Cove — Demo Analytics](https://docs.google.com/spreadsheets/d/1PbxMHjbUJKKNZZdCLg8smlJvOsCLAl3xV8w55mlNc88)**

### Deploy the tracking endpoint

1. Open the Google Sheet above
2. Go to **Extensions → Apps Script**
3. Delete any existing code and paste the contents of `apps-script.js` (in this folder)
4. Click **Deploy → New deployment**
5. Choose **Web app** as the type
6. Set:
   - **Execute as:** Me
   - **Who has access:** Anyone
7. Click **Deploy**
8. Copy the **Web app URL** (looks like `https://script.google.com/macros/s/AKfyc.../exec`)
9. Open `compliance-cove.html` and find `TRACKING_URL` near the top of the `<script>` section
10. Paste your URL there

That's it! Every demo page view will now log to your sheet automatically.

### What gets tracked

| Field | Example |
|---|---|
| Timestamp | 2026-06-12T15:30:00Z |
| Demo | banking-demo |
| Page URL | https://chain.chainalysis.com/page/abc123?... |
| Session ID | abc123 (from URL path) |
| User Agent | Mozilla/5.0... |
| Referrer | (previous page) |
| Screen | landing → send → compliance |
