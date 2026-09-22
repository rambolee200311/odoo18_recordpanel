# CC-04 Chatter-aware Preview Layout Requirement

## Status

Accepted requirement input. This document is an input to the future CC-04
Hardening & Integration contract. It does not modify or expand CC-03 v1.0.0
Frozen and does not authorize production implementation.

## Purpose

When a Many2one `extend` Preview is active, adapt the relationship between the
Business Form, Preview Pane, and the native Chatter so that the Form remains
usable without hiding, duplicating, or reimplementing Chatter.

## Required layout semantics

### Preview closed

Preserve the native Odoo Form/Chatter layout exactly. Do not create a Preview
placeholder or move Chatter while Preview is inactive.

### Wide viewport, Preview active, Chatter present

Use the primary horizontal relationship:

```text
Business Form | Preview Panel
Chatter       |
```

Chatter moves below the Business Form area and no longer competes with the
Preview for the Form's right-side space.

### Narrow viewport, Preview active, Chatter present

The required order is:

```text
Business Form
Preview Panel
Chatter
```

Preview must remain between the Form and Chatter.

### Preview active without Chatter

Use only the Form and Preview:

```text
Wide:   Business Form | Preview Panel
Narrow: Business Form → Preview Panel
```

Do not create Chatter or an empty Chatter placeholder.

### Preview close

Remove the Preview layout influence and restore the native Form/Chatter
relationship without reloading the business record, saving the Form, changing
business values, or losing unsaved state.

## Preservation and safety rules

- Keep the native Chatter component and all of its existing capabilities.
- Do not hide, copy, replace, or reimplement Chatter.
- Keep Preview read-only, single, page-scoped, and non-overlapping.
- Do not change Preview data semantics or the CC-02 full-record navigation
  contract.
- Layout transitions must not write business data or modify Many2one values.
- Do not modify Odoo official source files.

## Acceptance inputs for CC-04

- Native layout is unchanged while Preview is closed.
- Wide active layout places Form and Preview side by side with Chatter below
  the Form area.
- Narrow active layout orders Form, Preview, then Chatter.
- Forms without Chatter receive no Chatter placeholder.
- Native Chatter actions remain usable.
- Closing Preview restores native layout without business mutation or loss of
  unsaved state.
- Form, Preview, and Chatter never overlap at supported widths.

The concrete responsive breakpoint is intentionally left to the CC-04
technical design and browser verification; this requirement freezes relative
layout semantics, not a numeric breakpoint.

## Explicit scope boundary

This requirement does not authorize implementation. It does not include
manual position selection, configurable widths, drag/resizable split panes,
multiple Preview Panes, generic Split View, editable Preview, embedded or
custom Chatter, Chatter data-model changes, or user permission changes.
