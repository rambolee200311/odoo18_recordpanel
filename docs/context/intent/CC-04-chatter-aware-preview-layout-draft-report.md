# CC-04 Chatter-aware Preview Layout — Draft Report

## Review status

**Frozen as CC-04 v1.0.0 / Implementation Completed**

## Basis

This Draft is based on the accepted CC-04 Chatter-aware Preview Layout
Requirement and preserves the CC-03 v1.0.0 Frozen boundary.

## Draft decisions

- Native Form/Chatter layout is unchanged while Preview is closed.
- Wide active Preview prioritizes `Business Form | Preview`; native Chatter
  moves below the Business Form area when present.
- Narrow active Preview orders `Business Form → Preview → Chatter`.
- Forms without Chatter receive no Chatter placeholder.
- Preview close restores native layout without business mutation or reload.
- Chatter remains native; no clone, custom implementation, or data-model
  change is allowed.
- Breakpoint values remain implementation details until technical review.

## Pre-Freeze closure

The following were resolved before CC-04 Freeze:

1. Stable Odoo 18 Form/Chatter integration boundary.
2. Reliable detection of a native Chatter host without placeholder creation.
3. Responsive breakpoint selected from native behavior and Browser evidence.
4. Reversible integration that demonstrably preserves unsaved Form state.

## Frozen authorization boundary

CC-04 Freeze authorizes only the completed implementation within this
contract. It does not authorize:

- modification of CC-03;
- modification of Odoo official source;
- work on later change controls.
