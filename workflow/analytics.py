from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


SHEET_ID = "1c0kmUP0zw_umLQJzElGH3avG26eUs7SCxhLfYx7CqQU"


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    from chainalysis_skill_google_drive import GoogleDriveClient
    from datetime import datetime

    action = event.get("action", "track")
    client = GoogleDriveClient()

    if action == "track":
        row = [
            event.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            event.get("event", "unknown"),
            event.get("demo", ""),
            event.get("screen", ""),
            event.get("brand", ""),
            event.get("color", ""),
            event.get("domain", ""),
            event.get("address", ""),
            event.get("filter", ""),
            event.get("viewport", ""),
        ]

        client.sheets_request(
            "POST",
            f"{SHEET_ID}/values/A:J:append",
            params={"valueInputOption": "RAW"},
            json={"values": [row]},
        )

        return {"status": "tracked", "event": event.get("event")}

    elif action == "query":
        data = client.sheets_request("GET", f"{SHEET_ID}/values/A:J")
        rows = data.get("values", [])

        if len(rows) <= 1:
            return {"total": 0, "demos": {}, "events": {}, "brands": {}, "launches": [], "recent": [], "brandedDemos": [], "filters": {}, "screenings": 0}

        headers = rows[0]
        events_list = rows[1:]

        # Filter out test/setup rows
        events_list = [r for r in events_list if len(r) > 1 and r[1] not in ("test",)]

        # Aggregation
        demo_counts = {}
        event_counts = {}
        brand_counts = {}
        filter_counts = {}
        branded_demos = []  # List of {demo, brand, domain, timestamp}
        launches = []  # demo_launched events
        screening_count = 0
        daily_counts = {}

        for row in events_list:
            while len(row) < len(headers):
                row.append("")

            ts = row[0]
            evt = row[1]
            demo = row[2]
            brand = row[4]
            domain = row[6]
            filt = row[8]

            if demo:
                demo_counts[demo] = demo_counts.get(demo, 0) + 1
            if evt:
                event_counts[evt] = event_counts.get(evt, 0) + 1

            # Track branded demos specifically
            if brand and brand != "(default)":
                brand_counts[brand] = brand_counts.get(brand, 0) + 1

            if evt == "brand_customized" and brand and brand != "(default)":
                branded_demos.append({
                    "demo": demo,
                    "brand": brand,
                    "domain": domain,
                    "timestamp": ts,
                })

            if evt == "demo_launched":
                launches.append({
                    "demo": demo,
                    "brand": brand or "(default)",
                    "domain": domain,
                    "timestamp": ts,
                })

            if evt == "address_screened":
                screening_count += 1

            if filt:
                filter_counts[filt] = filter_counts.get(filt, 0) + 1

            # Daily aggregation
            day = ts[:10] if len(ts) >= 10 else "unknown"
            daily_counts[day] = daily_counts.get(day, 0) + 1

        # Recent events (last 50, newest first)
        recent = []
        for row in reversed(events_list[-50:]):
            while len(row) < len(headers):
                row.append("")
            recent.append(dict(zip(headers, row)))

        return {
            "total": len(events_list),
            "demos": demo_counts,
            "events": event_counts,
            "brands": brand_counts,
            "filters": filter_counts,
            "screenings": screening_count,
            "launches": launches[-20:],  # Last 20 launches
            "brandedDemos": branded_demos[-20:],
            "dailyCounts": daily_counts,
            "recent": recent,
        }

    return {"error": f"Unknown action: {action}"}
