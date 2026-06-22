# 📈 Compliance Cove — Analytics Platform Setup

## Architecture

```
Demo Pages  →  Analytics Workflow (org-public)  →  MongoDB Atlas
                      ↑                                 ↑
              analytics.html reads  ←─────────── aggregation queries
```

**How it works:**
1. Every demo page fires a lightweight event to the analytics workflow
2. The workflow writes to MongoDB (connection string stored as workflow env var — never in code)
3. The analytics dashboard page reads from the same workflow
4. All SAs get tracking automatically — zero setup on their end

## What You Need to Provide

### 1. MongoDB Atlas Data API (recommended over pymongo)

We'll use the [Atlas Data API](https://www.mongodb.com/docs/atlas/api/data-api/) — simple REST calls, no driver needed. This avoids package dependency issues in the workflow runtime.

**Enable it:**
1. Go to MongoDB Atlas → your cluster → **Data API** (left sidebar)
2. Click **Enable Data API**
3. Create an **API Key** — copy it
4. Note your **Data Source** name (usually your cluster name, e.g., `Cluster0`)

**What I need from you:**
| Value | Example | Where it goes |
|---|---|---|
| Data API Endpoint | `https://us-east-1.aws.data.mongodb-api.com/app/data-xxxxx/endpoint/data/v1` | Workflow env var: `MONGODB_DATA_API_URL` |
| API Key | `abc123...` | Workflow env var: `MONGODB_API_KEY` |
| Data Source | `Cluster0` | Workflow env var: `MONGODB_DATA_SOURCE` |
| Database name | `compliance-cove` | Hardcoded in workflow |
| Collection name | `events` | Hardcoded in workflow |

### 2. Alternative: Connection String (pymongo)

If you prefer a direct connection string instead of the Data API:

| Value | Example | Where it goes |
|---|---|---|
| MongoDB URI | `mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/compliance-cove` | Workflow env var: `MONGODB_URI` |

⚠️ **Note:** `pymongo` may not be pre-installed in the workflow runtime. The Data API approach is safer since it only uses `requests` (always available).

## What Gets Built

### 1. `workflow/analytics.py` — Event Tracker + Query API

Two actions via one workflow:

```python
# Track an event
POST /api/workflow/compliance-cove-analytics/invoke/sync
{ "input": { "action": "track", "event": "demo_view", "demo": "banking", "brand": "Chase", ... } }

# Query analytics
POST /api/workflow/compliance-cove-analytics/invoke/sync
{ "input": { "action": "query", "range": "30d" } }
```

### 2. Tracking Snippet (added to each demo page)

```javascript
// Fire-and-forget — no await, no error handling needed
fetch('/api/workflow/compliance-cove-analytics/invoke/sync', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ input: {
    action: 'track',
    event: 'demo_view',
    demo: 'banking',
    brand: new URLSearchParams(location.search).get('brand') || null,
    timestamp: new Date().toISOString(),
    viewport: innerWidth + 'x' + innerHeight,
  }})
}).catch(() => {});
```

### 3. `analytics.html` — Dashboard Page

Chart.js dashboard with:
- **Demo views over time** (line chart)
- **Most popular demos** (bar chart)
- **Branding customizations** (which prospects are being targeted)
- **Product filter usage** (which filters SAs click most)
- **Address screener usage** (how many live screens per day)

### 4. Event Schema

```json
{
  "event": "demo_view | screen_change | address_screened | brand_customized | filter_used",
  "demo": "banking | arcswap | exchange | gaming | ...",
  "brand": "Chase | null",
  "color": "#0052FF | null",
  "domain": "chase.com | null",
  "screen": "onboarding-step-3 | null",
  "address": "0x098B... | null",
  "filter": "KYT | Resources | null",
  "timestamp": "2026-06-16T12:00:00Z",
  "viewport": "1440x900",
  "sessionId": "auto-generated"
}
```

## Deployment Steps

```
1. I build the workflow + dashboard + tracking snippets
2. You deploy once:
   - Set env vars: MONGODB_DATA_API_URL, MONGODB_API_KEY, MONGODB_DATA_SOURCE
   - Run: client.set_org_public("compliance-cove-analytics", True)
3. All SAs get tracking automatically from that point forward
```

## Next Steps

Tell Chain:
> "I have MongoDB Atlas Data API enabled. Here are my values: [endpoint], [api key], [data source]. Build the analytics workflow and dashboard."
