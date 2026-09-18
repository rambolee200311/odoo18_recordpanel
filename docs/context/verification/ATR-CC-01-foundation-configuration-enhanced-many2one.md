# ATR — CC-01 Foundation / Configuration / Enhanced Many2one

| Item | Value |
|---|---|
| Contract | CC-01 v1.0.0 Frozen |
| Automated validation status | PASS |
| Database | `odoo18ce` |
| Odoo | 18.0 Community Edition |

## Automated evidence

| Check | Command | Result |
|---|---|---|
| Python syntax | `python3 -m py_compile ...` | PASS |
| JavaScript syntax | `node --check` for production and test files | PASS |
| Odoo module upgrade and Python tests | `python3 odoo-bin -c odoo.conf -d odoo18ce -u wd_advanced_m2o_record_panel --stop-after-init --test-enable --log-level=info` | PASS |
| Odoo test result | `0 failed, 0 error(s) of 6 tests` | PASS |
| Registry/module loading | `wd_advanced_m2o_record_panel` loaded and registry initialized | PASS |

## Covered automated behavior

- Configuration uniqueness remains enforced when inactive.
- Configuration fields must belong to the configured target model.
- Duplicate configured fields are rejected.
- Configuration line ordering is deterministic.
- Target model changes with existing lines are rejected.
- Internal user configuration read is allowed and write is denied.
- Enhanced field registration is isolated from the default `many2one` registry entry.
- `native`, `tab`, `extend`, missing, and invalid opening-mode resolution is covered by JS tests.

The duplicate-key and access-denied lines emitted in the Odoo log are expected evidence from tests asserting rejection and ACL enforcement; the final Odoo result is zero failures and zero errors.

## Not automated in CC-01

- Browser/HVR interaction and visual regression.
- Actual Tab Handler behavior.
- Actual Extend/Preview behavior.
- Production action URL construction.

Those items are intentionally outside CC-01 and are listed only for human validation or later contracts.
