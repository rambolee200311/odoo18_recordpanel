# CC-04 Chatter-aware Preview Layout

## Status

**v1.0.0 Frozen — Implementation Completed**

This Draft follows the accepted [CC-04 Chatter-aware Preview Layout
Requirement](./CC-04-chatter-aware-preview-layout-requirement.md). It does not
modify CC-03 v1.0.0 Frozen. The user approved implementation and subsequently approved this contract for
Freeze. No scope beyond this contract is authorized.

## 1. Goal

Integrate the page-scoped CC-03 Preview Pane with the native Odoo Form and
native Chatter layout so that Preview activation does not compress the
Business Form through a three-column competition.

The layout change is reversible and applies only while Preview is active.

## 2. Scope

### In scope

- Preserve native Form/Chatter layout while Preview is closed.
- Wide active layout: `Business Form | Preview`, with Chatter below the
  Business Form area when Chatter exists.
- Narrow active layout: `Business Form → Preview → Chatter` when Chatter
  exists.
- Active Preview without Chatter: Form and Preview only.
- Restore native layout when Preview closes.
- Preserve native Chatter DOM, behavior, permissions, and capabilities.
- Prevent overlap and business mutations during layout transitions.
- Integrate with the existing single page-scoped CC-03 Preview Pane.

### Explicitly out of scope

- Multiple Preview Panes.
- Editable Preview or Preview-side business actions.
- Generic Split View.
- Resizable or user-configurable panes.
- Custom, copied, embedded, or reimplemented Chatter.
- Chatter data-model or permission changes.
- User-selected Form/Preview/Chatter positions.
- Numeric breakpoint as a business contract.
- Odoo official source modifications.

## 3. Layout Contract

### 3.1 Preview closed

```text
Native Odoo Form / Chatter Layout
```

No Preview placeholder or Chatter relocation is allowed.

### 3.2 Wide viewport, active Preview, Chatter present

```text
Business Form | Preview Panel
Chatter       |
```

The Preview remains beside the Business Form. Chatter remains native and
usable, but is placed below the Business Form area rather than competing for
the Form's right-side space.

### 3.3 Narrow viewport, active Preview, Chatter present

```text
Business Form
Preview Panel
Chatter
```

Preview must remain between the Form and Chatter.

### 3.4 Active Preview without Chatter

```text
Wide:   Business Form | Preview Panel
Narrow: Business Form → Preview Panel
```

No Chatter or empty Chatter placeholder may be created.

### 3.5 Preview close

Remove Preview layout influence and restore the page's native Form/Chatter
relationship without record reload, save, field mutation, or loss of unsaved
state.

## 4. Chatter Preservation Contract

CC-04 may reposition the native Chatter host only. It must not hide, clone,
replace, reimplement, or copy Chatter content. Existing capabilities such as
Send Message, Log Note, Activities, Messages, Attachments, and Followers must
remain available where they were available before activation.

## 5. Preview Preservation Contract

CC-04 does not change CC-03 Preview semantics. Preview remains a single,
page-scoped, read-only related-record panel and continues to reuse the CC-02
Navigation Builder for Open Full Record.

## 6. State and Safety Contract

- Layout state is page-scoped and tied to Preview active/closed state.
- Layout transitions must not write the business record.
- Layout transitions must not change Many2one values.
- Layout transitions must not trigger an automatic save.
- Closing Preview must preserve unsaved Form state.
- At most one Preview Pane and one native Chatter host may exist.
- Form, Preview, and Chatter must not overlap at supported viewport sizes.
- The concrete responsive breakpoint is an implementation detail subject to
  Odoo 18 behavior and Browser/HVR evidence.

## 7. Verification Contract

### Automated ATR

ATR must cover:

- native layout preservation while Preview is closed;
- active/closed layout state transitions;
- Chatter host preservation without duplication;
- no-Chatter branch without placeholder creation;
- Form/Preview/Chatter ordering and overlap guards;
- close restoration without save, reload, or field mutation;
- regression of CC-03 Preview state and CC-02 navigation.

### Browser/HVR

HVR is limited to designated human layout checks:

1. Preview closed preserves the native layout.
2. Wide viewport with Chatter places Form and Preview side by side and Chatter
   below the Form area.
3. Narrow viewport orders Form, Preview, then Chatter.
4. A Form without Chatter receives no Chatter placeholder.
5. Native Chatter actions remain usable after layout activation.
6. Closing Preview restores native layout and preserves unsaved state.
7. No visible overlap occurs at supported widths.

HVR does not duplicate detailed Python/JS race and mutation assertions.

## 8. Dependencies

- CC-03 v1.0.0 remains the Preview behavior baseline.
- CC-02 v1.0.0 Navigation Builder remains unchanged.
- Native Odoo Form and Chatter components remain the source of truth.

## 9. Resolved Contract Questions

1. Which Odoo 18 Form/Chatter host boundary is stable enough for a non-invasive
   sibling/reparenting integration without modifying official source?
2. How should the implementation detect that the current Form actually owns a
   native Chatter host, without creating a placeholder?
3. Which breakpoint preserves Odoo's native responsive behavior while meeting
   the required narrow ordering?
4. What is the smallest reversible DOM/layout mechanism that preserves
   unsaved Form state and native Chatter lifecycle?

- The existing native Form/Chatter host boundary is used without modifying
  Odoo official source.
- Chatter presence is derived from the existing native host; no placeholder is
  created for Forms without Chatter.
- The responsive breakpoint is an implementation detail validated against
  Odoo 18 behavior and browser evidence.
- CSS-only activation and removal preserve the existing DOM and Form state.

## 10. Stop Conditions

Stop and return to Contract Review if:

- satisfying the ordering requires modifying Odoo official source;
- Chatter must be cloned, replaced, or reimplemented;
- preserving unsaved Form state cannot be demonstrated;
- a stable no-Chatter detection boundary cannot be established;
- a proposed solution changes CC-03 Preview semantics or CC-02 navigation.

## 11. Acceptance Gate

CC-04 was approved for Freeze after ATR completion and browser/HVR validation.
The frozen scope is closed; later layout features require a new Change
Control.
