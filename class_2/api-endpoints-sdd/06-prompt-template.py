"""Interactive call-summary tool — prompt assembled as code from menus.

Why menus instead of free text: a known set of inputs → predictable prompts →
predictable output. Free text lets the user ask for anything; constrained
choices only produce prompts we've already designed (the input-side cousin of
structured output in Lesson 3).

Static vs dynamic:
  - SYSTEM_PROMPT stays fixed (role/rules only — never the menu picks).
  - build_request_prompt() splices the chosen fragments + transcript into the
    user message.
"""

import os
import sys
from pathlib import Path

import boto3
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TRANSCRIPT_PATH = Path(__file__).resolve().parent / "data" / "call1.txt"

SYSTEM_PROMPT = (
    "You are a support-call analyst. Deliver exactly what the user asks for "
    "in the requested focus, format, and length. Use only facts supported by "
    "the transcript — do not invent details."
)

# Each option: short label shown in the menu → instruction fragment spliced
# into the user prompt. Adding an option is a one-liner; the prompt space stays known.
FOCUSES = {
    "billing": "Lead with billing: premium change, fees, and payment issues.",
    "retention": "Lead with retention: churn risk and what kept (or could keep) the customer.",
    "claim": "Lead with the open claim: status and the next steps that were promised.",
}

FORMATS = {
    "customer email": "Format as a short, warm email to the customer (greeting and sign-off).",
    "manager email": "Format as an internal email to the manager — status and risk first, no customer pleasantries.",
    "CRM note": "Format as a terse CRM note: no greeting or sign-off, compact factual bullets only.",
}

LENGTHS = {
    "concise": "Length: 1-2 sentences.",
    "short": "Length: 3-4 sentences.",
    "medium": "Length: one short paragraph (about 5-7 sentences).",
}


def choose(label: str, options: dict) -> str:
    """Numbered menu; reject out-of-range / non-numeric input and re-ask.

    Also accepts the option label (case-insensitive) so operators can type
    a name instead of a number — still constrained to the known set.
    """
    keys = list(options)
    print(f"\nSupport-call Agent: choose a {label} —")
    for i, key in enumerate(keys, 1):
        print(f"  {i}) {key}  — e.g. {options[key]}")

    by_label = {k.lower(): k for k in keys}
    while True:
        raw = input("You: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(keys):
            return keys[int(raw) - 1]
        if raw.lower() in by_label:
            return by_label[raw.lower()]
        print(f"  (enter a number 1-{len(keys)}, or an option name)")


def build_request_prompt(transcript: str, focus: str, fmt: str, length: str) -> str:
    """Assemble the dynamic user prompt from constrained choices + transcript.

    Constraining input → predictable prompt → predictable output. Pure function
    (no I/O) so each choice can be checked without a model call. Menu selections
    land here; the system prompt stays static and choice-free.
    """
    return (
        "Summarize this support call to these specs:\n"
        f"- {FOCUSES[focus]}\n"
        f"- {FORMATS[fmt]}\n"
        f"- {LENGTHS[length]}\n\n"
        f"Transcript:\n{transcript}"
    )


def call_bedrock(user_prompt: str, model_id: str, region: str) -> str:
    """Single Bedrock Converse call — swap providers by replacing this function."""
    client = boto3.client("bedrock-runtime", region_name=region)
    response = client.converse(
        modelId=model_id,
        system=[{"text": SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": user_prompt}]}],
        inferenceConfig={"maxTokens": 600, "temperature": 0.3},
    )
    return response["output"]["message"]["content"][0]["text"]


def main() -> None:
    model_id = os.environ.get("BEDROCK_MODEL_ID")
    region = os.environ.get("AWS_REGION", "us-east-1")
    if not model_id:
        print(
            "Error: BEDROCK_MODEL_ID is not set. Copy .env.example to .env "
            "(or run setup.sh) and set the model ID.",
            file=sys.stderr,
        )
        sys.exit(1)

    transcript = TRANSCRIPT_PATH.read_text(encoding="utf-8").strip()

    focus = choose("focus", FOCUSES)
    fmt = choose("format", FORMATS)
    length = choose("length", LENGTHS)

    user_prompt = build_request_prompt(transcript, focus, fmt, length)
    print("\nSupport-call Agent: here's what you asked for:\n")
    print(call_bedrock(user_prompt, model_id=model_id, region=region))


if __name__ == "__main__":
    main()
