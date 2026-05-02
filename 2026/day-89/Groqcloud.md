# KubeHealer — Modified for Free (Groq Instead of Claude)

> ⚠️ This is a modified version of the original KubeHealer repo.
> The original uses Claude (Anthropic paid API).
> This version uses **Groq free API** (llama-3.1-8b-instant) — completely free, no credit card needed.

---

## What is KubeHealer?
A production-grade AI agent that:
- 🔍 Scans Kubernetes cluster for broken pods
- 🧠 Diagnoses root cause using LLM (Groq/llama-3.1-8b-instant)
- 🔧 Fixes broken pods automatically
- ⚠️ Escalates unfixable issues to humans
- 🔄 Crash recovery via Temporal durable execution

---

## Free Services Used
| Service | Purpose | Link |
|---------|---------|------|
| Groq API | Free LLM (replaces Claude) | https://console.groq.com |
| Temporal | Durable workflow execution | Runs locally |
| Minikube | Local Kubernetes cluster | Runs locally |

---

## Prerequisites
- Docker installed and running
- Python 3.10+
- WSL (Ubuntu 24.04) if on Windows
- Minikube installed
- Temporal CLI installed

---

## Step 1 — Get Free Groq API Key
1. Go to https://console.groq.com
2. Sign in with Google (free, no credit card)
3. Click **API Keys** → **Create API key**
4. Copy the key — you'll need it later

---

## Step 2 — Clone the Repo
```bash
cd /mnt/d/
git clone https://github.com/TrainWithShubham/kubehealer.git
cd kubehealer
```

---

## Step 3 — Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install groq
```

---

## Step 4 — Modify Files (Replace Claude with Groq)

### 4a — Replace activities/llm_activities.py
```bash
cat > activities/llm_activities.py << 'EOF'
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
EOF
```

### 4b — Replace activities/chat_activities.py
```bash
cat > activities/chat_activities.py << 'EOF'
import json
from groq import Groq
from kubernetes import client, config
from temporalio import activity
from temporalio.exceptions import ApplicationError
from models import ClaudeRequest, ClaudeResponse

def _init_k8s():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        try:
            config.load_kube_config()
        except config.ConfigException:
            raise RuntimeError("No Kubernetes cluster found.")
    return client.CoreV1Api()

v1 = _init_k8s()

@activity.defn
async def call_claude(request: ClaudeRequest) -> ClaudeResponse:
    activity.logger.info(f"Calling Groq ({len(request.messages)} messages)")
    groq_client = Groq()
    messages = [{"role": "system", "content": request.system_prompt}] + request.messages
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=4096,
            messages=messages,
        )
    except Exception as e:
        raise ApplicationError(f"Groq API error: {e}")

    content = response.choices[0].message.content
    content_dicts = [{"type": "text", "text": content}]
    return ClaudeResponse(stop_reason="end_turn", content=content_dicts)

@activity.defn
async def list_pods_activity(namespace: str) -> str:
    activity.logger.info(f"Listing pods in namespace '{namespace}'")
    pods = v1.list_namespaced_pod(namespace=namespace)
    lines = [f"{'NAME':<50} {'STATUS':<25} {'READY':<8} {'RESTARTS'}"]
    lines.append("-" * 95)
    for pod in pods.items:
        name = pod.metadata.name
        phase = pod.status.phase or "Unknown"
        ready = "0/0"
        restarts = 0
        if pod.status.container_statuses:
            total = len(pod.status.container_statuses)
            ready_count = sum(1 for cs in pod.status.container_statuses if cs.ready)
            ready = f"{ready_count}/{total}"
            restarts = sum(cs.restart_count for cs in pod.status.container_statuses)
            for cs in pod.status.container_statuses:
                if cs.state and cs.state.waiting and cs.state.waiting.reason:
                    phase = cs.state.waiting.reason
                    break
        lines.append(f"{name:<50} {phase:<25} {ready:<8} {restarts}")
    return "\n".join(lines)

@activity.defn
async def get_pod_details_activity(pod_name: str, namespace: str) -> str:
    activity.logger.info(f"Getting details for pod '{pod_name}'")
    pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
    lines = [f"Pod: {pod_name}", f"Namespace: {namespace}", f"Phase: {pod.status.phase}"]
    if pod.status.container_statuses:
        for cs in pod.status.container_statuses:
            lines.append(f"\nContainer: {cs.name}")
            lines.append(f"  Image: {cs.image}")
            lines.append(f"  Ready: {cs.ready}")
            lines.append(f"  Restart Count: {cs.restart_count}")
            if cs.state:
                if cs.state.waiting:
                    lines.append(f"  State: Waiting — {cs.state.waiting.reason}")
                elif cs.state.terminated:
                    lines.append(f"  State: Terminated — {cs.state.terminated.reason}")
                elif cs.state.running:
                    lines.append("  State: Running")
    return "\n".join(lines)

@activity.defn
async def get_pod_logs_activity(pod_name: str, namespace: str, tail_lines: int) -> str:
    activity.logger.info(f"Getting logs for pod '{pod_name}'")
    try:
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, tail_lines=tail_lines)
        return logs if logs else "(no log output)"
    except Exception as e:
        return f"Could not get logs: {e}"

@activity.defn
async def get_pod_events_activity(pod_name: str, namespace: str) -> str:
    activity.logger.info(f"Getting events for pod '{pod_name}'")
    events = v1.list_namespaced_event(
        namespace=namespace,
        field_selector=f"involvedObject.name={pod_name},involvedObject.kind=Pod",
    )
    if not events.items:
        return f"No events found for pod '{pod_name}'."
    lines = []
    for event in events.items[-15:]:
        lines.append(f"[{event.type:<8}] {event.reason:<25} {event.message}")
    return "\n".join(lines)
EOF
```

### 4c — Fix worker.py (replace Anthropic check with Groq)
```bash
sed -i 's/ANTHROPIC_API_KEY/GROQ_API_KEY/g' worker.py
sed -i 's/Anthropic API key/Groq API key/g' worker.py
```

---

## Step 5 — Install Temporal CLI
```bash
curl -sSf https://temporal.download/cli.sh | sh
export PATH=$PATH:$HOME/.temporalite/bin
echo 'export PATH=$PATH:$HOME/.temporalite/bin' >> ~/.bashrc
```

---

## Step 6 — Start Minikube
```bash
minikube start --memory=1800mb --cpus=2 --driver=docker
```

---

## Step 7 — Deploy 3 Broken Apps (as Deployments NOT bare pods)
```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web
        image: ngnix:latest
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memory-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: memory-app
  template:
    metadata:
      labels:
        app: memory-app
    spec:
      containers:
      - name: app
        image: nginx:alpine
        resources:
          limits:
            memory: "1Mi"
        command: ["sh", "-c", "echo starting && sleep 3600"]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: config-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: config-app
  template:
    metadata:
      labels:
        app: config-app
    spec:
      containers:
      - name: app
        image: nginx:alpine
        envFrom:
        - configMapRef:
            name: app-config
EOF
```

---

## Step 8 — Set Groq API Key
```bash
export GROQ_API_KEY="your-groq-key-here"
echo 'export GROQ_API_KEY="your-groq-key-here"' >> ~/.bashrc
```

---

## Step 9 — Start Everything (3 terminals needed)

### Terminal 1 — Start Temporal
```bash
temporal server start-dev
```

### Terminal 2 — Start Worker
```bash
cd /mnt/d/kubehealer
source .venv/bin/activate
export GROQ_API_KEY="your-groq-key-here"
python3 worker.py
```

### Terminal 3 — Trigger Healing
```bash
cd /mnt/d/kubehealer
source .venv/bin/activate
export GROQ_API_KEY="your-groq-key-here"
python3 starter.py
```

---

## Step 10 — Watch Results
```bash
kubectl get pods
# web-app    → Running ✅ (fixed image typo)
# memory-app → Running ✅ (fixed memory limit)
# config-app → Still broken ⚠️ (needs manual ConfigMap)
```

View Temporal UI: http://localhost:8233

---

## Step 11 — Fix config-app Manually
```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  APP_ENV: "production"
  APP_PORT: "8080"
  APP_NAME: "my-app"
EOF
```

---

## Step 12 — Cleanup
```bash
minikube delete
# Stop Temporal with Ctrl+C
deactivate
```

---

## What Changed from Original
| Original | This Version |
|----------|-------------|
| Claude Sonnet (paid) | Groq llama-3.1-8b-instant (free) |
| `import anthropic` | `from groq import Groq` |
| `ANTHROPIC_API_KEY` | `GROQ_API_KEY` |
| Kind cluster | Minikube (more stable on low RAM) |
| Bare pods | Deployments (required by execute_fix) |

---

## Key Learnings
- Production agents need guardrails — approval, scope limits, audit trail
- Temporal prevents lost state during infrastructure changes
- Good agents know their limits (config-app escalation)
- Groq free API is a great Claude replacement for learning
- Use Deployments not bare Pods — KubeHealer patches Deployments
