# Hands-On with Seldon (Seldon Core v1): Building ML Training and Inference from Scratch

I've been curious about getting my hands dirty with various ML frameworks recently. One of these is Seldon.

In architecture discussions at scale, Seldon comes up frequently as the ML serving framework of choice for Kubernetes-native deployments. But most documentation and tutorials assume you're already operating production ML platforms — they jump straight to multi-model pipelines, A/B testing, and distributed inference graphs. This creates a gap for engineers trying to understand core concepts before implementing complex production patterns.

To address this, I built a learning-focused repository that strips away the complexity and demonstrates Seldon Core v1's foundational architecture through a practical sentiment analysis implementation.

**Repository**: https://github.com/r39132/learn-seldon/

> **⚠️ Note**: The sentiment analysis model used in this project is intentionally naive (Logistic Regression with TF-IDF) and designed purely for illustration purposes. The focus is on demonstrating Seldon Core v1 deployment architecture and patterns, not state-of-the-art NLP techniques.

This article covers:
- The technical landscape Seldon addresses and how it compares to alternatives
- Seldon's architecture with control plane and data plane components
- Implementation details for ML training and inference deployment
- A walkthrough of the learn-seldon project structure

---

## Problem Context: Scaling ML Model Deployment

[Seldon Core](https://github.com/SeldonIO/seldon-core) is an ML deployment framework built to address the operational challenges of running inference workloads on Kubernetes at scale.

The framework tackles several problems common in production ML deployments:

**Model Serving as Microservices**
ML models deployed as production services require the same operational rigor as other microservices: versioning, rollback capabilities, health checks, and observability. Seldon treats model deployments as first-class Kubernetes resources via Custom Resource Definitions (CRDs).

**Inference Graph Composition**
Real-world inference often requires multiple steps — preprocessing, model execution, ensemble aggregation, and post-processing. Seldon provides declarative inference graphs that compose these components with synchronous HTTP/gRPC communication.

**Language-Agnostic Deployment**
Production ML models are written in various languages (Python, Java, R, Go). Seldon's prepackaged model servers support multiple frameworks (scikit-learn, TensorFlow, PyTorch, XGBoost) while allowing custom containers for specialized logic.

**Traffic Management and Experimentation**
A/B testing, canary deployments, and shadow deployments require sophisticated traffic routing. Seldon implements this through Kubernetes-native mechanisms and service mesh integration.

Core architectural principles:

- Models wrapped in standardized containers exposing REST/gRPC APIs
- Inference graphs define multi-component workflows with synchronous composition
- Kubernetes Operator manages lifecycle of SeldonDeployment resources
- Service orchestrator (Ambassador/Istio/built-in) handles routing and observability
- All configuration expressed as Kubernetes Custom Resources

### Comparison with Alternative Frameworks

The ML serving landscape includes several options, each optimizing for different constraints:

**TorchServe** (PyTorch-specific)
Built for PyTorch models with tight framework integration. Does not provide multi-framework support or Kubernetes-native operations.

**BentoML** (Python SDK-focused)
Framework-agnostic serving with strong Python developer experience. Kubernetes integration is an add-on rather than core design principle.

**KServe** (formerly KFServing)
Kubernetes-native like Seldon but uses serverless paradigm (Knative). Different trade-offs in cold start latency vs resource efficiency.

**Ray Serve** (Distributed Python)
Built on Ray's distributed computing framework. Optimized for Python workloads with complex dependencies. Heavier runtime compared to dedicated inference servers.

**NVIDIA Triton** (High-performance inference)
GPU-optimized inference server supporting TensorFlow, PyTorch, ONNX, TensorRT. Seldon can use Triton as its inference server.

**Seldon's Differentiation**

**Kubernetes-Native Architecture**
Seldon implements ML serving as Kubernetes Custom Resources (SeldonDeployment). This enables:
- HPA integration for autoscaling based on inference metrics
- Native rollout strategies (canary, blue-green) using standard Kubernetes updates
- GitOps workflows using standard Kubernetes tools (ArgoCD, Flux)
- Prometheus and distributed tracing integration via service mesh patterns

**Composable Inference Graphs**
Many production use cases require more than simple model invocation. Seldon supports [inference graphs](https://docs.seldon.io/projects/seldon-core/en/v1.17.1/graph/inference-graph.html) with declarative component composition:
- Preprocessing transformers that normalize input data
- Ensemble models that aggregate predictions from multiple models
- Post-processing components for business rule application
- Conditional routing (A/B testing, multi-armed bandits) based on traffic splitting
- Combiners that merge outputs from parallel model execution

**Prepackaged Model Servers**
Seldon provides ready-to-use model servers for common ML frameworks:
- SKLearn Server for scikit-learn models
- TensorFlow Serving integration
- MLflow Server for MLflow models
- XGBoost Server for XGBoost models
- Custom servers via language wrappers (Python, Java, R, Go, NodeJS)

---

## Architecture Design

Seldon Core v1 implements a Kubernetes Operator pattern that transforms SeldonDeployment CRDs into standard Kubernetes resources (Deployments, Services) with intelligent inference graph orchestration.

### Core Components

**Seldon Core Operator**
Kubernetes controller that manages the lifecycle of ML deployments ([source](https://github.com/SeldonIO/seldon-core/tree/v1.17.1/operator)):
- Watches SeldonDeployment Custom Resources for changes
- Generates Kubernetes Deployments for each predictor component
- Creates Services for inference endpoints
- Manages ConfigMaps for model metadata and configurations
- Implements reconciliation loops to maintain desired state
- Supports multiple replicas per component with horizontal pod autoscaling

**Service Orchestrator**
Request routing layer with multiple implementation options:

*Ambassador (Default)*
- Kubernetes-native API Gateway built on Envoy
- Automatic endpoint discovery via annotations
- Canary and shadow deployments via weighted routing
- Metrics and distributed tracing

*Istio Integration*
- Service mesh integration for advanced traffic management
- mTLS for secure model-to-model communication
- Fine-grained observability and policy enforcement

*Seldon Engine (Built-in)*
- Lightweight service orchestrator included with Seldon
- REST/gRPC support for inference graphs
- Payload logging and metrics collection
- Simplified deployment without external dependencies

**Prepackaged Model Servers**
Ready-to-use containers for common ML frameworks:

- **SKLearn Server** – scikit-learn models (joblib/pickle format)
- **TFServing** – TensorFlow SavedModel format
- **XGBoost Server** – XGBoost models
- **MLflow Server** – MLflow packaged models
- **Triton Inference Server** – GPU-optimized for TensorRT, ONNX

**Language Wrappers**
SDKs for building custom prediction containers:
- Python (most common, includes s2i builder)
- Java (Spring Boot based)
- R (via Plumber)
- Go
- NodeJS

![Seldon Architecture](https://raw.githubusercontent.com/SeldonIO/seldon-core/v1.17.1/doc/source/workflow/diagrams/seldon-core-high-level.svg)

*High-level architecture: Operator translates SeldonDeployment CRDs into Kubernetes workloads*

### Inference Graph Patterns

Seldon supports several graph topologies for composing multi-component inference:

**Single Model**
Simplest deployment with one predictor:
```
Request → Predictor → Response
```

**Transformer → Model**
Preprocessing before prediction:
```
Request → Transformer → Predictor → Response
```

**Model Ensemble (Average/Vote)**
Parallel models combined via combiner:
```
Request → Predictor A ↘
                        → Combiner → Response
Request → Predictor B ↗
```

**A/B Test**
Traffic splitting between model versions:
```
Request → [90% → Predictor A] → Response
          [10% → Predictor B]
```

**Router (Multi-Armed Bandit)**
Dynamic routing based on learned policy:
```
Request → Router → [Predictor A or B or C] → Response
```

### Key Resource: SeldonDeployment CRD

Seldon v1 uses a single primary Custom Resource Definition:

**[SeldonDeployment](https://docs.seldon.io/projects/seldon-core/en/v1.17.1/reference/seldon-deployment.html)** – Complete inference service definition

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: sentiment-classifier
spec:
  predictors:
  - name: default
    replicas: 2
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: seldonio/sklearn-iris:0.1
          resources:
            requests:
              memory: 100Mi
    graph:
      name: classifier
      type: MODEL
      endpoint:
        type: REST
```

**Multi-component inference graph example:**
```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: sentiment-pipeline
spec:
  predictors:
  - name: default
    graph:
      name: transformer
      type: TRANSFORMER
      endpoint:
        type: REST
      children:
      - name: model
        type: MODEL
        endpoint:
          type: REST
```

**Related repos:**
- [SeldonIO/seldon-core](https://github.com/SeldonIO/seldon-core) – Core platform (use v1.17.x branch)
- [SeldonIO/seldon-core/wrappers](https://github.com/SeldonIO/seldon-core/tree/v1.17.1/wrappers) – Language wrappers
- [Seldon v1 Docs](https://docs.seldon.io/projects/seldon-core/en/v1.17.1/) – Official v1 documentation
- [Seldon Examples](https://github.com/SeldonIO/seldon-core/tree/v1.17.1/examples) – Reference implementations

---

## Implementation: Training and Deployment

Deploying models with Seldon requires understanding the division between model code and infrastructure configuration.

### Model Training

Model training follows standard ML framework patterns. The only requirement is serializing the model to a format compatible with the chosen inference server.

**Training script** (`src/train_model.py`):
- Use any ML framework (scikit-learn, TensorFlow, PyTorch, XGBoost)
- Serialize trained model to disk
- For scikit-learn: `joblib.dump(model, "sentiment_model.pkl")`
- For TensorFlow: `model.save("model_directory")`
- For PyTorch: `torch.save(model.state_dict(), "model.pth")`

**Model Artifact Storage**
Inference servers load models from remote storage. Supported backends (via rclone):
- Google Cloud Storage: `gs://bucket-name/path/to/model`
- AWS S3: `s3://bucket-name/path/to/model`
- Azure Blob Storage: `azureblob://container/path/to/model`
- Persistent Volume: `/mnt/models/path/to/model`

### Model Serving Interface

**Option 1: Prepackaged Model Servers**

For standard framework models, use prepackaged servers without custom code:
- scikit-learn: Use `seldonio/sklearn-server` image with joblib/pickle models
- TensorFlow: Use TensorFlow Serving integration
- XGBoost: Use `seldonio/xgboost-server` image
- MLflow: Use `seldonio/mlflow-server` image

**Option 2: Custom Python Wrapper**

For custom preprocessing or inference logic, implement the [Python wrapper interface](https://docs.seldon.io/projects/seldon-core/en/v1.17.1/python/python_component.html):

```python
class SentimentClassifier:
    def __init__(self):
        """Constructor loads model"""
        self.model = joblib.load("/mnt/models/sentiment_model.pkl")

    def predict(self, X, features_names=None):
        """Run inference - required method"""
        return self.model.predict(X)

    def predict_proba(self, X, features_names=None):
        """Return probabilities - optional"""
        return self.model.predict_proba(X)

    def metrics(self):
        """Custom metrics - optional"""
        return [{"type": "COUNTER", "key": "requests", "value": 1}]
```

**Build with s2i (Source-to-Image):**
```bash
s2i build . seldonio/seldon-core-s2i-python38:1.17.1 sentiment-model:0.1
```

### Deployment Configuration

**SeldonDeployment Manifest**

Seldon v1 uses a single CRD that defines the complete inference service.

**Simple deployment** (`k8s/sentiment-deployment.yaml`):
```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: sentiment-classifier
  namespace: seldon-demo
spec:
  predictors:
  - name: default
    replicas: 2
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: your-registry/sentiment-model:0.1
          env:
          - name: MODEL_FILE
            value: /mnt/models/sentiment_model.pkl
          resources:
            requests:
              memory: 100Mi
              cpu: 100m
          volumeMounts:
          - name: model-storage
            mountPath: /mnt/models
        volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: model-pvc
    graph:
      name: classifier
      type: MODEL
      endpoint:
        type: REST
```

**Deployment with preprocessing** (`k8s/sentiment-pipeline.yaml`):
```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: sentiment-pipeline
spec:
  predictors:
  - name: default
    componentSpecs:
    - spec:
        containers:
        - name: transformer
          image: your-registry/text-transformer:0.1
        - name: model
          image: your-registry/sentiment-model:0.1
    graph:
      name: transformer
      type: TRANSFORMER
      endpoint:
        type: REST
      children:
      - name: model
        type: MODEL
        endpoint:
          type: REST
```

**Apply deployment:**

```bash
# Install Seldon Core operator (one-time setup)
kubectl create namespace seldon-system
kubectl apply -f https://github.com/SeldonIO/seldon-core/releases/download/v1.17.1/seldon-core-operator.yaml

# Deploy model
kubectl apply -f k8s/sentiment-deployment.yaml

# Check status
kubectl get seldondeployments -n seldon-demo
kubectl get pods -n seldon-demo
```

**Key Files in learn-seldon:**

| File | Purpose |
|------|---------|
| `src/train_model.py` | Train scikit-learn model |
| `src/seldon_model.py` | Seldon v1 Python wrapper implementation |
| `src/model_server.py` | Simple FastAPI server (baseline without Seldon) |
| `k8s/namespace.yaml` | Kubernetes namespace |
| `k8s/model-server-deployment.yaml` | Deploy model server |
| `k8s/fastapi-deployment.yaml` | Deploy web UI |
| `k8s/seldon-deployment.yaml` | SeldonDeployment CRD manifest |
| `.s2i/environment` | s2i build configuration |

The project shows **two deployment paths**:
1. **Simplified** – FastAPI model server (no Seldon, for learning)
2. **Production** – Seldon Core v1 with SeldonDeployment CRD (see `k8s/seldon-deployment.yaml`)

---

## Reference Implementation: learn-seldon

The [learn-seldon](https://github.com/r39132/learn-seldon) repository provides a working implementation demonstrating Seldon's core concepts through a sentiment analysis use case.

**Technical Scope**
- Three-class sentiment classification (Positive, Neutral, Negative)
- Scikit-learn model trained on text features
- Two deployment paths:
  - Simplified: Standalone FastAPI server for local development
  - Production: Full Seldon Core with Kubernetes CRDs
- Complete end-to-end pipeline from data generation to deployed inference

**Learning Objectives**
- Understanding SeldonDeployment CRD structure and semantics
- Operator pattern for ML deployment lifecycle management
- Building custom prediction containers with Python wrapper
- Composing inference graphs (transformers, combiners, routers)
- Integration with service orchestrators (Ambassador/Istio)
- Implementing canary deployments and A/B tests

### Quick Start

```bash
# Clone and setup
git clone https://github.com/r39132/learn-seldon
cd learn-seldon
make setup

# Generate data and train model
make data && make train

# Run locally (no Kubernetes needed)
make run

# Deploy to Kubernetes (with minikube)
make k8s-deploy
```

**Project features:**
- ✅ Makefile-driven automation
- ✅ Pre-commit hooks (black, ruff, mypy, pytest)
- ✅ Jupyter notebooks for exploration
- ✅ Dockerfiles for both FastAPI and Seldon deployments
- ✅ Kubernetes manifests with detailed comments

---

## Summary

Seldon Core v1 addresses operational challenges in production ML deployments through Kubernetes-native architecture. The framework provides:

- Declarative ML deployments via SeldonDeployment CRD
- Composable inference graphs with transformers, routers, and combiners
- Prepackaged model servers for common frameworks (sklearn, TensorFlow, XGBoost)
- Language-agnostic custom containers via Python/Java/R/Go wrappers
- Sophisticated traffic management for A/B tests and canary deployments
- Service mesh integration for observability and security

The initial learning curve exists because Seldon optimizes for operational concerns (reusability, composition, standardization) rather than single-model simplicity. This trade-off makes sense for organizations operating multiple models in production with existing Kubernetes infrastructure.

The learn-seldon repository provides a reference implementation focused on v1 core concepts before introducing production complexity. This approach addresses the gap between "hello world" tutorials and production-grade deployments.

**Repository**: https://github.com/r39132/learn-seldon/

Contributions addressing gaps in documentation, additional examples, or new learning scenarios are welcome via pull requests and issues.
