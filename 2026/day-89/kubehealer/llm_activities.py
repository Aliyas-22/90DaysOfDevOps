
import json
import re
from groq import Groq
from temporalio import activity
from temporalio.exceptions import ApplicationError
from models import Diagnosis

SYSTEM_PROMPT = """You are a Kubernetes SRE expert. You receive pod diagnostic info and must identify the root cause and suggest a fix.

Respond ONLY with valid JSON, no markdown, no explanation outside the JSON:
{
  "pod_name": "the pod name from the input",
  "root_cause": "brief root cause",
  "severity": "low or medium or high",
  "action": "one of: restart_pod, fix_image, patch_resources, skip",
  "explanation": "one sentence a human would understand",
  "fix_details": {}
}

Rules for fix_details:
- If action is "fix_image": include {"image": "corrected-image:tag"}
- If action is "patch_resources": include {"memory": "128Mi"} or appropriate limit
- If action is "restart_pod" or "skip": empty {}

Common patterns:
- "ngnix" is a typo for "nginx"
- OOMKilled means memory limit is too low, suggest 128Mi or 256Mi
- Missing ConfigMap cannot be auto-fixed, use action "skip"
"""

VALID_ACTIONS = {"restart_pod", "fix_image", "patch_resources", "skip"}

def _parse_json_response(text: str) -> dict:
    cleaned = re.sub(r"```(?:json|JSON)?\s*", "", text)
    cleaned = re.sub(r"```\s*$", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()
    return json.loads(cleaned)

@activity.defn
async def diagnose_pod(pod_details: str) -> Diagnosis:
    activity.logger.info("Asking Groq to diagnose pod")
    client = Groq()
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": pod_details}
            ],
        )
    except Exception as e:
        raise ApplicationError(f"Groq API error: {e}")

    raw_text = response.choices[0].message.content
    if not raw_text:
        raise ApplicationError("Groq returned empty response")

    try:
        data = _parse_json_response(raw_text)
    except (json.JSONDecodeError, ValueError) as e:
        raise ApplicationError(f"Failed to parse Groq diagnosis JSON: {e}")

    action = data.get("action", "skip")
    if action not in VALID_ACTIONS:
        action = "skip"

    diagnosis = Diagnosis(
        pod_name=data["pod_name"],
        root_cause=data["root_cause"],
        severity=data["severity"],
        action=action,
        explanation=data["explanation"],
        fix_details=data.get("fix_details", {}),
    )
    activity.logger.info(f"Diagnosis: [{diagnosis.severity.upper()}] {diagnosis.root_cause}")
    return diagnosis
