# Define variables
APP_NAME = STOCK-TECH-FIB
NAMESPACE = STOCK-TECH-FIB

# Kubernetes commands
deploy:
	helm upgrade --install $(APP_NAME) charts/$(APP_NAME) --namespace $(NAMESPACE) --create-namespace

delete:
	helm uninstall $(APP_NAME) --namespace $(NAMESPACE)

status:
	kubectl get all -n $(NAMESPACE)
