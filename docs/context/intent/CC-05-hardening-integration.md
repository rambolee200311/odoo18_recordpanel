# CC-05 Hardening & Integration

## Status

**v1.0.0 Frozen — Implementation Completed**

This contract is the final hardening round following the completed CC-04
Chatter-aware Preview Layout requirement.

The original Frozen Implementation Plan identified this hardening round as
CC-04. After the separately introduced and completed Chatter-aware Preview
Layout round was assigned CC-04, the hardening round is now tracked as CC-05.
This renumbering is a document-history and traceability adjustment only. It
does not change the technical scope previously defined for the hardening
round, and does not silently modify the Frozen SRS, TDD, Implementation Plan,
or any completed Contract.

## 1. Contract Metadata

| Item | Value |
|---|---|
| Contract ID | CC-05 |
| Contract name | Hardening & Integration |
| Odoo | 18.0 Community Edition |
| Formal module | `mymodules/wd_advanced_m2o_record_panel/` |
| Upstream baseline | CC-01, CC-02, CC-03 and CC-04 complete |
| Historical round ID | CC-04 — Hardening & Integration |
| Renumbering reason | CC-04 Chatter-aware Preview Layout was inserted before hardening |
| Current status | Frozen / implementation completed |
| Spike dependency | None |

## 2. Goal

Systematically attack the completed CC-01 through CC-04 behavior and close
the production lifecycle, permission/error-handling verification,
concurrency, layout, configuration-change, upgrade-risk, and regression loop.
This Contract verifies and hardens the Frozen SRS/TDD semantics; it does not
introduce a new security model or permission model, new product capability, or
new UX capability.

## 3. Entry Criteria

- CC-03 acceptance gate is complete.
- Python, JavaScript, Browser, and HVR baseline evidence is saved.
- Formal tests do not install, import, or depend on SPIKE-02.
- CC-04 Chatter-aware Preview Layout is Frozen and complete.

## 4. Scope

### In scope

- activate, replace, update, clear, close, unmount, and re-enter lifecycle;
- rapid A→B, stale RPC, clear/close during loading, source change during
  loading, and unmount during request;
- page/source/target/request identity and same-target different-source
  isolation;
- model, record, and field permission changes, partial visibility, deleted
  records, and permission revocation;
- safe error classification and absence of display names, technical IDs,
  internal fields, tracebacks, SQL, and internal exception text;
- no, disabled, empty, invalid, and changed configuration;
- configuration changes while the source Form remains open, including an
  inactive config, changed target model, removed or reordered Preview fields,
  unreadable fields, and all configured fields becoming unreadable;
- standard Form, Notebook, Chatter, complex groups, scrolling, desktop,
  small-screen, and Tab + Extend mixed usage;
- Full Record navigation, popup behavior, leave/return, and formal operation
  without SPIKE-02 installed;
- final regression, upgrade-risk smoke checks, and test-layer summary.

## 5. Explicitly Out of Scope

- new business requirements or UX modes;
- editable Preview, multiple Pane/Profile, or generic Split View;
- cross-page or same-target Preview cache and background refresh;
- changes to Frozen SRS, TDD, or the product contract;
- Spike cleanup, migration, or uninstall work;
- modification of Odoo official source;
- `stock` dependency, business `sudo()`, raw SQL, or HTTP Controller.

## 6. Required Implementation Tasks

1. Build a complete lifecycle matrix and attach automated or Browser/HVR
   evidence to every transition.
2. Attack CC-03 page/source/target/request identity with rapid A→B→A,
   repeated activation, and out-of-order responses.
3. Verify clear/close/unmount during loading and source changes during
   loading. Where permission changes during an in-flight request are tested,
   verify that the final observable result remains consistent with the
   server-side access decision and Frozen DTO safety rules.
4. Test Loader behavior with restricted users and changing permissions.
5. Prove that disabled, empty, invalid, or changed configuration never uses
   cross-page stale state or cache.
6. Verify same-target different-source update and clear isolation.
7. Run Form, Notebook, Chatter, complex-layout, small-screen, scrolling, and
   Tab + Extend regression.
8. Verify installation, loading, and testing without SPIKE-02.
9. Record every failure and stop with `DESIGN CHANGE REQUIRED` if Frozen TDD
   or another frozen contract must change.

## 7. Verification Contract

### Python

- configuration changes and invalid fields;
- ACL, record-rule, field-read permission, deleted-record, and revoked-access
  behavior;
- DTO safety and error classification.

### JavaScript

- rapid A→B and stale-request protection;
- clear/close/unmount during loading;
- source identity isolation when targets are equal;
- re-entry cleanup, fallback rendering, and error handling.

### Browser

- standard Form, Notebook, Chatter, complex groups, and scrolling;
- desktop sibling and small-screen vertical layout;
- Tab + Extend mixed usage;
- Full Record, popup behavior, and leave/return.

### HVR

HVR covers human-observable regression and security-visible behavior that
automation cannot sufficiently establish:

- restricted users see only safe access-denied behavior;
- configuration changes do not visibly expose stale Preview content;
- revoked access does not leave previously visible target information in the
  Preview;
- native Many2one selection, search, create, clear, display, and open
  behavior remains usable;
- standard Tab navigation remains usable;
- wide Chatter-aware layout remains usable after hardening changes;
- narrow Form → Preview → Chatter layout remains usable.

## 8. Acceptance Gate

CC-05 may close only when all of the following are evidenced:

1. CC-01 through CC-04 Python, JavaScript, Browser, and HVR results remain
   traceable.
2. Lifecycle and concurrency scenarios pass; stale responses cannot
   repopulate the current Pane.
3. Same-target different-source isolation passes.
4. Model, record, field, and configuration-change cases disclose no
   forbidden information.
5. No configuration, disabled, empty, invalid-field, and error paths follow
   the Frozen SRS/TDD semantics.
6. Desktop, small-screen, Notebook, Chatter, complex groups, and scrolling do
   not break the primary Form.
7. The formal module has no SPIKE-02 dependency, no modification to Odoo
   official source files, no `stock` dependency, and no business-record
   `sudo()` used to bypass current-user access semantics.
8. Regression and upgrade-risk smoke results meet the release threshold
   explicitly recorded for this Contract Review; every failure has a
   disposition.
9. No new product capability, UX mode, configuration model, or persistent
   state mechanism is introduced under CC-05 without a new approved Change
   Control.

## 9. Failure and Stop Conditions

Stop and return to Contract Review if:

- any security case leaks display name, technical ID, internal field, SQL,
  traceback, or internal exception text;
- a stale response repopulates a Pane after clear, close, or unmount;
- native Many2one or standard Tab behavior regresses;
- small-screen layout covers the business area, or Notebook, Chatter, or
  scrolling becomes unusable;
- configuration changes require cross-page persistent cache;
- Frozen SRS, TDD, or an already Frozen Contract must change.
- a proposed change adds product capability, UX mode, configuration model, or
  persistent state rather than hardening existing behavior.

## 10. Traceability

- SRS: MVP, exception, permission, NFR, and acceptance requirements.
- TDD: sections 13, 16, 20–28, 31–33 and TD-007–TD-014.
- TVR: RUN-005/RUN-006, EXP-002-A–G and TVQ-05/06.
- Implementation Plan: historical hardening round labelled CC-04; this Draft
  uses CC-05 after CC-04 Chatter-aware Preview Layout was inserted. The
  renumbering changes document identity only, not hardening scope.

## 11. Authorization Boundary

This Frozen Contract is closed. Later hardening or new capability requires a
new Change Control.
