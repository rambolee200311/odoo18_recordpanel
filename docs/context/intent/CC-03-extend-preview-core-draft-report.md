# CC-03 Draft Report — Extend Preview Core

## Status

| Item | Result |
|---|---|
| Contract | CC-03 v0.1.1 Draft |
| Status | Not Authorized for Freeze or Implementation |
| Scope | Extend Handler + page-scoped Preview Core |
| Production code | Not modified |
| CC-04 | Not created |
| Commit/Push | Not performed |

## Drafted Responsibilities

- Extend dispatch only for explicit enhanced Many2one fields;
- one page-scoped sibling Preview Pane;
- FormView template extension with thin Controller lifecycle integration;
- required logical Server-side Preview Loader;
- current-user permission chain and safe DTO;
- authorized fallback with safe basic identity, message and Full Record only after target access is confirmed;
- access_denied DTO with only safe code/message and no identity;
- no Full Record action and no source-value identity recovery in access_denied;
- information-disclosure ordering independent of internal Loader call order;
- all-fields-denied classified as authorized fallback, not record denial;
- readonly renderer and formatting boundary;
- source identity and request/page token lifecycle;
- basic stale response discard in CC-03;
- desktop sibling and small-screen vertical stacked layout;
- reuse of the CC-02 Record Navigation Builder.

## Security Decisions

- configuration metadata may be read by ordinary internal users under CC-01 ACL;
- business records and fields are always read in the current-user environment;
- no business `sudo()`;
- denied records must not leak model, name, id or field values;
- denied fields may be omitted while authorized fields continue;
- DTOs contain no HTML, traceback, SQL or internal exception text.

## Boundary Decisions

- CC-03 is the complete Extend vertical slice;
- CC-03 must already implement basic request identity and stale protection;
- CC-04 performs combined race, permission-change, deletion and upgrade attacks;
- no cache, recursive Preview, editable controls, multiple Pane, overlay or HTTP Controller;
- no change to Frozen SRS/TDD/Implementation Plan/CC-01/CC-02.

## HVR Scope

Human verification is deliberately limited to six scenarios: persistent sibling Pane, readonly configured display, source switch/clear/close, denied target safety, Full Record navigation and narrow vertical layout. Field omission, deletion/network errors, source isolation, configuration changes and stale response behavior belong to Python/JS ATR.

## Open Questions

No Contract Review Questions are intentionally left open in the Draft. Remaining items are implementation details: Loader method/file, DTO key names, FormView selector, host wiring, formatter imports, CSS and test fixtures.

## Stop

CC-03 Drafting is complete. Wait for user review. Do not Freeze, implement, Commit, Push or enter CC-04.
