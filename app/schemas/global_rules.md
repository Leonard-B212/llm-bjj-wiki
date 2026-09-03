# Global Note Writing Rules

## Output Structure

- Do NOT include the title as a heading.
- Do not include unnecessary explanations outside the note content itself.
- Always include every heading and subheading defined in the schema, even if no information was provided for it. In that case, write a single placeholder bullet: `* TBD`.
- Do not skip, merge, or omit schema sections for any reason.

## Language and Terminology

- Technique names and wiki links must use standard English BJJ names.
- Descriptive content must be written in {LANGUAGE}.
- Keep established Brazilian Jiu-Jitsu terminology in English, even when descriptive content is written in another language.
- Do not translate common BJJ terms such as Underhook, Overhook, Crossface, Bridge, Shrimp, Guard, Mount, Side Control, Scramble, Frame, Base, Grip, Hook, Post, or Reversal into the content language.
- Use the commonly established BJJ term instead of a literal translation.
  - Example: use `Underhook`, never `Unterhaken`.

## Wiki Links

### Canonical Entities

- Existing note titles are canonical wiki entities. If a referenced concept matches an existing note, ALWAYS use its exact title as the link target.
- Links to non-existing notes are allowed when they represent a genuine BJJ entity that could reasonably have its own note.
- Do not avoid a meaningful wiki link merely because the target note does not exist yet. The link should remain valid if that note is created in the future.
- Top/bottom and offensive/defensive describe perspective, not separate position entities.
  - Example: "top Side Control" and "bottom Side Control" both refer to `[[Side-Control]]`, not `[[Top-Side-Control]]` or `[[Bottom-Side-Control]]`.

### Parent Techniques and Variations

- A note that intentionally describes a specific variation, entry, or application of a broader technique MUST link to its parent technique.
- This parent link is required even if the parent note does not exist yet.
  - Example: a note about `Calf-Slicer-from-Turtle` must link to `[[Calf-Slicer]]`.
- Do not create a self-link to the note currently being written.

### Entity Hierarchy

- Distinguish between broad BJJ categories and concrete BJJ entities.
- Broad categories classify entities and must NOT be used as wiki link targets merely because they describe what kind of technique or position something is.
- Wiki links should point to concrete BJJ concepts below the broad category level rather than to the category itself.

Examples:
- `Position` → `[[Side-Control]]`, `[[Mount]]`, `[[Turtle]]`
- `Guard` → `[[Closed-Guard]]`, `[[Open-Guard]]`, `[[Butterfly-Guard]]`, `[[Half-Guard]]`
- `Submission` → `[[Armbar]]`, `[[Calf-Slicer]]`, `[[Triangle-Choke]]`
- `Sweep` → `[[Butterfly-Sweep]]`
- `Pass` → `[[Knee-Slice]]`
- `Escape` → `[[Knee-Elbow-Escape]]`
- `Takedown` → a specific named takedown
- `Throw` → a specific named throw

- Concrete entities may themselves have more specific variations, entries, or applications below them.
- These more specific notes should link back to their meaningful parent entity.
  - Example: `Calf-Slicer-from-Turtle` → `[[Calf-Slicer]]`.
- Do NOT link the broad category itself when it is only being used as a classification.
  - Example: write `sweep`, not `[[Sweep]]`.
  - Example: write `submission`, not `[[Submission]]`.
  - Example: write `position`, not `[[Position]]`.

### What Should Be Linked

Create wiki links for meaningful relationships to concrete BJJ entities, especially:

- Parent techniques of variations or specific entries.
- Positions or Guards the technique meaningfully works from.
- Positions the technique meaningfully leads to.
- Specific submissions, sweeps, passes, escapes, takedowns, throws, or other techniques used as follow-ups, counters, combinations, or transitions.

All wiki link targets must use Hyphen-Case and standard English BJJ terminology: every word starts with a capital letter, words are separated by hyphens, and no spaces are used.

Examples:
- `[[Side-Control]]`
- `[[Knee-Elbow-Escape]]`
- `[[Bow-and-Arrow-Choke]]`

### What Should NOT Be Linked

- Do NOT link broad category or classification words such as `Position`, `Guard`, `Submission`, `Sweep`, `Pass`, `Escape`, `Takedown`, or `Throw` when they are only describing the type of a concrete BJJ entity.
  - Example: in "the opponent can counter with a sweep", write `sweep`, not `[[Sweep]]`.
  - A specific named sweep such as `[[Butterfly-Sweep]]` is a valid wiki entity.
- Do NOT create wiki links for generic BJJ mechanics, grips, controls, body parts, or movement concepts such as S-Grip, Underhook, Overhook, Crossface, Frame, Base, Shrimp, Bridge, Grip, Hook, Post, Butterfly Hook, Collar Tie, Shoulder Pin, Upper-Body Pressure, or Wedge.
  - Example: write `Underhook` and `Crossface`, not `[[Underhook]]` or `[[Crossface]]`.
- Mention these concepts as normal text when they are relevant to the technique.
- Do not invent wiki entities merely to create additional links.