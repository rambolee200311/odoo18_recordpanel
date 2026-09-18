# HVR-CC-03 Extend Preview Core

Run against a running Odoo 18 Community instance with an `extend` field
configured. Record the result and evidence for each item.

| ID | Scenario | Expected result | Result |
|---|---|---|---|
| HVR-03-01 | Click an `extend` Many2one | One persistent sibling Preview Pane appears beside the Form; no modal/drawer/overlay | PASS |
| HVR-03-02 | Inspect a configured target | Configured values display read-only, with no editable controls | PASS |
| HVR-03-03 | Switch source, clear value, and close Pane | Pane updates for the new target; clear/close removes preview safely | PASS |
| HVR-03-04 | Use a target the current user cannot read | Safe message only; no target identity or business values; no Open Full Record | PASS |
| HVR-03-05 | Click Open Full Record | Authorized ready/fallback state opens the correct complete record in a new browser tab | PASS |
| HVR-03-06 | Use a narrow viewport | Pane becomes vertically stacked and the main Form remains usable | PASS |

These six checks are the designated human-verification scenarios. Field
omission, stale response, deleted records, network errors, and source
isolation remain automated-contract coverage or CC-04 hardening.
