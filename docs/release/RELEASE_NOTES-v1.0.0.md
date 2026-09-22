# Release Notes — v1.0.0

## Summary

The v1.0.0 source release completes the planned Many2one Related Record View
Enhancement through CC-05 Final Hardening & Integration.

## Highlights

### Native and Tab navigation

- Ordinary Many2one fields retain native behavior.
- Explicit `tab` mode opens the related record in a standard new browser tab.
- Source Form state is preserved during Tab navigation.

### Read-only Extend Preview

- Explicit `extend` mode opens one page-scoped Preview Pane.
- Preview is read-only and does not save, create, delete, or edit business
  records.
- Authorized fallback and access-denied responses use safe DTOs.
- Full Record navigation reuses the standard Odoo route builder.

### Chatter-aware layout

- Wide screens keep Business Form and Preview side by side with Chatter below
  the Business Form.
- Narrow screens order Business Form, Preview, then Chatter.
- Preview close restores the native Form/Chatter relationship.
- Native Chatter is not cloned, replaced, or reimplemented.

### Hardening

- Missing and deleted records fail safely.
- Unreadable fields are omitted.
- Relational values are rendered as display names rather than technical IDs.
- Loading Preview can be closed.
- Load failures use safe user-facing messaging.
- Page/request stale-response protections remain active.

## Compatibility and boundaries

- Odoo 18 Community Edition.
- Formal module dependency remains `web`.
- No SPIKE-02 runtime dependency.
- No `stock` dependency.
- No business `sudo()`, raw SQL, DB driver, HTTP Controller, or official
  source modification.

## Verification and known findings

The release includes the recorded CC-01 through CC-05 ATR, HVR, and IHR
records. The Project Final Review records four non-code closure findings:

1. historical CC-04/CC-05 mapping differs from the Frozen Implementation Plan;
2. CC-03 ATR and HVR/IHR statements require evidence reconciliation;
3. CC-04 ATR and HVR/IHR statements require evidence reconciliation;
4. a single consolidated final install/upgrade/asset/browser smoke report was
   not captured.

These findings are retained for traceability. This release note does not
claim that they are resolved and does not independently declare production
release.
