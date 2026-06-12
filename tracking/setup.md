# Compliance Cove — Slack Analytics Setup

Every demo page view posts a message to a Slack channel. Takes 3 minutes to set up.

## Setup

### 1. Create a Slack App (one-time)

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Name it `Compliance Cove Analytics`, pick the **Chainalysis** workspace
3. In the left sidebar, click **Incoming Webhooks** → toggle **Activate** to On
4. Click **Add New Webhook to Workspace**
5. Select the channel you want notifications in (e.g. `#compliance-cove-analytics`)
6. Click **Allow**
7. Copy the **Webhook URL** — looks like `https://hooks.slack.com/services/T.../B.../xxx`

### 2. Set the URL in the code

Open `compliance-cove.html`, find this line near the bottom:

```js
var SLACK_WEBHOOK = '';
```

Paste your webhook URL between the quotes. That's it — every demo view will now post to Slack.

## What gets posted

Each demo page view sends a formatted Slack message:

```
📊 Compliance Cove — Demo View
Demo: Banking
Time: Jun 12, 2026 3:30 PM
Session: abc123
Screen: 1440×900
```

## Privacy

- No PII is collected — just demo name, timestamp, session ID, and viewport size
- Session ID is the Chain page viewer path segment (anonymous)
- Messages go to your private Slack channel only
