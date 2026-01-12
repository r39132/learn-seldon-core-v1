.PHONY: help setup install test lint format clean run train data docker-build k8s-deploy k8s-clean

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

run: ## Run FastAPI UI (requires model server running)
	@echo "🌐 Starting FastAPI UI..."
	@echo "⚠️  Note: Model server must be running on port 8001"
	@echo "   Run 'make run-model-server' in another terminal first"
	@uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

run-model-server: ## Run model server
	@echo "🤖 Starting model server..."
	@MODEL_PATH=models/sentiment_model.pkl uvicorn src.model_server:app --host 0.0.0.0 --port 8001

run-local: ## Run both UI and model server locally
	@./scripts/run-local.sh

docker-build: ## Build Docker images
	@echo "🐳 Building Docker images..."
	@docker build -t sentiment-classifier:latest -f Dockerfile.seldon .
	@docker build -t sentiment-ui:latest -f Dockerfile.fastapi .

k8s-deploy: ## Deploy to Kubernetes
	@echo "☸️  Deploying to Kubernetes..."
	@./scripts/deploy-k8s.sh

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

validate: ## Validate project configuration and data
	@echo "✅ Running project validation..."
	@python scripts/validate.py

.DEFAULT_GOAL := help
