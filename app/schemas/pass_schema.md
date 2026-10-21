# Pass Note Schema

Use this structure for guard passing techniques.

## Metadata

Start every pass note with YAML frontmatter using this structure:

---
type: pass
gi: nogi
from:
  - "[[...]]"
to:
  - "[[...]]"
---

- `type` must always be `pass`.
- `gi` must be `gi`, `nogi`, or `both`. Only use information provided by the user. If the user does not specify the context, use `nogi` as the default.
- `from` contains the concrete positions from which the pass starts.
- `to` contains the concrete positions that can be reached as a result of successfully performing the pass.
- `from` and `to` must be YAML lists of Wiki-Links. If the corresponding information was not provided, use `[]`.
- Only positions belong in `from` and `to`. Follow-up submissions or other techniques remain in the appropriate note sections and must not be added to `to`.
- Add `variant_of: "[[...]]"` only when the note describes a specific variation or application of a broader pass.
- Do not add `variant_of` to a general pass note.

IMPORTANT:

- Always include the tag: #pass
- The section below marked "EXAMPLE — REFERENCE ONLY" is illustrative only.
- Do NOT copy its content, wording, technique names, or technical details into your output.
- The example only demonstrates the expected structure, formatting, and possible level of detail.
- The example does NOT imply that every section must contain content.
- User input is the source of truth. Do NOT fill missing sections by inferring, reversing, or generating information from general BJJ knowledge.
- If the user did not provide information for a required section, keep the section and write only `* TBD`.
- Avoid inventing content even if the example contains information for that section.

---

#pass

---

# Attack (Top)

## Setup

* From which positions or situations does this pass work?
* What initial control or position is required?

## Execution

* Step-by-step explanation of the pass
* Focus on:
  * positioning
  * movement
  * control during transition

## Follow-Ups

* [[...]]
* [[...]]

## Control After Pass

* How do you stabilize the position?
* How do you prevent re-guard?

## Problems

* What commonly goes wrong?
* How does the opponent interrupt the pass?

## Hints

* Key concepts (timing, pressure, explosiveness, control)

---

# Defense (Bottom)

## Reactions / Defense

* How can the opponent defend?
* What should be done early?

## Problems

* What mistakes lead to getting passed?

---

---

# EXAMPLE — REFERENCE ONLY (Chest-Ride-Pass)

**(Do not include this section or its content in your generated output. It exists only to show the expected structure and depth.)**

---
type: pass
gi: nogi
from:
  - "[[Knee-On-Belly]]"
to:
  - "[[Mount]]"
---

# Attack (Top)

## Setup

* Possible from [[Knee-On-Belly]]
* Right leg placed on the belly

## Execution (Pass From Left Side)

* Place left leg on opponent's chest
* Rotate 180° to face the legs
* Continue rotation along opponent's legs
* End almost in a full 360° rotation
* Keep head elevated to avoid being swept

## Follow-Ups

* With one arm trapped → [[Armbar]] or [[Triangle]]
* With both arms trapped → transition to [[Mount]]
* If no arm control → maintain posture, possible no-hand [[Triangle]]

## Control After Pass

* Keep hips low
* Keep opponent flat
* Do not allow space (prevent re-guard)

## Problems

* Too slow → opponent frames or turns in

## Hints

* Explosiveness + timing are more important than strength
* Movement must be continuous (no stopping mid-pass)

---

# Defense (Bottom)

## Reactions / Defense

* Use frames against hips and upper body
* Stop rotation early
* Insert legs → recover guard
* Create space instead of staying flat

## Problems

* Reacting too late to the rotation