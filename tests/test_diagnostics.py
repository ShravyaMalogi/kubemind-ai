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


from ai_engine.analyzer import analyze_pod


def test_ai_fallback_without_token(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)

    pod = {
        "name": "broken-pod",
        "namespace": "default",
        "status": "Pending",
        "reason": "ImagePullBackOff",
        "restart_count": 0,
        "images": ["missing-image:v1"],
        "node": "worker-1"
    }

    result = analyze_pod(pod)

    assert result["source"] == "Rule-based fallback"
    assert result["analysis"]["issue"] == "Image Pull Failure"


def test_ai_fallback_detects_crash(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)

    pod = {
        "name": "crash-pod",
        "status": "Running",
        "reason": "CrashLoopBackOff",
        "restart_count": 5
    }

    result = analyze_pod(pod)

    assert result["source"] == "Rule-based fallback"
    assert result["analysis"]["issue"] == "Container Crash"
