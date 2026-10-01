# Position Note Schema

Use this structure for positional control in BJJ.

## Metadata

Start every position note with YAML frontmatter using this structure:

---
type: position
gi: nogi
---

- `type` must always be `position`.
- `gi` must be `gi`, `nogi`, or `both`. Only use information provided by the user. If the user does not specify the context, use `nogi` as the default.
- Position notes do not use `from` or `to`. They represent positional nodes rather than transitions between positions.
- Add `variant_of: "[[...]]"` only when the note describes a specific variation of a broader position.
- Do not add `variant_of` to a general position note.

IMPORTANT:

- Always include the tag: #position
- The section below marked "EXAMPLE — REFERENCE ONLY" is illustrative only.
- Do NOT copy its content, wording, technique names, or technical details into your output.
- The example only demonstrates the expected structure, formatting, and possible level of detail.
- The example does NOT imply that every section must contain content.
- User input is the source of truth. Do NOT fill missing sections by inferring, reversing, or generating information from general BJJ knowledge.
- If the user did not provide information for a required section, keep the section and write only `* TBD`.
- Avoid inventing content even if the example contains information for that section.

---

#position

---

# Attack (Top)

## Submissions

* [[...]]
* [[...]]

## Control

* How do you maintain control?
* What are the key pressure points?

## Transitions

* [[...]]
* [[...]]

---

# Defense (Bottom)

## Escapes

* [[...]]
* [[...]]

## Problems

* Common issues when stuck in this position
* What makes escaping difficult?

## Reactions

* What should you try to do first?
* Key defensive principles (frames, hip movement, space)

---

---

# EXAMPLE — REFERENCE ONLY (Mount)

**(Do not include this section or its content in your generated output. It exists only to show the expected structure and depth.)**

---
type: position
gi: nogi
---

# Attack (Top)

## Submissions

* [[Armbar]]
* [[Triangle]]
* [[Ezekiel-Choke]]

## Control

* Keep weight low and centered
* Control opponent's upper body
* Prevent frames from being established

## Transitions

* [[Back-Control]]
* [[Knee-On-Belly]]

---

# Defense (Bottom)

## Escapes

* [[Bridge-Escape]]
* [[Knee-Elbow-Escape]]

## Problems

* Cannot establish frames
* Neck becomes exposed when reaching
* Opponent controls posture

## Reactions

* Create frames early
* Bridge to disrupt balance
* Create space before attempting escape