
from kubemind.cluster import summarize_pod


def test_summarize_pod():
    pod = {
        "metadata": {
            "name": "echo-web",
            "namespace": "default"
        },
        "status": {
            "phase": "Running",
            "container_statuses": [
                {
                    "restart_count": 2,
                    "state": {
                        "waiting": None
                    }
                }
            ]
        },
        "spec": {
            "containers": [
                {"image": "nginx:latest"}
            ],
            "node_name": "worker-1"
        }
    }

    result = summarize_pod(pod)

    assert result["name"] == "echo-web"
    assert result["namespace"] == "default"
    assert result["status"] == "Running"
    assert result["restart_count"] == 2
    assert result["images"] == ["nginx:latest"]
    assert result["node"] == "worker-1"


def test_detect_image_pull_failure():
    pod = {
        "metadata": {"name": "broken-pod"},
        "status": {
            "phase": "Pending",
            "container_statuses": [
                {
                    "restart_count": 0,
                    "state": {
                        "waiting": {
                            "reason": "ImagePullBackOff"
                        }
                    }
                }
            ]
        },
        "spec": {"containers": []}
    }

    result = summarize_pod(pod)

    assert result["reason"] == "ImagePullBackOff"
