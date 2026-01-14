.PHONY: help setup data train k8s-deploy-model-server k8s-ms-logs k8s-clean clean-build-artifacts notebook k8s-ms-status run-ui stop-ui

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Run initial setup
	@echo "🚀 Running setup..."
	@chmod +x scripts/*.sh
	@./scripts/setup.sh

data: ## Generate training data
	@echo "📊 Generating training data..."
	@python src/generate_data.py

train: ## Train model
	@echo "🤖 Training model..."
	@python src/train_model.py

run-ui: ## Start UI server locally (requires Seldon Core deployed)
	@./scripts/run-local.sh

stop-ui: ## Stop UI server
	@echo "🛑 Stopping UI server..."
	@lsof -ti:8000 | xargs kill -9 2>/dev/null || true
	@echo "✅ UI server stopped"

k8s-deploy-model-server: ## Deploy model to Kubernetes with Seldon Core v1
	@echo "☸️  Deploying model server to Kubernetes..."
	@./scripts/deploy-seldon.sh

k8s-ms-status: ## Show deployments, pods, services
	@echo "📊 Checking Seldon deployment status..."
	@echo ""
	@echo "SeldonDeployments:"
	@kubectl get seldondeployments -n seldon 2>/dev/null || echo "  No SeldonDeployments found"
	@echo ""
	@echo "Pods:"
	@kubectl get pods -n seldon 2>/dev/null || echo "  No pods found"
	@echo ""
	@echo "Services:"
	@kubectl get svc -n seldon 2>/dev/null || echo "  No services found"

k8s-ms-logs: ## Stream pod logs from Seldon Core v1 model server
	@echo "📝 Viewing model server logs..."
	@kubectl logs -f -l seldon-deployment-id=sentiment-classifier -n seldon --tail=50

k8s-clean: ## Delete all Kubernetes resources
	@echo "🧹 Cleaning up Kubernetes..."
	@./scripts/cleanup-k8s.sh

clean-build-artifacts: ## Clean up generated files
	@echo "🧹 Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/ .coverage build/ dist/

notebook: ## Start Jupyter notebook
	@echo "📓 Starting Jupyter notebook..."
	@jupyter notebook

.DEFAULT_GOAL := help
