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

## macOS Installation Guide

### 1. Homebrew (Package Manager)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH (Apple Silicon)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. pyenv (Python Version Manager)

```bash
# Install pyenv
brew install pyenv

# Add to shell configuration (~/.zshrc or ~/.bash_profile)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Install Python 3.12.3
pyenv install 3.12.3
pyenv global 3.12.3

# Verify installation
python --version  # Should show: Python 3.12.3
```

### 3. jenv (Java Version Manager)

```bash
# Install jenv
brew install jenv

# Add to shell configuration
echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(jenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Install Java 17 (required for Seldon)
brew install openjdk@17

# Add to jenv
jenv add /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home

# Set global version
jenv global 17

# Verify installation
java -version  # Should show: openjdk version "17.x.x"
```

### 4. direnv (Environment Variable Manager)

```bash
# Install direnv
brew install direnv

# Add to shell configuration
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc  # for zsh
# OR
echo 'eval "$(direnv hook bash)"' >> ~/.bash_profile  # for bash

# Reload shell
source ~/.zshrc

# Allow direnv in project directory
cd /path/to/learn-seldon
direnv allow .
```

**Usage:**
- `direnv allow` - Allow .envrc in current directory
- `direnv deny` - Block .envrc in current directory
- `direnv reload` - Reload environment variables
- When you `cd` into the project, direnv automatically loads environment variables

### 5. uv (Fast Python Package Manager)

```bash
# Install uv
brew install uv

# Verify installation
uv --version
```

**Why uv?**
- 10-100x faster than pip
- Better dependency resolution
- Drop-in replacement for pip/pip-tools
- Used by this project for all package management

### 6. GitHub CLI

```bash
# Install gh
brew install gh

# Authenticate with GitHub
gh auth login

# Verify installation
gh --version

# Configure git to use gh
gh auth setup-git
```

### 7. Docker Desktop

```bash
# Install Docker Desktop
brew install --cask docker

# Start Docker Desktop from Applications
# Or use command line:
open -a Docker

# Verify installation
docker --version
docker-compose --version
```

**Post-installation:**
1. Open Docker Desktop
2. Go to Preferences → Resources
3. Allocate at least 4GB RAM and 2 CPUs for Kubernetes

### 8. kubectl (Kubernetes CLI)

```bash
# Install kubectl
brew install kubectl

# Verify installation
kubectl version --client
```

### 9. minikube (Local Kubernetes)

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

### 10. Additional Development Tools

```bash
# Install helpful tools
brew install tree     # Directory tree visualization
brew install jq       # JSON processor
brew install htop     # Process viewer
brew install watch    # Execute commands periodically
```

## Project Setup

Once all tools are installed, set up the project:

```bash
# Clone repository (if using GitHub)
gh repo clone <username>/learn-seldon
cd learn-seldon

# Allow direnv to load environment
direnv allow .

# Create virtual environment with uv
uv venv .venv --python 3.12.3

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
make help
```

## Tool Configuration Files

The project uses these configuration files:

```
learn-seldon/
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

## Verifying Your Setup

Run this comprehensive check:

```bash
# Python version
python --version          # Should be 3.12.3

# Java version
java -version            # Should be 17.x.x

# Package manager
uv --version             # Should show uv version

# GitHub CLI
gh --version             # Should show gh version

# Docker
docker --version         # Should show Docker version

# Kubernetes
kubectl version --client # Should show kubectl version
minikube status          # Should show "Running"

# Project dependencies
python -c "import fastapi; import sklearn; print('✅ Dependencies OK')"

# Pre-commit hooks
pre-commit run --all-files  # Should run all hooks
```

## Common Issues and Solutions

### pyenv: "python: command not found"

```bash
# Ensure pyenv is in PATH
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

### jenv: "java: command not found"

```bash
# Add Java to jenv
jenv add /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
jenv global 17
```

### direnv: "direnv: error .envrc is blocked"

```bash
# Allow direnv in the project directory
direnv allow .
```

### uv: "command not found"

```bash
# Install uv via brew
brew install uv

# Or use pip
pip install uv
```

### Docker: "Cannot connect to the Docker daemon"

```bash
# Ensure Docker Desktop is running
open -a Docker

# Wait for Docker to start, then verify
docker ps
```

### minikube: "Exiting due to MK_USAGE: Docker driver with privileged mode"

```bash
# Use Docker driver explicitly
minikube delete
minikube start --driver=docker
```

## Updating Tools

Keep your tools up to date:

```bash
# Update Homebrew and packages
brew update
brew upgrade

# Update Python packages
uv pip install --upgrade pip
uv pip install --upgrade -r requirements.txt

# Update pre-commit hooks
pre-commit autoupdate

# Update minikube
brew upgrade minikube
```

## IDE Integration

### VS Code Extensions

Recommended extensions for this project:

```bash
# Install via command line
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension eamodio.gitlens
code --install-extension GitHub.copilot
```

Or search in VS Code Extensions:
- Python
- Pylance
- Docker
- Kubernetes
- GitLens
- GitHub Copilot

### VS Code Settings

The project includes recommended settings in `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

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
