# Seldon Core v1 Deployment Guide

This guide covers deploying the sentiment analyzer using **Seldon Core v1** on Kubernetes.

> **⚠️ Educational Purpose**: The sentiment analysis model in this project is intentionally naive (Logistic Regression with TF-IDF) to keep the focus on Seldon Core v1 concepts and deployment patterns rather than complex NLP.

## Prerequisites

- Kubernetes cluster (minikube recommended for local development)
- kubectl configured
- Docker
- Trained model file (`models/sentiment_model.pkl`)

## Architecture

Seldon Core v1 deployment architecture:

```
REST API Request
    ↓
Seldon Service Orchestrator (Ambassador/Istio)
    ↓
SeldonDeployment CRD
    ↓
Service Orchestrator Engine (svc-orchestrator container)
    ↓
Model Container (sentiment-seldon:latest)
    ↓
SentimentClassifier Python Wrapper
    ↓
Scikit-learn Model
```

## Quick Start

### 1. Train the Model

```bash
make data
make train
```

This creates `models/sentiment_model.pkl`.

### 2. Deploy to Kubernetes with Seldon

```bash
make k8s-deploy-seldon
```

This script will:
- Start minikube (if not running)
- Build the Docker image in minikube
- Copy the model file to minikube
- Install Seldon Core v1.17.1 (if not installed)
- Deploy the SeldonDeployment CRD

### 3. Access the Model

**Port forward to the service:**
```bash
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000
```

**Test with curl:**
```bash
# Single prediction
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["This is absolutely amazing!"]}}'

# Batch prediction
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{"data":{"ndarray":["Great product!", "Not good", "It works fine"]}}'
```

**Or use the test script:**
```bash
# In terminal 1 (keep running)
kubectl port-forward svc/sentiment-classifier-default -n seldon 8080:8000

# In terminal 2
./scripts/test-seldon.sh
```

## Understanding the SeldonDeployment

The [k8s/seldon-deployment.yaml](../k8s/seldon-deployment.yaml) defines:

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: sentiment-classifier
  namespace: seldon
spec:
  predictors:
  - name: default
    graph:
      name: classifier
      type: MODEL
      endpoint:
        type: REST
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          image: sentiment-seldon:latest
```

**Key components:**
- **SeldonDeployment**: Custom Resource Definition (CRD) for ML deployments
- **Predictor**: Defines the inference graph (can have multiple for A/B testing)
- **Graph**: Defines the component topology (MODEL, TRANSFORMER, ROUTER, COMBINER)
- **ComponentSpecs**: Kubernetes pod specifications for containers

## Seldon Core v1 Components

When you deploy a SeldonDeployment, Seldon creates:

1. **Deployment**: `sentiment-classifier-default-0-classifier`
   - Your model container
   - Service orchestrator sidecar container

2. **Services**:
   - `sentiment-classifier-default`: Main service endpoint
   - `sentiment-classifier-default-classifier`: Model container service

3. **Virtual Service** (if using Istio):
   - Traffic routing configuration

## Monitoring and Debugging

### Check Status

```bash
# SeldonDeployment status
kubectl get seldondeployments -n seldon

# Pods
kubectl get pods -n seldon -l seldon-deployment-id=sentiment-classifier

# Services
kubectl get svc -n seldon
```

### View Logs

```bash
# Model container logs
kubectl logs -f -l seldon-deployment-id=sentiment-classifier -c classifier -n seldon

# Service orchestrator logs
kubectl logs -f -l seldon-deployment-id=sentiment-classifier -c seldon-container-engine -n seldon
```

### Describe Resources

```bash
# SeldonDeployment details
kubectl describe seldondeployment sentiment-classifier -n seldon

# Pod details
kubectl describe pod -l seldon-deployment-id=sentiment-classifier -n seldon
```

## Advanced Features

### A/B Testing

Deploy multiple predictors with traffic splitting:

```yaml
spec:
  predictors:
  - name: model-v1
    replicas: 1
    traffic: 90
    graph:
      name: classifier-v1
      type: MODEL
  - name: model-v2
    replicas: 1
    traffic: 10
    graph:
      name: classifier-v2
      type: MODEL
```

### Autoscaling

Add HPA (Horizontal Pod Autoscaler):

```yaml
spec:
  predictors:
  - name: default
    replicas: 1
    componentSpecs:
    - spec:
        containers:
        - name: classifier
          resources:
            requests:
              cpu: 200m
    hpaSpec:
      minReplicas: 1
      maxReplicas: 5
      metrics:
      - type: Resource
        resource:
          name: cpu
          targetAverageUtilization: 70
```

### Custom Transformer

Add preprocessing with a transformer:

```yaml
spec:
  predictors:
  - name: default
    graph:
      name: transformer
      type: TRANSFORMER
      endpoint:
        type: REST
      children:
      - name: classifier
        type: MODEL
        endpoint:
          type: REST
```

## Troubleshooting

### Pods Not Starting

```bash
# Check events
kubectl get events -n seldon --sort-by='.lastTimestamp'

# Check pod status
kubectl describe pod <pod-name> -n seldon
```

### Model File Not Found

```bash
# Verify model file in minikube
minikube ssh "ls -la /tmp/models/"

# Recopy model file
minikube cp models/sentiment_model.pkl /tmp/models/sentiment_model.pkl

# Restart deployment
kubectl rollout restart seldondeployment/sentiment-classifier -n seldon
```

### Seldon Operator Not Running

```bash
# Check operator status
kubectl get pods -n seldon-system

# View operator logs
kubectl logs -f deployment/seldon-controller-manager -n seldon-system
```

### Image Pull Errors

```bash
# Rebuild in minikube
eval $(minikube docker-env)
docker build -t sentiment-seldon:latest -f Dockerfile.seldon .

# Verify image exists
minikube ssh docker images | grep sentiment-seldon
```

## Clean Up

```bash
# Delete SeldonDeployment
kubectl delete seldondeployment sentiment-classifier -n seldon

# Or delete entire namespace
kubectl delete namespace seldon

# Stop minikube
minikube stop
```

## API Reference

### Prediction Endpoint

**URL**: `http://<service>/api/v1.0/predictions`

**Request Format**:
```json
{
  "data": {
    "ndarray": ["text to classify", "another text"]
  }
}
```

**Response Format**:
```json
{
  "data": {
    "names": [],
    "ndarray": ["positive", "negative"]
  },
  "meta": {}
}
```

### Prediction with Probabilities

Use `/api/v1.0/predictions` with the model's `predict_proba` method by adding metadata:

```bash
curl -X POST http://localhost:8080/api/v1.0/predictions \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {"ndarray": ["This is great!"]},
    "meta": {"method": "predict_proba"}
  }'
```

## Next Steps

- Read [blog.md](../blog.md) for detailed Seldon Core v1 architecture
- Explore [examples](https://github.com/SeldonIO/seldon-core/tree/v1.17.1/examples) in Seldon repo
- Review [official docs](https://docs.seldon.io/projects/seldon-core/en/v1.17.1/)
- Try implementing custom transformers or routers
- Experiment with multi-model ensembles
