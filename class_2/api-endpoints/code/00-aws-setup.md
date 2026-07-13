# Exercise 00 — Set up AWS Bedrock

This is a one-time setup that prepares your AWS account to run every exercise in this lab (01–06). There is no Python code here — it's a walkthrough of the AWS console plus a smoke test at the end.

If you hit a snag, see [**Getting help when setup fails**](#getting-help-when-setup-fails) at the bottom — it shows the *format* in which to share an error or screenshot with Claude so you get a useful answer fast.

## What you'll do

1. Sign in to AWS (or create an account).
2. Generate an Amazon Bedrock API key (bearer token).
3. Run `setup.sh` to seed `.env`, fill in your API key (and confirm the model ID in the Bedrock console), then re-run `setup.sh` to verify Bedrock works end-to-end.

> ⚠️ **Use a personal sandbox AWS account, or an explicit "course" account.** Don't run lab exercises against a production AWS account. The total cost of running every exercise in this course is roughly **a few cents to under a dollar** — but you're responsible for any charges.

---

## Step 1 — AWS account

If you don't have an AWS account, sign up at https://aws.amazon.com/. New accounts get a free tier, though Bedrock itself is pay-per-token (no free tier for inference).

## Step 2 — Generate a Bedrock API key

Bedrock supports API keys that authenticate as a **bearer token** — no IAM access-key / secret-key pair required. Exercise 01 sends it as an `Authorization: Bearer …` header; boto3 (exercises 02+) reads the same key from `AWS_BEARER_TOKEN_BEDROCK` automatically.

There are two key types:

- **Long-term** — lasts until a configured expiration (up to 365 days). Best for local course work; this is what the labs assume.
- **Short-term** — lasts up to 12 hours (or until your console session ends). Prefer this for production, not for a multi-day lab. Short-term keys are also **region-scoped**: `AWS_REGION` in `.env` must match the console region you used when generating the key.

Generate a long-term key:

1. Open the Bedrock console: https://console.aws.amazon.com/bedrock/
2. Set the region selector (top-right) to the region you'll put in `.env` (usually `us-east-1`).
3. In the left sidebar, click **API keys**.
4. Open the **Long-term API keys** tab → **Generate long-term API keys**.
5. Choose an expiration (30 or 90 days is fine for the course) and click **Generate**.
6. **Copy the key now.** It is shown only once. It usually starts with `bedrock-api-key-`.

Generating a long-term key creates a dedicated IAM user with Bedrock permissions attached for you — you do **not** need to create an IAM user or access keys separately for this course.

> Official reference: [Amazon Bedrock API keys](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html)

## Step 3 — Configure `.env` and verify with `setup.sh`

The setup script handles `.env` for you. You'll run it twice: once to seed the file, and again — after you fill in your API key and confirm the model ID — to actually verify Bedrock works.

> **On Windows?** Run `setup.sh` (and every later command) from **Git Bash**, not PowerShell or cmd — they can't source a `.sh` file. Easiest: open the project in VS Code and set the integrated terminal to Git Bash (`Ctrl+Shift+P` → *Terminal: Select Default Profile* → *Git Bash*). No Git Bash? Install [Git for Windows](https://git-scm.com/download/win), or use [WSL](https://learn.microsoft.com/windows/wsl/install) (behaves like native Linux). Started in PowerShell by mistake? Run `.\setup.ps1` from the lab folder and it'll point you to Git Bash. macOS/Linux: nothing special — the commands below work as-is.

### 3a. First run: seed `.env`

Move into the lab's `code/` folder and source the setup script from there. You'll stay in `code/` for the rest of the lab — it's where you run every exercise — so `cd` in now:

```bash
cd code        # from the root of the cloned repo
source setup.sh
```

On the first run (no `.env` exists yet) the script copies `.env.example` into place and stops with an "ACTION REQUIRED" message. That's expected — you haven't filled in your key yet.

### 3b. Fill in your Bedrock API key

Open the `.env` file the script just created in your editor. The path is printed in the script output (look for `→ Env root:`). Set:

```env
AWS_BEARER_TOKEN_BEDROCK=bedrock-api-key-...   # from Step 2
AWS_REGION=us-east-1                           # broadest Bedrock model availability
```

Do **not** put the Bedrock API key in `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`. Those are a different credential type; if leftover placeholders remain in `.env`, delete those two lines.

### 3c. Confirm — or update — the model ID

`.env.example` ships with `BEDROCK_MODEL_ID` set to **Amazon Nova 2 Lite** (`us.amazon.nova-2-lite-v1:0`), which is the course default. For most students this is fine and you can skip to 3d. You need to touch this line only if:

- you want to use a different model, **or**
- Amazon has shipped a newer Nova version since this lab was written and you want the latest.

To pick a current ID:

1. Open the Bedrock console: https://console.aws.amazon.com/bedrock/
2. Region selector (top-right) → match the value of `AWS_REGION` in your `.env`.
3. Left sidebar under **Discover** → **Model catalog** → filter by provider **Amazon**.
4. Click into the model you want → copy its **Model ID** from the detail page → paste it as `BEDROCK_MODEL_ID` in `.env`. Use the **cross-region inference-profile** ID (the `us.` one — e.g. `us.amazon.nova-2-lite-v1:0`), not the bare `amazon...` ID: Nova 2 Lite can't be called in-region on-demand in us-east-1, so the profile prefix is required.

> **Enable model access.** Before the first call, the model must be enabled for your account under **Model access** in the Bedrock console. Amazon's own models (Nova) are first-party and usually don't require the use-case form some third-party models do, but you may still need to toggle access on. If 3d below fails with an `AccessDeniedException` about model access, open **Model access**, enable **Amazon Nova 2 Lite**, wait a moment, then re-run the script.

### 3d. Second run: verify Bedrock works

Source the script again (you're already in `code/`):

```bash
source setup.sh
```

This time it runs the full check. On success the last lines are:

```
✓ Bedrock OK — model replied: 'ok'
✓ Lesson-02-API-Endpoints is ready. Run an exercise with:  python <exercise>.py
```

### If you see an error

The setup script prints a concrete action for every failure mode. The most common ones:

- **`AccessDeniedException: ... API Key is valid`** — Bedrock rejected the key itself. Usual causes: (a) `AWS_REGION` doesn't match the region where a **short-term** key was generated, (b) the key expired/was deactivated, or (c) the pasted value was truncated. Prefer a **long-term** key for the course.
- **`AccessDeniedException`** (other wording) — the key authenticated but the call was refused. Two common causes: (a) the key's IAM principal lacks `bedrock:InvokeModel` / `bedrock:CallWithBearerToken`, or (b) model access for Nova 2 Lite isn't enabled — re-read the **Model access** note in 3c.
- **`UnrecognizedClientException` / `InvalidSignatureException`** — `AWS_BEARER_TOKEN_BEDROCK` is wrong, expired, or still a placeholder; or leftover `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` placeholders are confusing auth. Re-check Step 2 and delete any access-key lines from `.env`.
- **`ResourceNotFoundException`** — the `BEDROCK_MODEL_ID` value isn't valid in your region. The most common cause is forgetting the `us.` inference-profile prefix (Nova 2 Lite needs it — the bare `amazon...` ID isn't on-demand callable in-region). Re-do 3c.
- **`EndpointConnectionError`** — `AWS_REGION` isn't a Bedrock-supported region. Try `us-east-1` or `us-west-2`.

If the error you're seeing isn't in that list — or the suggested action doesn't fix it — see [Getting help when setup fails](#getting-help-when-setup-fails) below.

Once `setup.sh` succeeds, you're ready for the exercises — every one of them uses only Bedrock (`AWS_BEARER_TOKEN_BEDROCK`, `AWS_REGION`, `BEDROCK_MODEL_ID`).

---

## Getting help when setup fails

AWS console UIs change, regions differ, and error messages come in many flavors. When you're stuck, the quality of Claude's answer depends almost entirely on the quality of what you paste. Include the same five pieces every time:

1. **Where you are.** Which step — "Step 3c, picking the model ID from the catalog."
2. **What you did.** The specific action that triggered the problem.
3. **What you expected vs. what happened.**
4. **Evidence.** The **exact** error text (copy-paste, not paraphrase), or a screenshot — both is better.
5. **Environment.** Region, model ID, and relevant `.env` values — **with secrets redacted.**

**Redact secrets.** Never paste Bedrock API keys in clear text — not in chat, not in a screenshot. Show a short prefix only:

```
AWS_BEARER_TOKEN_BEDROCK=bedrock-api-key-...REDACTED
```

If a screenshot accidentally exposes a key, **deactivate or delete it immediately** (Bedrock console → API keys → Actions → Deactivate / Delete) and generate a new one, then update `.env`.

### A good error-report prompt looks like this

```
I'm at Step 3d (verifying with setup.sh). I ran
`source setup.sh` and got:

  ✗ Bedrock returned [AccessDeniedException]: User: arn:aws:iam::123456789012:user/...
    is not authorized to perform: bedrock:InvokeModel

My .env has AWS_REGION=us-east-1 and
BEDROCK_MODEL_ID=us.amazon.nova-2-lite-v1:0 (API key redacted).
The account is brand new and I have not yet enabled model access
for Nova 2 Lite (Step 3c).

What's the most likely cause?
```

That lets Claude rule out 80% of failure modes immediately and zero in on the real one (here, model access). Compare it to "it doesn't work" — which forces three follow-up questions before any help is possible.

### When you don't know what to ask

The structured form still works:

```
Where I am:      Step [N] of the AWS Bedrock setup.
What I did:      [exact actions]
What I expected: [expected outcome]
What happened:   [actual outcome, exact words from console / terminal]
Evidence:        [paste the full error block, OR attach a screenshot, OR both]
Environment:     region=[...], model_id=[...], .env values, secrets redacted.

What's the most likely cause, and what's the next thing to check?
```

The same pattern works for every later lab in this course — and most of your real work after it.
