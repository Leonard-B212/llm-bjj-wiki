# Sweep Note Schema

Use this structure for sweep techniques.

## Metadata

Start every sweep note with YAML frontmatter using this structure:

---
type: sweep
gi: nogi
from:
  - "[[...]]"
to:
  - "[[...]]"
---

- `type` must always be `sweep`.
- `gi` must be `gi`, `nogi`, or `both`. Only use information provided by the user. If the user does not specify the context, use `nogi` as the default.
- `from` contains the concrete positions from which the sweep starts.
- `to` contains the concrete positions reached by successfully performing the sweep.
- `from` and `to` must be YAML lists of Wiki-Links. If the corresponding information was not provided, use `[]`.
- Add `variant_of: "[[...]]"` only when the note describes a specific variation or application of a broader sweep.
- Do not add `variant_of` to a general sweep note.

IMPORTANT:

- Always include the tag: #sweep
- The section below marked "EXAMPLE — REFERENCE ONLY" is illustrative only.
- Do NOT copy its content, wording, technique names, or technical details into your output.
- The example only demonstrates the expected structure, formatting, and possible level of detail.
- The example does NOT imply that every section must contain content.
- User input is the source of truth. Do NOT fill missing sections by inferring, reversing, or generating information from general BJJ knowledge.
- If the user did not provide information for a required section, keep the section and write only `* TBD`.
- Avoid inventing content even if the example contains information for that section.

---

#sweep

---

# Attack

## Works When

* Under which conditions does the sweep work?
* Opponent weight distribution, posture, base

## Setup

* How do you prepare the sweep?
* What grips / controls are needed?
* How do you isolate the opponent?

## Execution

* Step-by-step execution
* Focus on:
  * off-balancing (kuzushi)
  * timing
  * direction of movement

## Leads To

* [[...]]
* [[...]]

## Problems

* What commonly goes wrong?
* When does the sweep fail?

## If Blocked / Combinations

* [[...]]
* [[...]]

---

# Defense

## Reactions

* How does the opponent defend?
* How can they prevent the sweep?

## Problems

* What leads to getting swept?

---

---

# EXAMPLE — REFERENCE ONLY (Pendulum-Sweep)

**(Do not include this section or its content in your generated output. It exists only to show the expected structure and depth.)**

---
type: sweep
gi: nogi
from: []
to:
  - "[[Mount]]"
---

# Attack

## Works When

* Opponent shifts weight forward
* Arm is on chest / isolatable
* Opponent has weak base (no strong posting)

## Setup

* Pull arm across chest → back slightly exposed
* Control the head
* Trap the arm
* Ideally left hand on opponent's rear lat to secure the trap

## Execution

* Open guard
* Bring hand between legs
* Use pendulum motion with the leg
* Off-balance opponent
* Sweep and land in [[Mount]]

## Leads To

* [[Mount]]

## Problems

* Opponent posts with free arm
* Weight too far back → cannot off-balance

## If Blocked / Combinations

* Opponent posts → switch direction
* Opponent pulls arm back → alternative sweep or [[Armbar]]

---

# Defense

## Reactions

* Widen base (post)
* Shift weight backward
* Prevent arm from being isolated

## Problems

* Arm gets isolated
* Weight too far forward