# Define variables
APP_NAME = TEMPLATE_PYTHON
NAMESPACE = TEMPLATE_PYTHON

# Kubernetes commands
deploy:
	helm upgrade --install $(APP_NAME) charts/$(APP_NAME) --namespace $(NAMESPACE) --create-namespace

delete:
	helm uninstall $(APP_NAME) --namespace $(NAMESPACE)

status:
	kubectl get all -n $(NAMESPACE)
