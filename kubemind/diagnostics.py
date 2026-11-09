def diagnose_pod(status, restart_count=0, reason=None):
    if reason == "ImagePullBackOff":
        return {
            "issue": "Image Pull Failure",
            "severity": "High",
            "cause": "Kubernetes cannot pull the container image.",
            "solution": "Check image name, tag and registry credentials."
        }

    if reason == "CrashLoopBackOff":
        return {
            "issue": "Container Crash",
            "severity": "High",
            "cause": "The container repeatedly exits after starting.",
            "solution": "Inspect application logs and container configuration."
        }

    if status == "Pending":
        return {
            "issue": "Pod Pending",
            "severity": "Medium",
            "cause": "The pod has not been scheduled or started.",
            "solution": "Check node resources and pod scheduling events."
        }

    if status == "Running" and restart_count > 0:
        return {
            "issue": "Container Restart Detected",
            "severity": "Medium",
            "cause": f"The container has restarted {restart_count} times.",
            "solution": "Inspect previous container logs."
        }

    if status == "Running":
        return {
            "issue": "Healthy",
            "severity": "Low",
            "cause": "The pod is running normally.",
            "solution": "No action required."
        }

    return {
        "issue": "Unknown Status",
        "severity": "Medium",
        "cause": "Unable to identify the problem automatically.",
        "solution": "Inspect pod description and Kubernetes events."
    }