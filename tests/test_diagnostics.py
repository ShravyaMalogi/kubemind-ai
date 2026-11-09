from kubemind.diagnostics import diagnose_pod


def test_crash_loop():
    result = diagnose_pod("Running", reason="CrashLoopBackOff")
    assert result["issue"] == "Container Crash"


def test_image_pull():
    result = diagnose_pod("Pending", reason="ImagePullBackOff")
    assert result["issue"] == "Image Pull Failure"


def test_healthy_pod():
    result = diagnose_pod("Running")
    assert result["issue"] == "Healthy"