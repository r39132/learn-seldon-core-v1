# Getting Started with Sentiment Analyzer

Welcome! This guide will help you start using the Sentiment Analyzer project.

## Prerequisites

By following this guide, you'll have:
- A trained sentiment analysis ML model (for learning purposes)
- A beautiful web UI for sentiment analysis
- Everything running either locally or on Kubernetes

## 📝 Step-by-Step Guide

### Step 1: Prerequisites

Make sure you have:
- macOS (this guide assumes macOS)
- [Homebrew](https://brew.sh) installed

```bash
# Check if Homebrew is installed
brew --version
```

### Step 2: Clone the Repository

```bash
cd ~/Projects  # or wherever you keep projects
gh repo clone <username>/learn-seldon-core-v1  # Using GitHub CLI
cd learn-seldon-core-v1

# Allow direnv to auto-load environment (if installed)
direnv allow .
```

### Step 3: Run Setup

```bash
make setup
```

This will:
- Install pyenv, jenv, direnv, uv, and GitHub CLI
- Install Python 3.12.3 and Java 17
- Create virtual environment
- Install all dependencies
- Set up pre-commit hooks
- Generate training data
- Train the model

### Step 4: Verify Setup

```bash
make validate
```

You should see all checks passing ✅

### Step 5: Run the Application

Start both the model server (port 8001) and UI (port 8000):
```bash
make run
```

Open your browser to: **http://localhost:8000**

To stop the servers:
```bash
make stop
```

To restart after model changes:
```bash
make restart
```

## 🎨 Using the Web Interface

1. Open http://localhost:8000
2. Type or paste text in the text area
3. Click "Analyze Sentiment"
4. See the result: Positive 😊 or Negative 😞

Example texts to try:
- **Positive:** "I absolutely love this product! It's amazing!"
- **Neutral:** "The product works as expected. Nothing special."
- **Negative:** "Terrible quality. Very disappointed."

## 🚢 Deploy to Kubernetes (Optional)

```bash
# Deploy everything to minikube
make k8s-deploy
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📚 Next Steps

Now that you have the basics working, explore:

### 1. Jupyter Notebooks

```bash
make notebook  # Start Jupyter notebook
# or
make jupyter   # Start Jupyter Lab
```

Check out:
- `notebooks/01_train_model.ipynb` - Complete training workflow
- `notebooks/02_inference_test.ipynb` - Interactive testing

### 2. Development Workflow

```bash
make data      # Regenerate training data
make train     # Retrain model
make test      # Run tests
make test-cov  # Tests with coverage
make lint      # Check code quality
make format    # Auto-format code
```

### 3. Explore the Code

Key files:
- `src/app.py` - FastAPI web application
- `src/train_model.py` - Model training
- `src/generate_data.py` - Data generation
- `src/templates/index.html` - Web UI

## 🔧 Common Tasks

```bash
make install       # Update dependencies
make train         # Retrain model
make clean         # Clean cache files
make k8s-clean     # Clean K8s resources
make precommit     # Run code quality checks
make validate      # Verify project setup
```

## ❓ Troubleshooting

**Setup issues:** See [TROUBLESHOOTING_SETUP.md](TROUBLESHOOTING_SETUP.md) for common setup problems.

**Runtime issues:**

```bash
make validate      # Check project setup
make train         # Fix "Model not found"
make install       # Reinstall dependencies
```

**Port conflicts:** Check with `lsof -i :8000` or `lsof -i :8001`

See [QUICKREF.md](QUICKREF.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for more troubleshooting.

## 📖 Documentation

- [TOOLS_SETUP.md](TOOLS_SETUP.md) - Development environment setup
- [TROUBLESHOOTING_SETUP.md](TROUBLESHOOTING_SETUP.md) - Setup troubleshooting
- [README.md](../README.md) - Comprehensive project documentation
- [QUICKREF.md](QUICKREF.md) - Quick reference for commands
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guides

## 💡 Tips

```bash
make help          # See all available commands
make test          # Run tests
make precommit     # Run all code quality checks
make notebook      # Best way to learn the ML pipeline
```

**Environment:** Make sure `direnv` loads environment variables automatically when you `cd` into the project

**Pre-commit hooks:** Run automatically on `git commit` to ensure code quality

## 🎓 Learning Path

**Beginner:**
1. Run the application (`make run`)
2. Try the web interface
3. Explore Jupyter notebooks (`make notebook`)
4. Edit `src/generate_data.py` to modify training data
5. Retrain the model (`make train`)

**Intermediate:**
1. Customize model in `src/train_model.py`
2. Enhance UI in `src/templates/index.html`
3. Add tests in `tests/`
4. Deploy to Kubernetes (`make k8s-deploy`)

**Advanced:**
1. Integrate real datasets
2. Implement deep learning models
3. Add monitoring and observability
4. Deploy to cloud (see [DEPLOYMENT.md](DEPLOYMENT.md))

## 🆘 Getting Help

1. **Setup issues:** See [TROUBLESHOOTING_SETUP.md](TROUBLESHOOTING_SETUP.md)
2. **Quick reference:** Check [QUICKREF.md](QUICKREF.md)
3. **Examples:** Look at existing tests in `tests/`
4. **Deployment help:** See [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Open an issue:** If you're still stuck, open an issue on GitHub

## 🎉 Success!

If you've made it this far, congratulations! You now have:

✅ A working ML pipeline
✅ A trained sentiment analysis model
✅ A web interface for predictions
✅ Knowledge of how to deploy to Kubernetes
✅ A solid foundation for ML projects

**Happy learning and building! 🚀**

---

**Pro Tip:** Star this repository and share it with others learning ML deployment!
