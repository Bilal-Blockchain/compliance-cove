# Compliance Cove - Internal Data Disclaimer

Add this wherever Chainalysis screening/monitoring results are shown, to make clear the data is for the compliance team, not the end customer.

## HTML

```html
<div class="cove-disclaimer">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
  <span><strong>Internal Compliance View</strong>, this data is only visible to your compliance team. Your customers never see screening results, risk scores, or exposure data. This is the insight your team uses to make informed decisions.</span>
</div>
```

> No em-dashes in copy. Use a comma, as above.

## CSS (add once per page)

```css
.cove-disclaimer {
  display: flex; align-items: flex-start; gap: 8px;
  padding: 10px 14px; margin: 8px 0; border-radius: 8px;
  background: rgba(26,107,106,0.06); border: 1px solid rgba(26,107,106,0.15);
  font-size: 11px; line-height: 1.5; color: #1a6b6a;
}
.cove-disclaimer svg { flex-shrink: 0; margin-top: 1px; color: #1a6b6a; }
```

For dark-themed demos (ArcSwap, Hexagate, Trading Firm, Insurance), brighten it:

```css
.cove-disclaimer {
  background: rgba(26,107,106,0.08); border: 1px solid rgba(26,107,106,0.2);
  color: #2d9f8f;
}
.cove-disclaimer svg { color: #2d9f8f; }
```
