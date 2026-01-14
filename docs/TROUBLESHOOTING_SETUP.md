# Development Tools Troubleshooting Guide

Common issues and solutions when setting up development tools for this project.

## Tool Installation Issues

### pyenv: "python: command not found"

**Problem:** Python commands don't work after installing pyenv.

**Solution:**
```bash
# Ensure pyenv is in PATH
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Make sure these lines are added to your shell configuration file (`~/.zshrc` or `~/.bash_profile`), then restart your terminal.

### jenv: "java: command not found"

**Problem:** Java commands don't work after installing jenv.

**Solution:**
```bash
# Add Java to jenv
jenv add /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
jenv global 17

# Verify
java -version
```

If the path doesn't exist, check where Homebrew installed Java:
```bash
brew info openjdk@17
```

### direnv: "direnv: error .envrc is blocked"

**Problem:** Environment variables aren't loading when entering the project directory.

**Solution:**
```bash
# Allow direnv in the project directory
direnv allow .
```

You need to explicitly allow direnv for each project directory for security reasons.

### uv: "command not found"

**Problem:** uv package manager is not found.

**Solution:**
```bash
# Install uv via brew
brew install uv

# Or use pip
pip install uv

# Verify installation
uv --version
```

## Docker and Kubernetes Issues

### Docker: "Cannot connect to the Docker daemon"

**Problem:** Docker commands fail because the daemon isn't running.

**Solution:**
```bash
# Ensure Docker Desktop is running
open -a Docker

# Wait for Docker to start, then verify
docker ps
```

Make sure Docker Desktop is configured to start on login in its preferences.

### minikube: "Exiting due to MK_USAGE: Docker driver with privileged mode"

**Problem:** minikube fails to start with Docker driver.

**Solution:**
```bash
# Delete existing cluster and start fresh
minikube delete
minikube start --driver=docker

# If that doesn't work, specify resources explicitly
minikube start --driver=docker --cpus=4 --memory=8192
```

### kubectl: "connection refused" or "server not found"

**Problem:** kubectl commands fail to connect to Kubernetes cluster.

**Solution:**
```bash
# Ensure minikube is running
minikube status

# If not running, start it
minikube start

# Verify kubectl can connect
kubectl get nodes
```

## Python Environment Issues

### Virtual environment not activating

**Problem:** `source .venv/bin/activate` fails or doesn't work.

**Solution:**
```bash
# Ensure virtual environment was created
ls -la .venv/

# If it doesn't exist, create it
uv venv --python 3.12.3

# Then activate
source .venv/bin/activate

# Verify you're in the venv
which python
```

### Package installation fails

**Problem:** `uv pip install` or `make install` fails.

**Solution:**
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Try installing with more verbose output
uv pip install -e ".[dev]" -v

# If a specific package fails, try installing dependencies first
uv pip install wheel setuptools
```

### ImportError: No module named 'sklearn'

**Problem:** Python can't find installed packages.

**Solution:**
```bash
# Verify you're using the venv Python
which python
# Should show: /path/to/project/.venv/bin/python

# If not, activate the venv
source .venv/bin/activate

# Reinstall dependencies
make install
```

## Shell Configuration Issues

### Changes to ~/.zshrc or ~/.bash_profile not taking effect

**Problem:** Added the required exports but tools still don't work.

**Solution:**
```bash
# Reload your shell configuration
source ~/.zshrc  # for zsh
# OR
source ~/.bash_profile  # for bash

# Or simply restart your terminal
```

### Multiple Python versions causing conflicts

**Problem:** System Python interfering with pyenv Python.

**Solution:**
```bash
# Check which Python is being used
which python
python --version

# Ensure pyenv is taking precedence
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Set local Python version in project
cd /path/to/learn-seldon-core-v1
pyenv local 3.12.3
```

## Pre-commit Hook Issues

### pre-commit hooks failing

**Problem:** `pre-commit run` fails or prevents commits.

**Solution:**
```bash
# Reinstall pre-commit hooks
pre-commit uninstall
pre-commit install

# Update to latest versions
pre-commit autoupdate

# Run manually to see specific errors
pre-commit run --all-files
```

### Black or Ruff formatting issues

**Problem:** Code formatting checks fail during pre-commit.

**Solution:**
```bash
# Format code manually
make format

# Then try committing again
git add .
git commit -m "Your message"
```

## GitHub CLI Issues

### gh: command not found

**Problem:** GitHub CLI not available after installation.

**Solution:**
```bash
# Install via Homebrew
brew install gh

# Verify installation
gh --version

# Authenticate
gh auth login
```

### gh auth login fails

**Problem:** Cannot authenticate with GitHub.

**Solution:**
```bash
# Try logging in with web browser
gh auth login --web

# Or use a personal access token
gh auth login --with-token < your-token.txt
```

## Data and Model Issues

### Training data not found

**Problem:** Model training fails because data is missing.

**Solution:**
```bash
# Generate training data
make data

# Verify data exists
ls -lh data/raw/sentiment_data.csv
```

### Model training fails

**Problem:** `make train` or training script fails.

**Solution:**
```bash
# Ensure dependencies are installed
make install

# Ensure data exists
make data

# Check for errors
python src/train_model.py

# Check logs for specific error messages
```

## Getting Help

If you encounter an issue not covered here:

1. **Check the logs** - Most tools provide verbose output with `-v` or `--verbose`
2. **Verify versions** - Check tool versions match requirements
3. **Check PATH** - Ensure tools are in your PATH: `echo $PATH`
4. **Review documentation** - See [TOOLS_SETUP.md](TOOLS_SETUP.md) for installation steps
5. **Clean and retry** - Try `make clean-build-artifacts` then `make setup`

## Additional Resources

- [pyenv troubleshooting](https://github.com/pyenv/pyenv/wiki/Common-build-problems)
- [Docker Desktop troubleshooting](https://docs.docker.com/desktop/troubleshoot/overview/)
- [minikube troubleshooting](https://minikube.sigs.k8s.io/docs/drivers/docker/)
- [direnv troubleshooting](https://github.com/direnv/direnv/wiki)

---

For setup instructions, see [TOOLS_SETUP.md](TOOLS_SETUP.md).
