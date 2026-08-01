# Lesson 2 — Run sheet (instructor-only)

> Lab `code/`: **00-setup** + **01–06** — raw HTTP → boto3 Converse → real prompt → streaming → reasoning (extended thinking) → prompts-as-code (template builder). The **foundations** half: *calling* the model. Structured output / schema / validation / context engineering live in **Lesson 3**.
> **SDD rebuild target: 06** (`06-prompt-template.py`). Phases 4–5 are 06 only — the scaffold ships just what 06 needs.

## Six phases

| # | Phase | Time | Focus |
|---|---|---|---|
| 1 | Presentation | 30–45 | Concepts, no code. |
| 2 | Reference walkthrough | ~30 | Walk `code/` live. **Skim 01–04, quickly demo 05 (reasoning on — but Nova redacts the trace; show the token counter), dwell on 03 + 06.** |
| 3 | Lab exploration | 20–30 | Students run + interrogate via `code/PROMPTS.md`. |
| 4 | SDD discussion | 15–20 | How to spec 06: constraints in `PROMPT.md` vs design choices left open vs a skill. |
| 5 | Student build | 30–45 | Rebuild 06 in `SDD/`, then `validate-lab`. |
| 6 | Review *(opt)* | 10–15 | Compare static/dynamic splits + builders. Cut first if short. |

This is the **onboarding** lesson: first contact with AWS setup, `.env`/venv/`setup.sh`, the lab format, Claude Code, and the first SDD rebuild. The concepts (01–06) are a deliberately gentle ramp so attention can go to the machinery — the rebuild target (06) is approachable on purpose. The genuinely hard concepts come in Lesson 3, once the format is second nature.

**Concept spine (Phase 1):** endpoint = HTTP POST → what the SDK hides (URL, SigV4, transient retries) → real prompt (system/user, inferenceConfig) → streaming = delivery, not API → extended thinking = opt-in reasoning (off by default; effort low/med/high; **Nova redacts the trace — you pay for thinking you can't read**) → prompts are **code** (static cacheable prefix + a dynamic builder/template). Land **"the same call shape recurs"** and **"prompts are code you compose"** hardest.

## Exercises — walkthrough hook · watch for

| File | Hook (walkthrough) | Watch for |
|---|---|---|
| `01-http-raw` | call = one `requests.post` to Bedrock Converse with a Bearer token | needs `AWS_BEARER_TOKEN_BEDROCK` (401/403 → setup / model access) |
| `02-basic-call` | diff vs 01: URL/signing/retries → boto3; response still raw (dump shows the envelope) | first real Bedrock call (skipped-setup caught here); Converse not `invoke_model` |
| `03-summarize` | system/user split + inferenceConfig — the reused call shape | students restate the instruction in the user msg; system already did it. temp A/B (1.0×3 vs 0.0×3) to feel it |
| `04-streaming` | `converse_stream`, same call; only `contentBlockDelta` matters | not a different API or model mode — bytes just arrive incrementally |
| `05-reasoning` | `converse_stream` + `reasoningConfig` effort (low/med/high); `reasoningContent` streams *before* `text` but **redacted to `[REDACTED]`**; token counter shows the hidden cost | reasoning **off by default** (opt-in knob); **Nova redacts the trace** — great teaching beat (providers differ: Claude summarizes, Nova hides); at `high` effort `temperature`/`topP`/`maxTokens` must be unset or Bedrock 400s |
| **`06-prompt-template`** ⟵ rebuild | interactive: three menus (focus / format / length) → `build_request_prompt()` splices the chosen fragments; static `SYSTEM_PROMPT` kept separate | **constrain the input (menu) not free text → predictable output**; = rebuild divergences below |

## Discussion & build (06)

**Phase 3 — seed the room** (from `code/PROMPTS.md`):
- "Why menus instead of a free-text request?" → a known input space → predictable output; the input-side cousin of structured output.
- "What's static vs dynamic in 06, and which half would a cache reward?" → static prefix / dynamic payload.
- Manual: add a fourth menu (e.g. AUDIENCE), or swap one menu for a free-text `input()` and watch the output shape get unpredictable — that's the determinism point, broken on purpose.

**Phase 4 — SDD discussion** (what sits in `PROMPT.md` *is* the conversation):
- **Constraints vs task** — stack rules (boto3 Converse, env config, one call function) are in `PROMPT.md`'s Constraints; the *what* (menus, fragments, static/dynamic split) is left as `▢ YOU DECIDE`. Right line?
- **Where does a prompt template live** — inline / a builder function / a versioned prompt store? When does a prompt graduate out of code?
- **Deliberate omissions** — `PROMPT.md` withholds the variable choice and the static/dynamic boundary. Right things to leave to the student?

**Phase 5 — divergence traps** (the happy path hides them; "it printed a summary" ≠ done):
1. A free-text `input("what do you want?")` instead of **constrained menus** — misses the whole point; the input space must be known.
2. A chosen option is **read but never spliced into the prompt** — every run comes back the same. The builder must interpolate all the choices.
3. The per-call choices leak into the **static** system prompt — breaks the static/dynamic split (and a real cache).
4. **No input validation** — a bad/out-of-range pick crashes or is silently accepted.

**Validate:** from `SDD/`, *"Run validate-lab against my `06-prompt-template.py`."* Scores /100 (can exceed 100), per-check gaps, cheat prompt for anyone out of time.

**Phase 6:** read out 2–3 builds — the live divergence is which dimensions each made into menus, whether every choice actually reached the prompt, and whether anyone left a free-text escape hatch.

**The takeaway to land (debrief).** Most builds score ~90+ from a near-empty prompt — surface that, don't apologize for it. The point isn't a clever agent; it's that for a well-specified, **convergent** task the agent does the mechanical build, and the leverage is (1) describing the use case clearly + (2) the last mile (menu options, fragment wording, static/dynamic split). **That's spec-driven development in one lab — you don't hand-write the tool, you specify it and fine-tune.** Hook for L3: its exercises genuinely diverge, so spec quality actually separates builds there.

## Setup (00) — flag once, recurs every lab

First lesson shipping code → first contact with `setup.sh`, repo-rooted `.env`, shared `.venv`. ~5 min up front:
- **Sourced, not executed** — venv activation only persists in the sourcing shell (script errors if executed).
- **Two-run pattern** — run 1 seeds `.env` and stops → student fills keys → run 2 does venv→deps→Bedrock smoke test. Intentional friction before a paid API.
- **One `.env`, above the lab**; Python finds it via `find_dotenv()`. Show the `→ Env root:` line.
- **Gotchas:** setup only seeds when `.env` is missing → `.env.example` edits don't propagate (hand-edit or delete+re-source); per-lab `.env.example` snapshot can drift from root.
- **Stuck students** → the "Getting help when setup fails" section in `00-aws-setup.md`; it *is* the structured-error-sharing lesson. Make them write the error in that format first — they often self-solve.
- **Pre-class:** have a clean AWS sandbox ready to screenshot — enabling **Model access** for Nova 2 Lite is the #1 first-time blocker (Amazon's own models skip the Anthropic use-case form, but access still has to be toggled on).

## Homework (`homework/README.md`) — "what a basic call leaves on the table: memory, cost, autonomy"

- **Multi-turn** (extends 03) — Converse is **stateless**; *you* hold history and resend it each turn. "The model remembers" is wrong; "I choose what to remind it of" is right. Watch input tokens grow.
- **Prompt caching** (extends 03) — large stable prefix + varying suffix. Add a `cachePoint`, repeat the transcript past the min-token threshold, read `cacheWrite/ReadInputTokens`. The concrete payoff of 06's static/dynamic split (and a bridge to Lesson 3's context engineering).
- **Model drives the menu** (extends 06 + 05) — hand the FOCUSES/FORMATS/LENGTHS to the *model*, turn on extended thinking, let it pick + justify + act (escalate on high churn risk). **reason → choose-from-a-bounded-set → act** = an agent in miniature; the menu is the safe action space. The teaser for where the course is heading (agents).
