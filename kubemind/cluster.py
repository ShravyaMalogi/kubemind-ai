
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


def connect_to_cluster():
    """Connect using the available Kubernetes configuration."""
    try:
        config.load_incluster_config()
    except ConfigException:
        try:
            config.load_kube_config()
        except ConfigException as error:
            raise RuntimeError(
                "No Kubernetes configuration found. "
                "Configure a cluster before using live monitoring."
            ) from error

    return client.CoreV1Api()


def summarize_pod(pod):
    """Convert Kubernetes pod data into a simple diagnostic record."""
    metadata = pod.get("metadata") or {}
    status_data = pod.get("status") or {}
    spec = pod.get("spec") or {}

    container_statuses = status_data.get("container_statuses") or []

    restart_count = sum(
        container.get("restart_count", 0)
        for container in container_statuses
    )

    images = [
        container.get("image")
        for container in (spec.get("containers") or [])
    ]

    reason = None

    for container in container_statuses:
        state = container.get("state") or {}
        waiting = state.get("waiting") or {}

        if waiting.get("reason"):
            reason = waiting["reason"]
            break

    return {
        "name": metadata.get("name", "unknown"),
        "namespace": metadata.get("namespace", "default"),
        "status": status_data.get("phase", "Unknown"),
        "reason": reason,
        "restart_count": restart_count,
        "images": images,
        "node": spec.get("node_name")
    }


def get_cluster_pods():
    """Retrieve pods from all accessible namespaces."""
    api = connect_to_cluster()

    pods = api.list_pod_for_all_namespaces()

    return [
        summarize_pod(pod.to_dict())
        for pod in pods.items
    ]
