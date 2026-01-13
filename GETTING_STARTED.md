# Getting Started with Sentiment Analyzer

Welcome! This guide will help you get started with the Sentiment Analyzer project in just a few minutes.

> **⚠️ Note**: This project uses a naive sentiment analysis model (Logistic Regression with TF-IDF) designed for educational purposes only. The focus is on demonstrating Seldon Core v1 deployment patterns, not production-grade NLP.

## 🎯 What You'll Build

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
gh repo clone <username>/learn-seldon  # Using GitHub CLI
cd learn-seldon

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
make docker-build  # Build Docker images
make validate      # Verify project setup
```

## ❓ Troubleshooting

```bash
make validate      # Check project setup
make train         # Fix "Model not found"
make setup         # Reinstall dependencies
```

**Port conflicts:** Check with `lsof -i :8000`

See [QUICKREF.md](QUICKREF.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for more troubleshooting.

## 📖 Documentation

- **README.md** - Comprehensive project documentation
- **QUICKREF.md** - Quick reference for commands
- **PROJECT_SUMMARY.md** - Project overview
- **CONTRIBUTING.md** - How to contribute

## 💡 Tips

```bash
make help          # See all available commands
make test          # Run before committing
make notebook      # Best way to learn the ML pipeline
```

**direnv:** Automatically loads environment when you `cd` into the project
**Pre-commit hooks:** Run automatically on `git commit` (setup.sh installs them)

## 🎓 Learning Path

**Beginner:**
1. `make setup && make run`
2. Try the web interface
3. `make notebook` - Explore Jupyter notebooks
4. Edit `src/generate_data.py` - Modify training data

**Intermediate:**
1. Customize model in `src/train_model.py`
2. Enhance UI in `src/templates/index.html`
3. Add tests in `tests/`
4. `make k8s-deploy` - Deploy to Kubernetes

**Advanced:**
1. Integrate real datasets
2. Implement deep learning models
3. Add monitoring and observability
4. Deploy to cloud (see [DEPLOYMENT.md](DEPLOYMENT.md))

## 🆘 Getting Help

1. Check the **Troubleshooting** section in README.md
2. Review **QUICKREF.md** for quick answers
3. Look at existing tests for examples
4. Open an issue on GitHub

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
