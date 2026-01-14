.PHONY: help setup install test lint format clean run train data docker-build k8s-deploy k8s-clean stop restart validate-setup precommit

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Run initial setup
	@echo "🚀 Running setup..."
	@chmod +x scripts/*.sh
	@./scripts/setup.sh

install: ## Install dependencies
	@echo "📦 Installing dependencies..."
	@uv pip install -e ".[dev]"

test:
	@echo "🧪 Running tests..."
	@pytest

test-cov:
	@echo "🧪 Running tests with coverage..."
	@pytest --cov=src --cov-report=html --cov-report=term

lint:
	@echo "🔍 Running linters..."
	@ruff check src/ tests/
	@mypy src/

format:
	@echo "✨ Formatting code..."
	@black src/ tests/
	@ruff check --fix src/ tests/

precommit: ## Run code quality checks (format, lint, test)
	@echo "🔧 Running code quality checks..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) test
	@echo "✅ All quality checks passed!"

data: ## Generate training data
	@echo "📊 Generating training data..."
	@python src/generate_data.py

train: ## Train model
	@echo "🤖 Training model..."
	@python src/train_model.py

run: ## Start UI (requires Seldon Core deployed)
	@./scripts/run-local.sh

stop: ## Stop UI server
	@echo "🛑 Stopping UI server..."
	@lsof -ti:8000 | xargs kill -9 2>/dev/null || true
	@echo "✅ UI server stopped"

restart: stop run ## Restart UI server

docker-build: ## Build Docker images for Seldon deployment
	@echo "🐳 Building Docker images..."
	@docker build -t sentiment-seldon:latest -f Dockerfile.seldon .
	@docker build -t sentiment-ui:latest -f Dockerfile.fastapi .

docker-build-seldon: ## Build Seldon model image
	@echo "🐳 Building Seldon model image..."
	@docker build -t sentiment-seldon:latest -f Dockerfile.seldon .

k8s-deploy: ## Deploy to Kubernetes (non-Seldon FastAPI version)
	@echo "☸️  Deploying to Kubernetes..."
	@./scripts/deploy-k8s.sh

k8s-deploy-seldon: ## Deploy to Kubernetes with Seldon Core
	@echo "☸️  Deploying to Kubernetes with Seldon Core..."
	@./scripts/deploy-seldon.sh

k8s-seldon-status: ## Check Seldon deployment status
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

k8s-seldon-logs: ## View Seldon deployment logs
	@echo "📝 Viewing Seldon deployment logs..."
	@kubectl logs -f -l seldon-deployment-id=sentiment-classifier -n seldon --tail=50

k8s-seldon-forward: ## Port forward to Seldon service (background process)
	@echo "🌐 Setting up port forwarding to Seldon service..."
	@echo "  Access at: http://localhost:8080/api/v1.0/predictions"
	@echo "  Press Ctrl+C to stop port forwarding"
	@kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000

k8s-seldon-test: ## Test Seldon deployment
	@./scripts/test-seldon.sh

k8s-clean: ## Clean up Kubernetes resources
	@echo "🧹 Cleaning up Kubernetes..."
	@./scripts/cleanup-k8s.sh

clean: ## Clean up generated files
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

jupyter: ## Start Jupyter lab
	@echo "📓 Starting Jupyter lab..."
	@jupyter lab

validate: ## Validate project configuration and data
	@echo "✅ Running project validation..."
	@python scripts/validate.py

validate-setup: ## Verify development environment setup
	@echo "🔍 Verifying Development Environment Setup"
	@echo "=========================================="
	@echo ""
	@echo "📦 Checking installed tools..."
	@echo ""
	@echo -n "Python version: "
	@python --version 2>/dev/null || echo "❌ Not found"
	@echo -n "Java version: "
	@java -version 2>&1 | head -n 1 || echo "❌ Not found"
	@echo -n "uv: "
	@uv --version 2>/dev/null || echo "❌ Not found"
	@echo -n "gh: "
	@gh --version 2>/dev/null | head -n 1 || echo "❌ Not found"
	@echo -n "Docker: "
	@docker --version 2>/dev/null || echo "⚠️  Not found (optional for local dev)"
	@echo -n "kubectl: "
	@kubectl version --client 2>/dev/null | head -n 1 || echo "⚠️  Not found (optional for k8s)"
	@echo -n "minikube: "
	@minikube version 2>/dev/null | head -n 1 || echo "⚠️  Not found (optional for k8s)"
	@echo ""
	@echo "🐍 Checking Python dependencies..."
	@python -c "import fastapi; import sklearn; print('✅ Core dependencies installed')" 2>/dev/null || echo "❌ Dependencies missing - run 'make install'"
	@echo ""
	@echo "🔧 Checking pre-commit hooks..."
	@pre-commit run --all-files --show-diff-on-failure 2>&1 | head -n 20 || echo "⚠️  Pre-commit hooks not configured"
	@echo ""
	@echo "=========================================="
	@echo "✅ Setup verification complete"
	@echo "Run 'make validate' to check project data"

.DEFAULT_GOAL := help
