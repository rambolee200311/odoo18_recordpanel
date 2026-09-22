# ATR-CC-04 Chatter-aware Preview Layout

## Scope

CC-04 Chatter-aware Preview Layout implementation only. CC-03 Preview
semantics and CC-02 navigation remain unchanged.

## Automated/browser instrumentation evidence

| Check | Result |
|---|---|
| JavaScript syntax and `git diff --check` | PASS |
| Wide active Preview: Form and Preview are horizontal | PASS |
| Wide active Preview: Chatter is below the Form area | PASS |
| XXL/maximized active Preview: Form container does not collapse to 1px | PASS |
| Narrow active Preview: DOM order is Form → Preview → Chatter | PASS |
| Preview close restores the native root layout direction | PASS |
| Preview close leaves the Chatter host present | PASS |

The checks were performed against the running Odoo 18 browser page at
`action-266/9` using the module's debug assets.

## Implementation boundary

- Uses module CSS only; no Odoo official source was changed.
- Uses the existing native Chatter host and existing CC-03 Preview Pane.
- No Chatter clone, custom Chatter, business write, or Many2one mutation was
  introduced.

## Remaining human verification

Human verification has passed for the native layout restoration, wide
Form/Preview/Chatter relationship, narrow Form → Preview → Chatter ordering,
and non-overlap at wide and narrow viewports. Native Chatter actions,
no-Chatter Forms, and preservation of unsaved Form state remain separate
checklist items pending explicit evidence.
