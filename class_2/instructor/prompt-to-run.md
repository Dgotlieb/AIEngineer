# Prompt to run — Lesson 2 (build the SDD target, `06-prompt-template.py`)

> Instructor reference, not student-facing — this is the **answer-key prompt**. `SDD/PROMPT.md` ships to students *deliberately partial*: which dimensions become menus, the instruction fragment behind each option, the static-vs-dynamic boundary, and *why* menus beat a free-text request are left as the exercise. The prompt below is the **complete** version with every gap filled.
>
> **When to use it:** someone's stuck in Phase 5. Show it on screen, send it, or paste it yourself to demo the target build. Stack constraints already live in student `SDD/PROMPT.md` (boto3 Converse, env config, one call function); this cheat prompt fills only the design gaps. Produces code equivalent to `code/06-prompt-template.py`.

---

## The prompt

Build `06-prompt-template.py`: an interactive call-summary tool whose prompt is assembled **as code from constrained menu choices**, not from a free-text request.

**Three menus, defined as data.** Three option dicts, each mapping a short label to the instruction fragment that label injects into the prompt:
- `FOCUSES` — e.g. billing / retention / the open claim;
- `FORMATS` — email to customer (warm, greeting + sign-off) / email to manager (internal, lead with status & risk) / CRM note (terse, no greeting, bullet points);
- `LENGTHS` — concise (1-2 sentences) / short (3-4) / medium (a short paragraph).

**A chooser.** `choose(label, options)` prints a numbered menu (each option shown with its example), reads the user's pick, and **re-asks on invalid input** (non-numeric or out of range). Returning a key the template understands — rather than accepting free text — is the constraint that makes output predictable.

**A builder.** `build_request_prompt(transcript, focus, fmt, length)` returns the user message, splicing the three chosen instruction fragments + the transcript into one template. Pure function (no I/O), so it's testable.

**A static system prompt.** A module-level `SYSTEM_PROMPT` (analyst role + "produce exactly what's asked, stick to the transcript") with **no** per-call choices in it, passed via `system=[...]`.

**The call + flow.** Keep the Converse call in one function (`inferenceConfig` modest `maxTokens`, `temperature` ~0.3). In `main()`: read the transcript from `data/call1.txt`, run the three menus in turn (focus → format → length), then print `"Support-call Agent: here's what you asked for:"` followed by the model's deliverable. Read `BEDROCK_MODEL_ID` / `AWS_REGION` from the environment; exit clearly if the model ID is unset.

---

## What this fills in (vs. `SDD/PROMPT.md`'s ▢ YOU DECIDE)

| Decision left to the student | Answer baked in above |
|---|---|
| Which dimensions become menus? | focus, format, length (3 menus). |
| What's behind each option? | an instruction fragment spliced into the prompt — the menu value *is* the instruction. |
| Static system prompt vs dynamic builder? | role/rules are static (`SYSTEM_PROMPT`); the three choices + transcript are dynamic (`build_request_prompt`). |
| Why menus instead of free text? | a known, finite input space → predictable prompts → predictable output — the input-side cousin of structured output (Lesson 3). |

> If you hand this to an agent and it produces a *complete, correct* 06, that's the point — it's the cheat prompt. Tell students to reach for it **only when out of time**; the learning is in closing the gap themselves from the partial `PROMPT.md`.
