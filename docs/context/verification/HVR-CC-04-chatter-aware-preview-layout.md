# HVR-CC-04 Chatter-aware Preview Layout

Run against a running Odoo 18 Community browser session.

| ID | Scenario | Expected result | Result |
|---|---|---|---|
| HVR-04-01 | Preview closed | Native Form/Chatter layout is unchanged | PASS — manual verification at wide and narrow viewport |
| HVR-04-02 | Wide viewport with Chatter and active Preview | Form and Preview are side by side; Chatter is below the Form area | PASS — manual verification, including maximized/XXL viewport |
| HVR-04-03 | Narrow viewport with Chatter and active Preview | Order is Form → Preview → Chatter | PASS — manual verification |
| HVR-04-04 | Form without Chatter and active Preview | Only Form and Preview appear; no Chatter placeholder | PASS — included in approved manual validation |
| HVR-04-05 | Use native Chatter actions after activation | Send Message, Log Note, Activities, attachments/followers remain usable where present | PASS — included in approved manual validation |
| HVR-04-06 | Close Preview after editing an unsaved field | Native layout returns; no reload, save, field mutation, or loss of unsaved state | PASS — included in approved manual validation |
| HVR-04-07 | Inspect supported wide/narrow widths | Form, Preview, and Chatter do not overlap | PASS — manual verification at wide and narrow viewport |

These checks are limited to human layout and native-Chatter verification.
Detailed state and mutation assertions remain automated coverage.
