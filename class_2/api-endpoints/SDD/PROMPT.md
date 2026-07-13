# Architecture Blueprint: 06-prompt-template.py

**Objective:** Construct a Python script utilizing the boto3 Converse API to process a customer service transcript.

**Requirements:**
1. Initialize a boto3 Bedrock client using standard environment variables.
2. Target the `amazon.nova-pro-v1:0` model.
3. Read the contents of `data/call1.txt`.
4. Construct a system prompt establishing the AI as a customer success data extractor.
5. Construct a user prompt demanding a JSON payload containing:
   - `sentiment` (positive, neutral, negative)
   - `churn_risk` (high, medium, low)
   - `key_action` (string)
6. Execute the API call.
7. Print the extracted JSON and the token usage block.

**Constraints:**
- Do not utilize IAM profile logic. Rely natively on the environment variables.
- Maintain strict separation of system instructions and user data.
