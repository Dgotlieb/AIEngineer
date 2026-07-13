import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_REGION"))
model_id = "amazon.nova-pro-v1:0"

with open("../data/call1.txt", "r") as f:
    transcript = f.read()

system_prompt = "You are a customer success data extractor."
user_prompt = f"Analyze the following transcript and return a JSON with 'sentiment', 'churn_risk', and 'key_action':\n\n{transcript}"

response = client.converse(
    modelId=model_id,
    messages=[{"role": "user", "content": [{"text": user_prompt}]}],
    system=[{"text": system_prompt}]
)

print(json.dumps(response['output']['message']['content'], indent=2))
print("Usage:", response['usage'])
