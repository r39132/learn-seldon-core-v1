# Project Summary

Production-ready sentiment analysis with Seldon Core on Kubernetes.

## Features

- **3-class sentiment** (Positive/Neutral/Negative) + confidence scores
- **Scikit-learn** model (Logistic Regression + TF-IDF)
- **FastAPI** web UI
- **Seldon Core** model serving
- **Kubernetes** deployment (minikube)
- **Modern tooling** (pyenv, jenv, direnv, uv, gh)
- **Best practices** (testing, linting, type checking, pre-commit hooks)

## Stats

- **Files:** 45+
- **Code:** ~3,500+ lines
- **Tests:** 80%+ coverage
- **Python:** 3.12.3
- **Dependencies:** 20+ packages
- **Training Data:** 1,000 samples (balanced)

## Quick Commands

```bash
make help      # Show all commands
make setup     # Setup project
make data      # Generate data
make train     # Train model
make run       # Start web UI
make test      # Run tests
make validate  # Verify setup
```

## Technology Stack

**ML:** scikit-learn, pandas, numpy  
**Web:** FastAPI, Jinja2, httpx  
**Serving:** Seldon Core  
**Container:** Docker  
**Orchestration:** Kubernetes (minikube)  
**Tools:** uv, pyenv, jenv, direnv, gh  
**Quality:** black, ruff, mypy, pytest

## Documentation

- [README.md](README.md) - Main overview
- [TOOLS_SETUP.md](TOOLS_SETUP.md) - Dev tools setup
- [GETTING_STARTED.md](GETTING_STARTED.md) - Tutorial
- [DEPLOYMENT.md](DEPLOYMENT.md) - K8s deployment
- [QUICKREF.md](QUICKREF.md) - Quick reference
- [ENHANCEMENTS.md](ENHANCEMENTS.md) - Recent changes

---

Run `make help` to see all available commands.
