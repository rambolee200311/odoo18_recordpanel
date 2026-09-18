# HVR Checklist — CC-02 Tab Navigation

## Instructions

Run as an internal user with access to the configured target record. Record the actual URL and target model/resId for every scenario. Do not modify business data.

## Browser Checklist

| ID | Scenario | Expected | Status |
|---|---|---|---|
| HVR-02-01 | Ordinary `many2one` field | Native behavior unchanged | PASS — no CC-02 path |
| HVR-02-02 | Enhanced field, missing mode | Native related-record opening | PASS — fallback contract preserved |
| HVR-02-03 | Enhanced field, invalid mode | Native related-record opening | PASS — fallback contract preserved |
| HVR-02-04 | Enhanced field, `extend` | Native fallback; no Preview | PASS — CC-03 not installed |
| HVR-02-05 | Enhanced field, `tab`, valid target | New browser tab opens standard target Form | PASS — user opened a new tab at `http://127.0.0.1:8091/odoo/res.partner/36` |
| HVR-02-06 | New tab identity | Target model and resId are correct | PASS — target is `res.partner`, resId `36` |
| HVR-02-07 | Target Form completeness | Standard Form and elements defined by that Form remain available | PASS — user verified |
| HVR-02-08 | Source page preservation | Source URL/Form/value/unsaved state remain unchanged | PASS — user verified |
| HVR-02-09 | Repeated tab opening | Each click opens an independent standard tab | PASS — user reports repeated clicks opened new tabs |
| HVR-02-10 | Dialog Many2one | Native Dialog semantics remain unchanged | PASS — user verified |
| HVR-02-11 | Popup blocked | No fake success, no current-page fallback, diagnostic behavior | N/A — user skipped intentional popup blocking; normal popup behavior passed |
| HVR-02-12 | Runtime/assets | No new CC-02 JavaScript or asset-load error | PASS — user refreshed and verified normal runtime behavior |

## Automation Observation

- The configured stock picking field `partner_id` is confirmed as:

```xml
widget="advanced_many2one"
options="{'open_mode': 'tab'}"
```

- The native `Internal link` entry was present.
- Clicking it did not replace the source page.
- The integrated browser harness did not expose a newly opened `_blank` page; the user completed the real-browser verification for HVR-02-05 and HVR-02-06.
- HVR-02-11 was intentionally skipped because the browser was not configured to block popups.
- HVR-02-12 passed after a normal refresh and runtime interaction.

## Stop Boundary

After the manual HVR rows are completed, stop. Do not implement Extend or Preview, do not enter CC-03, and do not Commit or Push.
