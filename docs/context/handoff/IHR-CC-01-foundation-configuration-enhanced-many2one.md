# IHR — CC-01 Foundation / Configuration / Enhanced Many2one

| Item | Value |
|---|---|
| Contract | CC-01 |
| Contract version | v1.0.0 Frozen |
| Implementation status | Complete for authorized CC-01 scope |
| Odoo | 18.0 Community Edition |
| Module | `wd_advanced_m2o_record_panel` |
| Handoff status | Ready for human validation; stop before CC-02 |

## Implemented

- Formal module skeleton with `web` as the only dependency.
- `wd.preview.configuration` and `wd.preview.configuration.line` ORM models.
- One configuration per target model, including inactive configurations.
- Target-model/field consistency and duplicate-field validation.
- Deterministic line ordering with `sequence, id`.
- Configuration target-model changes rejected while lines exist.
- Configuration ACLs: internal users read; configuration administrators CRUD.
- Administrator-only configuration menu.
- `advanced_many2one` registry entry reusing the official `Many2OneField`.
- `open_mode` resolution for `native`, `tab`, and `extend`; unsupported or missing values resolve to `native`.
- CC-01 native fallback only. No Tab Handler, Preview Host, Preview State, Loader, Renderer, or business-record read path was added.
- Python and JavaScript test assets within the authorized test directories.

## Boundary confirmation

- No Odoo core or official addon source was modified.
- No `stock` dependency was added.
- No business-record `sudo()` or custom business read path was added.
- No CC-02 or later implementation was started.
- No commit or push was performed.

## Required next step

Perform the HVR items in the companion checklist. After human validation, the next contract decision remains outside this handoff.
