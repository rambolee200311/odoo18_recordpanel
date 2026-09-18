# HVR Checklist — CC-01 Foundation / Configuration / Enhanced Many2one

Manual validation is required before proceeding to any later Coding Contract.

| # | Check | Expected result | Actual | Status | Evidence |
|---:|---|---|---|---|---|
| 1 | Install/upgrade module from Apps or configured Odoo runtime | Module loads without UI/server error | Passed | PASS | User HVR report |
| 2 | Open configuration menu as configuration administrator | Menu is visible and list/form views load | Passed | PASS | User HVR report |
| 3 | Create one configuration for a target model | Record saves successfully | Passed | PASS | User HVR report |
| 4 | Try a second configuration for the same target model | User receives a diagnostic uniqueness error | Passed | PASS | User HVR report |
| 5 | Add valid fields from the target model | Valid fields can be selected and saved | Passed | PASS | User HVR report |
| 6 | Add a field from another model | UI/domain prevents it or server rejects it safely | Passed | PASS | User HVR report |
| 7 | Add the same field twice | User receives a diagnostic duplicate-field error | Passed | PASS | User HVR report |
| 8 | Change target model while lines exist | Change is rejected; lines are not silently cleared | Passed | PASS | User HVR report |
| 9 | Open configuration menu as ordinary internal user | Management menu is not visible | User `comaback` cannot find the configuration menu | PASS | User HVR report |
| 10 | Read configuration as ordinary internal user | Read ACL is available for service/loader access; management UI remains hidden | Opened `stock.picking.form`; configuration read path is available without exposing the management menu | PASS | User HVR report |
| 11 | Load a form containing ordinary `many2one` | Default widget behavior remains unchanged | Passed | PASS | User HVR report |
| 12 | Load a field with `widget="advanced_many2one"` | Native Many2one display/autocomplete/search/select/clear behavior remains usable | `stock.picking.form` `partner_id` renders as a Many2one combobox; opening it shows candidate contacts and `Search More...`, with the `Internal link` button available | PASS | Browser page `WH/IN/00002`, 2026-09-18 |
| 13 | Use `open_mode` missing or invalid | Related-record opening remains native | Passed; related-record opening remained native | PASS | User HVR report |
| 14 | Use `open_mode="tab"` or `"extend"` in CC-01 | No blank/no-op/JS error; native fallback remains usable | Passed; no blank page, no no-op, and native fallback remained usable | PASS | User HVR report |
| 15 | Inspect browser console during checks | No new module asset or runtime errors | Passed; no new module asset or runtime errors observed | PASS | User HVR report |

## Human validation record

- Validator: User
- Date: 2026-09-18
- User role(s):
- Database: odoo18ce
- Browser:
- Overall result: PASS — items 1–15 passed.
- Notes: Ordinary users do not receive the configuration management menu. Their read permission is intentionally available to the future Preview Loader/service path, not to the management UI. HVR item results were supplied by the user. Do not proceed to CC-02 until the remaining checklist items are completed.
