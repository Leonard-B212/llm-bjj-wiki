# Escape Note Schema

Use this structure for escape techniques.

## Metadata

Start every escape note with YAML frontmatter using this structure:

---
type: escape
gi: nogi
from:
  - "[[...]]"
to:
  - "[[...]]"
---

- `type` must always be `escape`.
- `gi` must be `gi`, `nogi`, or `both`. Only use information provided by the user. If the user does not specify the context, use `nogi` as the default.
- `from` contains the concrete positions from which the escape starts.
- `to` contains the concrete positions reached by successfully performing the escape.
- `from` and `to` must be YAML lists of Wiki-Links. If the corresponding information was not provided, use `[]`.
- Add `variant_of: "[[...]]"` only when the note describes a specific variation or application of a broader escape.
- Do not add `variant_of` to a general escape note.

IMPORTANT:

- Always include the tag: #escape
- The section below marked "EXAMPLE — REFERENCE ONLY" is illustrative only.
- Do NOT copy its content, wording, technique names, or technical details into your output.
- The example only demonstrates the expected structure, formatting, and possible level of detail.
- The example does NOT imply that every section must contain content.
- User input is the source of truth. Do NOT fill missing sections by inferring, reversing, or generating information from general BJJ knowledge.
- If the user did not provide information for a required section, keep the section and write only `* TBD`.
- Avoid inventing content even if the example contains information for that section.

---

#escape

---

# Goal

* From which position are you escaping?
* What is the target position?
* Typical targets: [[Half-Guard]], [[Guard]], or a better position

---

# Works From

* [[...]]
* [[...]]

---

# Setup

* What needs to be established first? (frames, positioning, timing)
* What conditions make this escape easier or harder?
* Optional: combinations with other escapes

---

# Execution

## Standard Variation

* Step-by-step explanation of the main escape
* Focus on:
  * Frames
  * Movement (hip, shoulders)
  * Creating space
  * Bringing in the knee / recovering position

## Variations (optional)

* Different situations (e.g. Mount, Side-Control)
* Adjustments depending on opponent behavior

---

# Key Details

* Key concepts (e.g. connection of knee and elbow)
* What must always be respected?
* What makes the technique work reliably?

---

# Problems

* What typically goes wrong?
* How does the opponent shut the escape down?

---

# If Blocked / Combinations

* [[...]]
* [[...]]

---

---

# EXAMPLE — REFERENCE ONLY (Knee-Elbow-Escape)

**(Do not include this section or its content in your generated output. It exists only to show the expected structure and depth.)**

---
type: escape
gi: nogi
from:
  - "[[Mount]]"
  - "[[Side-Control]]"
to:
  - "[[Half-Guard]]"
  - "[[Guard]]"
---

# Goal

* From Mount / Side Control back to [[Half-Guard]] or [[Guard]]

---

# Works From

* [[Mount]]
* [[Side-Control]]

---

# Setup

* Establish frames
* Read opponent's weight distribution
* Works better if opponent is not extremely low and heavy
* Often combined with [[Bridge-Escape]]

---

# Execution

## Standard Variation From Mount

* Establish frames
  * Left elbow inside opponent's knee (arm upright)
  * Right arm along the hip, hands connected for a stable frame
* Bring knee under opponent's leg
  * Slide your knee under the opponent's foot
  * If the foot is flat, create space with your other leg
* Push against the frame
* Recover to [[Half-Guard]] or [[Guard]]

## Variation From Side-Control

* Set frames
  * Bottom arm at the hip (against hip pressure)
  * Top arm at neck/shoulder (against crossface)
* Turn onto your side (most important step)
* Create space
  * Use frames
  * Shrimp hips away
* Insert knee
  * Bring top knee between bodies
  * Connect knee and elbow
* Secure position
  * Recover [[Half-Guard]]
  * Or go to [[Guard]] if enough space

---

# Key Details

* Connect elbow and knee
* Do not stay flat
* First create space, then bring the leg in

---

# Problems

* Opponent switches position (e.g. [[Knee-On-Belly]]) before entry

---

# If Blocked / Combinations

* [[Bridge-Escape]]
* [[Shrimp-Escape]]