# IHR — CC-02 Tab Navigation

## Handoff Status

| Item | Result |
|---|---|
| Contract | CC-02 v1.0.0 Frozen |
| Implementation | Complete within authorized scope |
| Automated validation | Syntax and asset validation complete; isolated Hoot result not obtained |
| Browser/HVR | Complete; HVR-02-11 marked N/A because intentional popup blocking was skipped |
| Next contract | CC-03 not started |
| Commit/Push | Not performed |

## Implemented Components

### Tab Handler

`AdvancedMany2OneField` now overrides only `openAction()`:

- `open_mode="tab"` uses the Tab Handler;
- missing/invalid mode uses inherited native behavior;
- `extend` uses inherited native behavior;
- Dialog external opening remains inherited native behavior;
- no RPC is made before opening the new tab;
- popup failure produces a warning without opening the current page as a fallback.

### Navigation Builder

`buildRecordNavigation(targetModel, targetResId)`:

- validates a non-empty target model;
- validates a positive integer target resId;
- uses Odoo 18 `router.stateToUrl()`;
- emits a Router-restorable standard record URL;
- does not read the target business record;
- does not carry source `active_id`, source action stack, or arbitrary context.

## Asset/Test Integration

- Production source is included in `web.assets_backend`.
- CC-02 unit-test source is included once in `web.assets_unit_tests`.
- The obsolete duplicate `web.assets_tests` registration was removed to prevent duplicate suite registration in Odoo 18 Hoot.

## Verification Evidence

- JavaScript syntax check: PASS.
- Python syntax check: PASS.
- Odoo module upgrade through ORM: PASS.
- Backend asset inspection: PASS.
- Unit-test asset inspection: PASS; CC-02 test file appears once.
- Source Form remained unchanged after automated related-record click.
- Odoo's broad Web Hoot run contains unrelated pre-existing viewport/file-input failures; no isolated CC-02 Hoot PASS is claimed.
- Browser automation did not expose a new `_blank` page reliably; manual HVR is required for new-tab behavior.

## Explicit Non-Changes

- No Extend implementation.
- No Preview, Loader, Renderer or Preview State.
- No server-side production model or controller.
- No business-record `sudo()`.
- No official Odoo source modification.
- No `stock` dependency.
- No CC-03/CC-04 work.
- No Commit or Push.

## Handover Boundary

The manual HVR rows are complete; HVR-02-11 is explicitly N/A because intentional popup blocking was not configured. Stop and wait for user review. Do not begin CC-03.
