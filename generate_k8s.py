import os
import sys

def create_directory(path):
    """Create a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)

def generate_helm_chart(app_name, repo_path):
    """Generate a Helm chart for the application."""
    helm_path = os.path.join(repo_path, "charts", app_name)
    create_directory(helm_path)
    create_directory(os.path.join(helm_path, "templates"))

    chart_yaml = f"""\
apiVersion: v2
name: {app_name}
description: A Helm chart for {app_name}
type: application
version: 0.1.0
appVersion: "1.0"
"""
    values_yaml = f"""\
replicaCount: 1

image:
  repository: {app_name}
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080
"""
    deployment_yaml = f"""\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: {{ {{ .Values.replicaCount }} }}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: "{{ {{ .Values.image.repository }} }}:{{ {{ .Values.image.tag }} }}"
        ports:
        - containerPort: 8080
"""

    with open(os.path.join(helm_path, "Chart.yaml"), "w") as f:
        f.write(chart_yaml)
    with open(os.path.join(helm_path, "values.yaml"), "w") as f:
        f.write(values_yaml)
    with open(os.path.join(helm_path, "templates", "deployment.yaml"), "w") as f:
        f.write(deployment_yaml)

def generate_kubernetes_manifests(app_name, repo_path):
    """Generate Kubernetes deployment YAMLs."""
    k8s_path = os.path.join(repo_path, "k8s", app_name)
    create_directory(k8s_path)

    deployment_yaml = f"""\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {app_name}:latest
        ports:
        - containerPort: 8080
"""

    service_yaml = f"""\
apiVersion: v1
kind: Service
metadata:
  name: {app_name}
spec:
  selector:
    app: {app_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
"""

    with open(os.path.join(k8s_path, "deployment.yaml"), "w") as f:
        f.write(deployment_yaml)
    with open(os.path.join(k8s_path, "service.yaml"), "w") as f:
        f.write(service_yaml)

def generate_argocd_manifests(app_name, repo_path):
    """Generate ArgoCD application manifests."""
    argocd_path = os.path.join(repo_path, "argocd", app_name)
    create_directory(argocd_path)

    application_yaml = f"""\
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {app_name}
  namespace: argocd
spec:
  destination:
    namespace: default
    server: https://kubernetes.default.svc
  source:
    repoURL: https://github.com/my-org/{app_name}.git
    path: charts/{app_name}
    targetRevision: main
    helm:
      valueFiles:
        - values.yaml
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
"""

    with open(os.path.join(argocd_path, "application.yaml"), "w") as f:
        f.write(application_yaml)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_k8s.py <app-name>")
        sys.exit(1)

    app_name = sys.argv[1]
    repo_path = os.getcwd()

    generate_helm_chart(app_name, repo_path)
    generate_kubernetes_manifests(app_name, repo_path)
    generate_argocd_manifests(app_name, repo_path)

    print(f"✅ All Kubernetes, Helm, and ArgoCD files created for {app_name}.")
    print("Modify the generated files before deploying.")
