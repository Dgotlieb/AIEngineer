# Validation Target: 06-prompt-template.py

**Execution Parameters:**
- Path: `../../api-endpoints-sdd/06-prompt-template.py`

**Validation Criteria:**
1. **Client Initialization Check:** Verify `boto3.client('bedrock-runtime')` is present.
2. **Model Selection Check:** Verify `modelId` targets `amazon.nova-pro-v1:0`.
3. **Execution Check:** Execute the script. Verify standard output contains a valid JSON block with `sentiment`, `churn_risk`, and `key_action` keys.
4. **Token Visibility Check:** Verify standard output contains the `usage` block.

**Scoring:**
- 25 points per successful criteria.
- 100 points required to pass.
