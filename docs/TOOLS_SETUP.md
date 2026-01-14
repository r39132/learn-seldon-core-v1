# Development Tools Setup Guide

Complete guide for setting up all development tools used in this project.

## Overview

This project uses modern Python development tools and best practices:

- **pyenv** - Python version management
- **jenv** - Java version management (for Seldon dependencies)
- **direnv** - Automatic environment variable loading
- **uv** - Fast Python package installer
- **gh** - GitHub CLI for repository management
- **pre-commit** - Git hooks for code quality
- **Docker** - Container runtime
- **kubectl** - Kubernetes CLI
- **minikube** - Local Kubernetes cluster

## Setup Guide (macOS)

Follow these steps in order to set up your development environment.

### Step 1: Install Homebrew

Homebrew is required for all subsequent installations:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (Apple Silicon)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Step 2: Clone Repository and Run Setup

```bash
# Clone repository (if using GitHub)
gh repo clone <username>/learn-seldon-core-v1
cd learn-seldon-core-v1

# Run automated setup
make setup
```

**What `make setup` installs and configures:**
- Installs missing tools: pyenv, jenv, direnv, uv, gh, Java 17
- Configures Python 3.12.3 with pyenv
- Creates virtual environment with uv
- Installs all Python dependencies (including dev dependencies)
- Sets up pre-commit hooks
- Generates training data
- Trains the initial model

### Step 3: Configure Shell Integration

Add these hooks to your shell configuration file:

```bash
# Add to ~/.zshrc (for zsh) or ~/.bash_profile (for bash)

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# jenv
export PATH="$HOME/.jenv/bin:$PATH"
eval "$(jenv init -)"

# direnv
eval "$(direnv hook zsh)"  # or: eval "$(direnv hook bash)" for bash
```

### Step 4: Restart Terminal and Activate Environment

```bash
# Close and reopen your terminal, then:
cd learn-seldon-core-v1

# Allow direnv to load environment variables
direnv allow .

# Activate virtual environment
source .venv/bin/activate
```

### Step 5: Install Kubernetes Tools (Optional)

Only needed if you plan to deploy to Kubernetes:

#### Docker Desktop

```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop
open -a Docker

# Verify installation
docker --version
```

**Configuration:**
1. Open Docker Desktop
2. Go to Preferences → Resources
3. Allocate at least 4GB RAM and 2 CPUs

#### kubectl

```bash
# Install kubectl
brew install kubectl

# Verify installation
kubectl version --client
```

#### minikube

```bash
# Install minikube
brew install minikube

# Start minikube with Docker driver
minikube start --driver=docker --cpus=4 --memory=8192

# Enable metrics server (optional)
minikube addons enable metrics-server

# Verify installation
minikube status
kubectl get nodes
```

## Tool Configuration Files

The project uses these configuration files:

```
learn-seldon-core-v1/
├── .python-version          # pyenv: Python 3.12.3
├── .java-version            # jenv: Java 17
├── .envrc                   # direnv: Environment variables
├── .pre-commit-config.yaml  # Pre-commit hooks
├── pyproject.toml           # Project metadata & dependencies
└── .gitignore               # Git ignore patterns
```

## Environment Variables

The `.envrc` file automatically sets these variables when you enter the project directory:

```bash
PROJECT_NAME="sentiment-analyzer"
LOG_LEVEL="INFO"
MODEL_SERVER_HOST="localhost"
MODEL_SERVER_PORT="8001"
# ... and more
```

To override, create a `.env` file (gitignored):

```bash
cp .env-example .env
# Edit .env with your custom values
```

### Step 6: Verify Setup

Run the automated verification:

```bash
# Verify development environment (tools and dependencies)
make validate-setup

# Validate project configuration and data
make validate
```

**What `make validate-setup` checks:**
- Python version (should be 3.12.3)
- Java version (should be 17.x.x)
- Package managers (uv, gh)
- Docker and Kubernetes tools (optional - only if installed in Step 5)
- Python dependencies
- Pre-commit hooks

**What `make validate` checks:**
- Configuration files exist (.python-version, .java-version, .envrc, etc.)
- Documentation files exist
- Python environment compatibility
- Training data quality and balance

> **Having issues?** See [TROUBLESHOOTING_SETUP.md](TROUBLESHOOTING_SETUP.md) for common problems and solutions.

## Best Practices

1. **Always use virtual environments** - Never install packages globally
2. **Use uv for package management** - Faster and more reliable than pip
3. **Commit .python-version and .java-version** - Ensures team uses same versions
4. **Never commit .env files** - Use .env-example as a template
5. **Run pre-commit hooks before pushing** - Catches issues early
6. **Keep tools updated** - Run `brew upgrade` monthly
7. **Use direnv** - Automatically loads environment variables

## Additional Resources

- [pyenv Documentation](https://github.com/pyenv/pyenv)
- [jenv Documentation](https://www.jenv.be/)
- [direnv Documentation](https://direnv.net/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [minikube Documentation](https://minikube.sigs.k8s.io/docs/)

---

For project-specific setup, see [GETTING_STARTED.md](GETTING_STARTED.md).
