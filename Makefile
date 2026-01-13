.PHONY: help setup install test lint format clean run train data docker-build k8s-deploy k8s-clean stop restart

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

test: ## Run tests
	@echo "🧪 Running tests..."
	@pytest

test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	@pytest --cov=src --cov-report=html --cov-report=term

lint: ## Run linting
	@echo "🔍 Running linters..."
	@ruff check src/ tests/
	@mypy src/

format: ## Format code
	@echo "✨ Formatting code..."
	@black src/ tests/
	@ruff check --fix src/ tests/

data: ## Generate training data
	@echo "📊 Generating training data..."
	@python src/generate_data.py

train: ## Train model
	@echo "🤖 Training model..."
	@python src/train_model.py

run: ## Start both UI and model server
	@./scripts/run-local.sh

stop: ## Stop all local servers
	@echo "🛑 Stopping servers..."
	@lsof -ti:8000,8001 | xargs kill -9 2>/dev/null || true
	@echo "✅ Servers stopped"

restart: stop run ## Restart servers

docker-build: ## Build Docker images
	@echo "🐳 Building Docker images..."
	@docker build -t sentiment-seldon:latest -f Dockerfile.seldon .
	@docker build -t sentiment-model-server:latest -f Dockerfile.modelserver .
	@docker build -t sentiment-ui:latest -f Dockerfile.fastapi .

docker-build-seldon: ## Build only Seldon model image
	@echo "🐳 Building Seldon model image..."
	@docker build -t sentiment-seldon:latest -f Dockerfile.seldon .

k8s-deploy: ## Deploy to Kubernetes (non-Seldon FastAPI version)
	@echo "☸️  Deploying to Kubernetes..."
	@./scripts/deploy-k8s.sh

k8s-deploy-seldon: ## Deploy to Kubernetes with Seldon Core
	@echo "☸️  Deploying to Kubernetes with Seldon Core..."
	@./scripts/deploy-seldon.sh

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

pre-commit: ## Run pre-commit hooks
	@echo "🔧 Running pre-commit hooks..."
	@pre-commit run --all-files

pre-push: ## Run pre-push hooks
	@echo "🚀 Running pre-push hooks..."
	@pre-commit run --hook-stage pre-push --all-files

pre-commit-install: ## Install pre-commit hooks
	@echo "📦 Installing pre-commit hooks..."
	@pre-commit install
	@pre-commit install --hook-type pre-push
	@echo "✅ Pre-commit and pre-push hooks installed"

validate: ## Validate project configuration and data
	@echo "✅ Running project validation..."
	@python scripts/validate.py

.DEFAULT_GOAL := help
