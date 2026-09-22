# HVR-CC-05 Hardening & Integration

## Status

CC-05 v1.0.0 Frozen. All designated HVR scenarios PASS by manual
verification.

| ID | Scenario | Expected result | Result |
|---|---|---|---|
| HVR-05-01 | Restricted user opens a denied target | Only safe access-denied behavior is visible; no identity or technical details leak | PASS — manual verification |
| HVR-05-02 | Configuration changes while source Form remains open | Preview does not retain stale configuration or stale content | PASS — manual verification |
| HVR-05-03 | Access is revoked after a Preview was visible | Previously visible target information is not retained after refresh/re-entry | PASS — manual verification |
| HVR-05-04 | Native Many2one regression | Select, search, create, clear, display, and open remain usable | PASS — manual verification |
| HVR-05-05 | Standard Tab navigation regression | Tab opens the standard related record without changing source state | PASS — manual verification |
| HVR-05-06 | Wide Chatter-aware layout regression | Form, Preview, and Chatter remain usable without overlap | PASS — manual verification |
| HVR-05-07 | Narrow Chatter-aware layout regression | Form → Preview → Chatter remains usable and ordered correctly | PASS — manual verification |

These checks are limited to human-observable behavior. Detailed lifecycle,
permission, DTO, and stale-response assertions belong to Python/JavaScript/
Browser automation.
