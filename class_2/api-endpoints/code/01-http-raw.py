"""Exercise 01 — An LLM API endpoint is just an HTTP POST.

Hit Bedrock's Converse endpoint with plain `requests`: URL, headers, JSON body.
Auth is a Bearer token (`AWS_BEARER_TOKEN_BEDROCK`) — the same key boto3 uses
in exercise 02. Diff this file against 02 to see what the SDK takes over
(client construction, retries, parsing the response into a dict).
"""

import os

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

region = os.environ["AWS_REGION"]
model_id = os.environ["BEDROCK_MODEL_ID"]
url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/converse"

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {os.environ['AWS_BEARER_TOKEN_BEDROCK']}",
        "Content-Type": "application/json",
    },
    json={
        "messages": [
            {"role": "user", "content": [{"text": "What is 2+2? Reply in one sentence."}]}
        ]
    },
)
response.raise_for_status()

print(response.json()["output"]["message"]["content"][0]["text"])
