
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from kubernetes import client, config

app = FastAPI(
    title="NEXUS API",
    description="Kubernetes Pod Placement Monitoring API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "application": "NEXUS",
        "status": "Running",
        "message": "Kubernetes Pod Placement Monitor API"
    }


@app.get("/api/health")
def health():
    return {
        "service": "Backend",
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/info")
def application_info():
    return {
        "application": "NEXUS",
        "platform": "Kubernetes",
        "namespace": "pod-placement",
        "frontend": "HTML, CSS, JavaScript",
        "backend": "Python FastAPI",
        "scheduling": [
            "Pod Affinity",
            "Preferred Pod Anti-Affinity",
            "Required Pod Anti-Affinity"
        ]
    }


@app.get("/api/pods")
def get_pods():
    try:
        config.load_kube_config()

        v1 = client.CoreV1Api()

        pods = v1.list_namespaced_pod(
            namespace="pod-placement"
        )

        result = []

        for pod in pods.items:
            result.append({
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "node": pod.spec.node_name or "Not Scheduled",
                "ip": pod.status.pod_ip or "Not Assigned",
                "labels": pod.metadata.labels or {}
            })

        return {
            "namespace": "pod-placement",
            "total_pods": len(result),
            "pods": result
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Unable to retrieve Kubernetes Pods"
        }
