
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from kubemind.diagnostics import diagnose_pod
from ai_engine.analyzer import analyze_pod

st.set_page_config(
    page_title="KubeMind | Kubernetes AI Monitor",
    page_icon="☸️",
    layout="wide"
)

st.title("☸️ KubeMind")
st.subheader("AI-Powered Kubernetes Troubleshooting Assistant")

st.markdown("Monitor Kubernetes workloads and identify potential problems.")

# Sample cluster data for the dashboard
pods = [
    {
        "name": "frontend-app",
        "namespace": "default",
        "status": "Running",
        "reason": None,
        "restart_count": 0,
        "images": ["nginx:latest"],
        "node": "worker-1"
    },
    {
        "name": "payment-service",
        "namespace": "default",
        "status": "Running",
        "reason": "CrashLoopBackOff",
        "restart_count": 5,
        "images": ["payment:v1"],
        "node": "worker-2"
    },
    {
        "name": "database",
        "namespace": "default",
        "status": "Pending",
        "reason": "ImagePullBackOff",
        "restart_count": 0,
        "images": ["database:v2"],
        "node": "worker-1"
    }
]

# Summary metrics
total_pods = len(pods)
healthy_pods = sum(
    1 for pod in pods
    if diagnose_pod(
        pod["status"], pod["restart_count"], pod["reason"]
    )["issue"] == "Healthy"
)
problem_pods = total_pods - healthy_pods
total_restarts = sum(pod["restart_count"] for pod in pods)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pods", total_pods)
col2.metric("Healthy Pods", healthy_pods)
col3.metric("Pods with Issues", problem_pods)
col4.metric("Total Restarts", total_restarts)

st.divider()

st.subheader("Pod Monitoring")

pod_table = []

for pod in pods:
    diagnosis = diagnose_pod(
        pod["status"],
        pod["restart_count"],
        pod["reason"]
    )

    pod_table.append({
        "Pod Name": pod["name"],
        "Namespace": pod["namespace"],
        "Status": pod["status"],
        "Issue": diagnosis["issue"],
        "Severity": diagnosis["severity"],
        "Restarts": pod["restart_count"]
    })

st.dataframe(
    pd.DataFrame(pod_table),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("AI Troubleshooting")

selected_pod_name = st.selectbox(
    "Select a pod to investigate",
    [pod["name"] for pod in pods]
)

if st.button("Analyze with KubeMind AI"):
    selected_pod = next(
        pod for pod in pods
        if pod["name"] == selected_pod_name
    )

    with st.spinner("Analyzing pod..."):
        result = analyze_pod(selected_pod)

    st.caption(f"Analysis source: {result['source']}")

    if "warning" in result:
        st.warning(f"AI unavailable: {result['warning']}")

    if isinstance(result["analysis"], dict):
        st.write("**Problem:**", result["analysis"]["issue"])
        st.write("**Severity:**", result["analysis"]["severity"])
        st.write("**Likely cause:**", result["analysis"]["cause"])
        st.write("**Suggested solution:**", result["analysis"]["solution"])
    else:
        st.markdown(result["analysis"])

st.caption("KubeMind prototype | Sample data — not connected to a live cluster yet.")
