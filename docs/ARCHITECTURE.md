# Architecture Documentation

## Table of Contents

- [System Architecture](#system-architecture)
- [Deployment Architectures](#deployment-architectures)
- [Data Flow](#data-flow)
- [Component Details](#component-details)
- [Technology Stack](#technology-stack)
- [Resource Requirements](#resource-requirements)
- [Scaling Considerations](#scaling-considerations)
- [Security](#security)
- [Monitoring & Observability](#monitoring--observability)

## System Architecture

### High-Level Architecture

```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    subgraph UI["User Interface"]
        Browser["Web Browser<br/>HTML/CSS/JS Frontend<br/>- Text Input Area<br/>- Submit Button<br/>- Sentiment Result Display"]
    end

    subgraph AppLayer["Application Layer"]
        FastAPI["FastAPI Web Server<br/>Port 8000<br/><br/>Endpoints:<br/>GET / → Render UI<br/>POST /analyze → Analyze sentiment<br/>GET /health → Health check"]
    end

    subgraph ModelLayer["Model Serving Layer"]
        Seldon["Seldon Core Model Server<br/>Port 9000<br/><br/>SentimentClassifier Wrapper<br/>- predict()<br/>- predict_proba()<br/>- health_status()"]
    end

    subgraph MLLayer["ML Model Layer"]
        Pipeline["Scikit-Learn Pipeline"]
        TFIDF["TF-IDF Vectorizer<br/>max_features: 5000<br/>ngram_range: 1,2"]
        LogReg["Logistic Regression<br/>binary classification<br/>positive/negative<br/>max_iter: 1000"]

        Pipeline --> TFIDF
        TFIDF --> LogReg
    end

    subgraph DataLayer["Data Layer"]
        Model["Stored Model:<br/>models/sentiment_model.pkl"]
        Data["Training Data:<br/>data/raw/sentiment_data.csv"]
    end

    Browser -->|HTTP POST /analyze| FastAPI
    FastAPI -->|REST API Call| Seldon
    Seldon -->|Load & Predict| Pipeline
    Pipeline -.->|Uses| Model
```

## Deployment Architectures

### Local Development

```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    subgraph DevMachine["Developer Machine - macOS"]
        subgraph VirtualEnv[".venv Virtual Environment"]
            FastAPIApp["FastAPI App<br/>Port 8000"]
            TrainedModel["Trained Model<br/>sentiment_model.pkl"]
        end

        Tools["Tools:<br/>- pyenv Python 3.12.3<br/>- uv package manager<br/>- Jupyter notebooks"]
    end

    VirtualEnv -.->|Uses| Tools
```

### Kubernetes Deployment (Minikube)

```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    subgraph MinikubeCluster["Minikube Cluster"]
        subgraph SeldonNS["Namespace: seldon"]
            subgraph FastAPIDeploy["FastAPI Deployment"]
                UIPod["Pod: sentiment-ui<br/>Container: fastapi<br/>Port: 8000<br/>Image: sentiment-ui:latest"]
                UISvc["Service: sentiment-ui<br/>NodePort: 30080"]
                UIPod --> UISvc
            end

            subgraph SeldonDeploy["Seldon Deployment"]
                SeldonDeployment["SeldonDeployment:<br/>sentiment-classifier"]
                ClassifierPod["Pod: classifier<br/>Container: classifier<br/>Port: 9000<br/>Image: sentiment-classifier:latest<br/>Volume: /mnt/models"]
                ClassifierSvc["Service:<br/>sentiment-classifier-default"]

                SeldonDeployment --> ClassifierPod
                ClassifierPod --> ClassifierSvc
            end

            UISvc -->|HTTP| ClassifierSvc
        end

        subgraph SeldonSystem["Namespace: seldon-system"]
            Operator["Seldon Core Operator<br/>Controller Manager"]
        end

        Operator -.->|Manages| SeldonDeploy
    end
```

## Data Flow

### Training Pipeline

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart TD
    GenScript["Data Generation Script<br/>python src/generate_data.py"]
    RawData["Raw Data<br/>data/raw/<br/>- sentiment_data.csv<br/>- sentiment_data.json"]
    TrainScript["Training Script<br/>python src/train_model.py<br/><br/>Steps:<br/>1. Load data<br/>2. Split train/test<br/>3. Create pipeline<br/>4. Train model<br/>5. Evaluate<br/>6. Save model"]
    TrainedModel["Trained Model<br/>models/<br/>sentiment_model.pkl"]

    GenScript -->|Generates 1000 samples| RawData
    RawData -->|Read by| TrainScript
    TrainScript -->|Saves to| TrainedModel
```

### Inference Pipeline

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart TD
    UserInput["User Input<br/>'Text...'"]
    FastAPIEndpoint["FastAPI Endpoint<br/>POST /analyze<br/><br/>1. Receive text<br/>2. Format request<br/>3. Call Seldon API"]
    SeldonServer["Seldon Model Server<br/><br/>1. Receive request<br/>2. Extract text<br/>3. Call predict()"]
    MLPipeline["ML Pipeline<br/><br/>1. TF-IDF transform<br/>2. Logistic regression<br/>3. Return prediction"]
    Response["Response<br/>{<br/>  'sentiment': 'positive',<br/>  'text': '...'<br/>}"]
    FastAPIResponse["FastAPI Response<br/><br/>Render HTML with result"]
    UserSees["User sees<br/>😊 Positive"]

    UserInput -->|HTTP POST| FastAPIEndpoint
    FastAPIEndpoint -->|REST API| SeldonServer
    SeldonServer -->|Load model & predict| MLPipeline
    MLPipeline -->|Prediction| Response
    Response -->|JSON response| FastAPIResponse
    FastAPIResponse -->|HTML| UserSees
```

## Component Details

### FastAPI Application

**File:** `src/app.py`

**Responsibilities:**
- Serve web UI
- Handle user requests
- Call Seldon API
- Format responses
- Error handling

**Key Functions:**
- `home()` - Render UI
- `analyze_sentiment()` - Handle analysis
- `call_seldon_api()` - Call model server
- `health_check()` - Health endpoint

### Seldon Model Wrapper

**File:** `src/seldon_model.py`

**Responsibilities:**
- Load trained model
- Implement Seldon interface
- Handle predictions
- Manage model lifecycle

**Key Methods:**
- `load()` - Load model from disk
- `predict()` - Make predictions
- `predict_proba()` - Get probabilities
- `health_status()` - Health check

### Training Script

**File:** `src/train_model.py`

**Responsibilities:**
- Load training data
- Create ML pipeline
- Train model
- Evaluate performance
- Save model

**Pipeline:**
1. TF-IDF Vectorizer
2. Logistic Regression

## Technology Stack

### Development
- **Python:** 3.12.3+
- **Package Manager:** uv
- **Version Manager:** pyenv
- **Notebooks:** Jupyter

### ML Stack
- **Framework:** scikit-learn
- **Data:** pandas, numpy
- **Serialization:** joblib

### Web Stack
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Templates:** Jinja2
- **HTTP Client:** httpx

### Deployment
- **Containers:** Docker
- **Orchestration:** Kubernetes
- **ML Serving:** Seldon Core
- **Local K8s:** Minikube

### DevOps
- **Formatter:** black
- **Linter:** ruff
- **Type Checker:** mypy
- **Testing:** pytest
- **CI/CD:** GitHub Actions

## Resource Requirements

### Local Development
- **CPU:** 2+ cores
- **RAM:** 4+ GB
- **Disk:** 2+ GB

### Minikube Cluster
- **CPU:** 4 cores (recommended)
- **RAM:** 8 GB (recommended)
- **Disk:** 20+ GB

### Container Resources

**FastAPI Container:**
- Requests: 250m CPU, 256Mi RAM
- Limits: 500m CPU, 512Mi RAM

**Seldon Model Container:**
- Requests: 500m CPU, 512Mi RAM
- Limits: 1000m CPU, 1Gi RAM

## Scaling Considerations

### Horizontal Scaling

**FastAPI UI:**
```bash
kubectl scale deployment sentiment-ui -n seldon --replicas=3
```

**Seldon Model:**
Edit `k8s/seldon-deployment.yaml`:
```yaml
replicas: 3
```

### Performance

**Expected:**
- Request latency: < 100ms
- Throughput: 100+ req/sec
- Model size: < 10MB

**Optimization:**
- Model caching
- Connection pooling
- Load balancing
- Resource limits

## Security

### Best Practices Implemented
- ✅ Environment variables for config
- ✅ No hardcoded secrets
- ✅ Resource limits set
- ✅ Health checks enabled
- ✅ Non-root containers
- ✅ Read-only file systems (where applicable)

### Future Enhancements
- [ ] Authentication/Authorization
- [ ] Rate limiting
- [ ] TLS/SSL encryption
- [ ] Network policies
- [ ] Secret management
- [ ] RBAC policies

## Monitoring & Observability

### Current Implementation
- Health check endpoints
- Container logs
- Resource metrics

### Recommended Additions
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Distributed tracing
- [ ] Log aggregation (ELK stack)
- [ ] Model performance monitoring
- [ ] Alerting (PagerDuty, Slack)

---

**For more details, see:**
- README.md - General documentation
- QUICKSTART.md - Getting started guide
- PROJECT_SUMMARY.md - Project overview
