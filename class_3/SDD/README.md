# Lesson 3 — API Endpoints, Advanced · Spec-Driven Build (SDD)

The build-it-yourself half of Lesson 3. You've studied the worked lab in
[`../code/`](../code/); now **rebuild** its culminating script —
`03-validate-and-retry.py` — from a spec, driving a coding agent with `PROMPT.md`,
then score yourself with the `validate-lab` skill.

## How it works

You build in a **fresh clone of the build slate** so your agent starts from a
blank slate — no answer key, no rubric to game, no dependency hints. You clone
**just** the standalone `lesson-03-api-endpoints-advanced-sdd` repo (§1), so the
reference answer isn't even downloaded. This `SDD/` folder holds the **task** (`PROMPT.md`)
and the **validator** (`validate-lab/`).

## 1. Get a clean build workspace

Clone **just the build slate** into a fresh folder — also sent via WhatsApp /
Google Drive:

```bash
git clone "https://github.com/Dgotlieb/AIEngineer.git"
cd AIEngineer/class_3_new/SDD
# create a working .env here (your AWS creds + BEDROCK_MODEL_ID) before the next line
source setup.sh                  # venv + base deps (boto3, python-dotenv) + Bedrock smoke test
mv CLAUDE.md-example CLAUDE.md   # activate the build conventions your agent reads
```

> The slate is deliberately bare — **setup + conventions only**, no `PROMPT.md`,
> no `requirements.txt`, no answer, no `.env.example`. **Bring your own `.env`** —
> the same AWS creds you use for this lesson.
>
> Your agent will need `jsonschema` and `tenacity` for this lab — let it install
> those as it goes (the base setup only ships boto3 + python-dotenv).
>
> **On Windows?** Run these from Git Bash (easiest via VS Code's integrated terminal).

## 2. Build

Hand your agent the task — **`PROMPT.md` in this `SDD/` folder** (open it and paste
it, or point your agent at it). It's a *partial* spec; the load-bearing decisions
are yours (the `▢ YOU DECIDE` block). Build `03-validate-and-retry.py` in your
build folder, run it, iterate:

```bash
python 03-validate-and-retry.py
```

## 3. Validate

Back here in this lesson's `SDD/` folder, invoke the **validate-lab** skill. It
asks for the path to your build folder, then scores your `03-validate-and-retry.py`
against the reference `../code/03-validate-and-retry.py` out of 100 — naming what's
missing / weaker / better, with a cheat prompt if you're out of time.
