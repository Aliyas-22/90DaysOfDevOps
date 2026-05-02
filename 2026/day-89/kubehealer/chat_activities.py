
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
