#!/bin/bash
# Setup script for macOS

set -e

echo "🚀 Setting up Sentiment Analyzer with Seldon..."

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install from https://brew.sh"
    exit 1
fi

# Install pyenv if not present
if ! command -v pyenv &> /dev/null; then
    echo "📦 Installing pyenv..."
    brew install pyenv
    echo "${YELLOW}⚠️  Please add pyenv to your shell configuration and restart your terminal${NC}"
    echo "   Add to ~/.zshrc or ~/.bash_profile:"
    echo '   export PYENV_ROOT="$HOME/.pyenv"'
    echo '   export PATH="$PYENV_ROOT/bin:$PATH"'
    echo '   eval "$(pyenv init --path)"'
    echo '   eval "$(pyenv init -)"'
fi

# Install jenv if not present
if ! command -v jenv &> /dev/null; then
    echo "📦 Installing jenv..."
    brew install jenv
    echo "${YELLOW}⚠️  Please add jenv to your shell configuration and restart your terminal${NC}"
    echo "   Add to ~/.zshrc or ~/.bash_profile:"
    echo '   export PATH="$HOME/.jenv/bin:$PATH"'
    echo '   eval "$(jenv init -)"'
fi

# Install direnv if not present
if ! command -v direnv &> /dev/null; then
    echo "📦 Installing direnv..."
    brew install direnv
    echo "${YELLOW}⚠️  Please add direnv to your shell configuration and restart your terminal${NC}"
    echo "   Add to ~/.zshrc:"
    echo '   eval "$(direnv hook zsh)"'
    echo "   Or add to ~/.bash_profile:"
    echo '   eval "$(direnv hook bash)"'
fi

# Install GitHub CLI if not present
if ! command -v gh &> /dev/null; then
    echo "📦 Installing GitHub CLI..."
    brew install gh
    echo "${GREEN}✓ Run 'gh auth login' to authenticate with GitHub${NC}"
fi

# Install Python 3.12.3 or later
echo "🐍 Setting up Python 3.12.3..."
if ! pyenv versions | grep -q "3.12.3"; then
    pyenv install 3.12.3
fi
pyenv local 3.12.3

# Install uv
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    brew install uv
fi

# Install Java 17 for Seldon if not present
if ! command -v java &> /dev/null; then
    echo "📦 Installing Java 17 (required for Seldon)..."
    brew install openjdk@17
    if command -v jenv &> /dev/null; then
        jenv add /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home 2>/dev/null || true
        jenv global 17 2>/dev/null || true
    fi
fi

# Allow direnv if available
if command -v direnv &> /dev/null; then
    echo "🔧 Allowing direnv to load .envrc..."
    direnv allow . 2>/dev/null || true
fi

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment with uv..."
if [ ! -d ".venv" ]; then
    uv venv --python 3.12.3
else
    echo "   Virtual environment already exists, skipping..."
fi

echo "📦 Installing Python dependencies..."
source .venv/bin/activate
uv pip install -e ".[dev]"

# Copy .env-example to .env if .env doesn't exist
if [ ! -f .env ] && [ -f .env-example ]; then
    echo "📝 Creating .env file..."
    cp .env-example .env
fi

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

echo "✅ Setup complete!"
echo ""
echo "${GREEN}Next steps:${NC}"
echo "  1. If you installed new tools, restart your terminal and run 'direnv allow .'"
echo "  2. Review and update .env file with your configuration"
echo "  3. Activate virtual environment: 'source .venv/bin/activate'"
echo "  4. Generate training data: 'make data'"
echo "  5. Train the model: 'make train'"
echo "  6. Verify project: 'make validate'"
echo "  7. Start UI: 'make run' (requires Seldon Core deployed)"
echo "  8. For Kubernetes deployment, see docs/SELDON_DEPLOYMENT.md"
echo ""
echo "${GREEN}📖 Documentation:${NC}"
echo "  - Complete tools setup: TOOLS_SETUP.md"
echo "  - Getting started: GETTING_STARTED.md"
