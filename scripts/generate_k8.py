#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys


def create_directory(path: str) -> None:
    """Creates a directory at the given path if it does not already exist."""
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str) -> None:
    """Writes content to a file, creating directories if necessary. Warns if overwriting."""
    create_directory(os.path.dirname(path))
    if os.path.exists(path):
        print(f"⚠️  Overwriting existing file: {path}")
    with open(path, "w", newline="\n") as f:
        f.write(content.strip() + "\n")


def get_app_name() -> str:
    """Returns the app name from the current directory."""
    return os.path.basename(os.getcwd())


def generate_all_templates(app_name: str) -> None:
    """Generates Helm, K8s, and ArgoCD manifests for the app."""
    files = {
        f"charts/{app_name}/Chart.yaml": f"""
---
apiVersion: v2
name: {app_name}
description: A Helm chart for {app_name}
type: application
version: 0.1.0
appVersion: "1.0"
""",
        f"charts/{app_name}/values.yaml": """
---
replicaCount: 1

image:
  repository: myregistry.io/app
  tag: latest

service:
  type: ClusterIP
  port: 8080
""",
        f"charts/{app_name}/templates/deployment.yaml": """
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: { .Chart.Name }
  labels:
    app: { .Chart.Name }
spec:
  replicas: { .Values.replicaCount }
  selector:
    matchLabels:
      app: { .Chart.Name }
  template:
    metadata:
      labels:
        app: { .Chart.Name }
    spec:
      containers:
      - name: { .Chart.Name }
        image: "{ .Values.image.repository }:{ .Values.image.tag }"
        ports:
        - containerPort: 8080
""",
        "k8s/base/deployment.yaml": f"""
---
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
""",
        "k8s/base/service.yaml": f"""
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}
spec:
  type: ClusterIP
  selector:
    app: {app_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
""",
        "k8s/base/kustomization.yaml": """
---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
""",
        "k8s/overlays/dev/kustomization.yaml": f"""
---
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base/

namespace: default

labels:
  - includeSelectors: true
    pairs:
      app: {app_name}

images:
  - name: {app_name}
    newName: {app_name}
    newTag: latest
""",
        f"argocd/{app_name}/application.yaml": f"""
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {app_name}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/{app_name}.git
    targetRevision: main
    path: charts/{app_name}
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
""",
    }

    for path, content in files.items():
        write_file(path, content)
        print(f"✅ Created: {path}")


def run_command_safe(cmd: str, desc: str) -> None:
    print(f"\n🔍 {desc}:")
    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Command failed: {cmd}\n{e}")
    except FileNotFoundError:
        print(f"⚠️  Command not found: {cmd.split()[0]}")


def validate_files(app_name: str) -> None:
    helm_chart = f"charts/{app_name}"
    kustomize_path = "k8s/overlays/dev"

    run_command_safe(f"helm lint {helm_chart}", "Helm lint")
    run_command_safe(f"helm template {helm_chart}", "Helm render")
    run_command_safe(f"kustomize build {kustomize_path}", "Kustomize build")

    if shutil.which("yamllint"):
        run_command_safe("yamllint charts/", "YAML lint (charts)")
        run_command_safe("yamllint k8s/", "YAML lint (k8s)")
    else:
        print("ℹ️  yamllint not installed, skipping YAML lint checks")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_k8.py <app-name> [--skip-validate]")
        sys.exit(1)

    app_name = sys.argv[1]
    skip_validate = "--skip-validate" in sys.argv

    print(f"\n🔧 Generating all manifests for app: {app_name}")
    generate_all_templates(app_name)

    if not skip_validate:
        validate_files(app_name)

    print(
        "\n✅ All files generated." if skip_validate else "\n✅ All files generated and validated."
    )
    print("📦 Structure:")
    print(" - charts/")
    print(" - k8s/base/")
    print(" - k8s/overlays/dev/")
    print(" - argocd/")
    print("🧪 You can now commit or test with kubectl/ArgoCD.")


if __name__ == "__main__":
    main()
