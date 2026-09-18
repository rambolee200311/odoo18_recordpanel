# ATR-CC-03 Extend Preview Core

## Scope

CC-03 v1.0.0 Frozen: Extend Preview Core only. CC-04 hardening and broader
navigation semantics are out of scope.

## Automated evidence

| Check | Result |
|---|---|
| Python syntax for module models | PASS |
| JavaScript syntax for preview and enhanced field sources | PASS |
| JavaScript syntax for Many2one tests | PASS |
| `git diff --check` | PASS |
| Odoo module upgrade (`-u wd_advanced_m2o_record_panel --stop-after-init --no-http`) | PASS |

## Implemented contract evidence

- `extend` dispatches only a target model and positive record id through the
  page event bus.
- The page host owns one Preview Pane and invalidates page/request tokens on
  close and unmount.
- The Loader checks current-user record and field access without business
  `sudo()`.
- Authorized records produce `ready` or safe `fallback` DTOs.
- Inaccessible or invalid targets produce `access_denied` without target
  identity.
- The renderer is read-only and only offers Open Full Record for authorized
  states.
- Full-record navigation reuses the CC-02 Navigation Builder.

## Not claimed

The Odoo HTTP service was unavailable during this validation pass, so no
Browser/HVR result is claimed here. Manual HVR must be completed against a
running Odoo instance before CC-03 is considered complete.
