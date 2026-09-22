# IHR-CC-04 Chatter-aware Preview Layout

## Status

Implementation completed for CC-04 v1.0.0. All designated HVR items have been
accepted, including wide, narrow, XXL, no-Chatter, native-Chatter, unsaved
state, and overlap checks. CC-04 is Frozen; later layout features require a
new Change Control.

## Implemented

- Native layout remains unchanged while Preview is closed.
- Wide active Preview uses Form/Preview as the primary horizontal relationship.
- Native Chatter remains below the Business Form area.
- Narrow active Preview orders Form, Preview, then Chatter.
- Forms without Chatter do not receive a placeholder.
- Closing Preview removes the active layout behavior.
- Existing CC-03 Preview and CC-02 navigation behavior are preserved.

## Technical boundary

The implementation is limited to module CSS in
`static/src/preview/preview.scss`. It does not modify Odoo official source,
Chatter components, Chatter data, or business records.

## Frozen stop point

CC-04 implementation and verification are complete. Do not expand to
unrelated layout features or enter a later Change Control.
