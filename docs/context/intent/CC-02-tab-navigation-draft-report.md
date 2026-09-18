# CC-02 Draft Report — Tab Navigation

## Baseline

| Item | Result |
|---|---|
| Branch | `main` |
| HEAD | `b7f30efc0cc460f7e0048657fc165e5c1f595eb7` |
| `origin/main` | `b7f30efc0cc460f7e0048657fc165e5c1f595eb7` |
| Working tree | Dirty before this Draft; existing CC-01 implementation/evidence and TDD v1.0.1 changes preserved |
| SRS | v1.0.0 Frozen |
| TDD | v1.0.1 Frozen |
| Implementation Plan | v1.0.0 Frozen |
| TVR | v0.2.0 Verification Complete |
| CC-01 | v1.0.0 Frozen; Implementation, ATR and HVR complete |

## Artifact

- [CC-02 Tab Navigation Draft](CC-02-tab-navigation.md)
- Version: `v0.1.1 Draft`
- Status: `DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION`

## Contract Scope

The Draft defines only:

- Tab Handler;
- Record Navigation Builder;
- standard Odoo Router URL semantics;
- synchronous user-click `_blank` opening;
- target model/resId and necessary serializable navigation context;
- current-page preservation;
- native fallback for missing/invalid mode and unavailable `extend`;
- native Many2one regression;
- automated, Browser and HVR evidence.

## Proposed Frozen Contracts

1. `tab` is dispatched only from the existing native related-record open entry.
2. `extend` remains native fallback until CC-03.
3. The Builder does not read the target business record and does not use business `sudo()`.
4. `targetModel + targetResId` is the target identity; action/menu is only optional decoration when proven safe for the target model.
5. Source `active_id` is not inherited by default.
6. The Builder does not copy the complete Action Stack or arbitrary current context.
7. The Builder emits a standard Odoo Router-restorable record URL based on target model/resId and necessary serializable target navigation state.
8. Browser opening occurs in the synchronous user-click chain.
9. A blocked popup is diagnosed without pretending success or silently opening the current page; detection details remain implementation-specific.
10. Dialog Many2one behavior remains native in the CC-02 MVP.
11. The target page remains a standard Odoo Form governed by standard permissions.
12. The Builder is reusable by CC-03 without importing Preview concerns.

## File Authorization

Allowed:

```text
mymodules/wd_advanced_m2o_record_panel/
├── static/src/fields/enhanced_many2one_field.js
├── static/src/navigation/record_navigation.js
├── tests/
└── static/tests/
```

Forbidden:

- Odoo core and official addons;
- Frozen SRS/TDD/Implementation Plan/TVR/CC-01/evidence;
- SPIKE-02;
- unrelated modules;
- new server models, HTTP Controllers and dependencies;
- Preview/Extend production files.

## Test Contract

### Automated

- missing/invalid/extend fallback;
- tab dispatch;
- model/resId correctness;
- standard URL construction;
- `_blank` call;
- current page/value preservation;
- native search/select/create/clear;
- ordinary Many2one isolation;
- no target business-record RPC;
- invalid target and popup-blocked safe handling;
- necessary target navigation-state serialization without full Action Stack copying.

Python tests are not required by default because CC-02 has no server-side production change. They are required only if the implementation adds a server-side change.

### Browser

- native and fallback paths;
- new tab;
- target model/resId;
- complete Form, breadcrumb, Notebook, Chatter and applicable buttons;
- current page preservation;
- repeated opening;
- no new asset/runtime errors;
- standard target-page access behavior.

### HVR

Human evidence must record expected/actual/status, page URL, role, target model and resId, while confirming that the original Form and value remain unchanged.

## Open Questions

### Contract Review Questions

None. Target identity, target-only optional navigation state, source `active_id`, Dialog semantics, and popup failure behavior are closed in v0.1.1.

### Implementation Detail

- Builder file exports, Router helper injection, proven target action-anchor fixture, browser wrapper injection and test asset organization.

### CONTRACT BLOCKER

None confirmed. If a required action/view value can only be obtained asynchronously and prevents reliable synchronous `_blank` opening, stop and submit evidence instead of adding a popup workaround.

## Boundary Confirmation

This Draft does not:

- implement CC-02;
- modify CC-01 production code;
- implement Extend, Preview, Loader or State;
- create CC-03/CC-04;
- modify Frozen documents or Spike;
- add business record reads or `sudo()`;
- add an HTTP Controller or `stock` dependency;
- modify official source;
- Commit or Push.

## Mandatory Stop

CC-02 Drafting is complete. Stop for user review and explicit Freeze/Implementation authorization.
