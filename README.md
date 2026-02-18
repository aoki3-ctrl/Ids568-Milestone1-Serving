# IDS 568 – Milestone 2: CI/CD Dockerized ML Service

![CI/CD](https://github.com/aoki3-ctrl/Ids568-Milestone1-Serving/actions/workflows/build.yml/badge.svg)



## Service Overview

This milestone implements a production-style CI/CD pipeline for a Dockerized Python Flask ML API.

The service exposes:

- `/health` – health check endpoint
- `/predict` – ML inference endpoint

The container image is automatically:
- Tested with `pytest`
- Built using a multi-stage Dockerfile
- Tagged using semantic versioning (`vMAJOR.MINOR.PATCH`)
- Pushed to GitHub Container Registry (GHCR)



## Container Image

Registry:

ghcr.io/aoki3-ctrl/milestone2-app:v1.0.0

##  Quick Start

### 1. Pull Image

```
docker pull ghcr.io/aoki3-ctrl/milestone2-app:v1.0.0
```

### 2️. Run Container
```
docker run -p 5000:5000 ghcr.io/aoki3-ctrl/milestone2-app:v1.0.0
```
Service will start at:

http://localhost:5000


### 3️. Health Check
```
curl http://localhost:5000/health
```
Expected response:
```json
{"status":"healthy"}
```


### 4️. Example Prediction Request
```
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"feature1": 1, "feature2": 2}'
```
## CI/CD Pipeline
Workflow location:
.github/workflows/build.yml

Pipeline stages:
- Run unit tests (pytest)
- Build optimized multi-stage Docker image (builder + runtime stage)
- Tag image using semantic versioning
- Push image to GHCR

## Versioning Strategy
Images follow semantic versioning:

vMAJOR.MINOR.PATCH
Current release:

v1.0.0

---

# Below: IDS 568 – Milestone 1: ML Model Serving on Google Cloud Run

# Overview
This project demonstrates end-to-end deployment of a machine learning inference service using FastAPI, Docker, Google Artifact Registry, and Google Cloud Run.

A trained Iris classification model is containerized and deployed as a scalable HTTPS service. The project follows best practices for ML serving, containerization, and cloud-native deployment.

# Technologies Used
- Python 3
- FastAPI
- Docker
- Google Cloud Run
- Google Artifact Registry
- Google Cloud CLI (`gcloud`)
- scikit-learn
- Google Cloud Functions (Gen2)


# Project Structure
- app/
- main.py #FastAPI inference service
- model.pkl #Trained ML model artifact
- requirements.txt #Python dependencies
- Dockerfile #Container build instructions
- screenshots/ #Deployment evidence
- README.md



# Step 1: Model Training
An Iris classification model was trained locally and serialized into `model.pkl`.  
The model artifact is loaded once at application startup (eager loading) to minimize inference latency.


# Step 2: FastAPI Inference Service
A FastAPI application was implemented with:
- Pydantic request validation
- `/health` endpoint for monitoring
- `/predict` endpoint for inference
- Proper model loading lifecycle

The service was tested locally before containerization.


# Step 3: Containerization & Artifact Registry
The application was containerized using Docker and pushed to Google Artifact Registry.

## Artifact Registry Image
![Artifact Registry Image](screenshots/artifact-registry-image.png)

This screenshot confirms that the `iris-api` Docker image was successfully stored in the
`ids568-mlops-images` repository in `us-central1`.


# Step 4: Cloud Run Deployment
The container image was deployed to Google Cloud Run using the Google Cloud CLI.

## Cloud Run CLI Deployment Image
![Cloud Run CLI Deployment](screenshots/cloudrun-deploy-terminal.png)

The deployment output shows that the service revision was successfully deployed and is serving traffic.

## Cloud Run Service
![Cloud Run Service](screenshots/cloudrun-service.png)

This screenshot shows the Cloud Run service actively serving traffic over HTTPS.


# Step 5: Service Verification (Authenticated Access)
The service was verified using authenticated HTTPS requests:

## Authenticated Health Check Image
![Authenticated Health Check](screenshots/cloudrun-healthcheck.png)

Example command used:
```bash
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
https://iris-api-340394144067.us-central1.run.app/health
```

Response:
```json
{"status":"healthy","model_loaded":true}

```

# Step 6: Benchmarking Cold Start vs Warm Latency (Cloud Run)

Cold start and warm request latency were measured using authenticated requests to the /health endpoint.

Command used:
```bash
time curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
https://iris-api-340394144067.us-central1.run.app/health
```
#Observed results:
# Cold Start (First Request)
![Cloud Run Cold Start](screenshots/cloudrun-cold-start.png)
Cold start latency: 8.9 seconds (first request after idle)
This includes:
- Container startup
- Image initialization
- FastAPI boot
- Model loading

# Warm Start (Subsequent Request)
![Cloud Run Warm Start](screenshots/cloudrun-warm-start.png)
Warm request latency: 112 milliseconds (subsequent requests)

The cold start latency reflects container startup, image initialization, and application boot time. 
The warm requests benefit from an already running container and in-memory model, resulting in significantly lower latency.



# Step 7: Cloud Functions Deployment Attempt
A Google Cloud Function (Gen 2) was implemented using the same Iris model prediction logic and deployed in a personal Google Cloud project.
Deployment command:
gcloud functions deploy iris-function \
--gen2 \
--runtime python311 \
--region us-central1 \
--entry-point predict \
--trigger-http \
--allow-unauthenticated

The function deployed successfully and is active:
Function URL:
https://us-central1-ids568-milestone1-personal.cloudfunctions.net/iris-function

The deployment automatically created an underlying Cloud Run service (Gen 2 architecture). The function is publicly accessible and serves HTTP requests.

# Benchmarking Cold Start vs Warm Latency (Cloud Functions)
Cold and warm latency were measured using the time command.
Command used:
time curl https://us-central1-ids568-milestone1-personal.cloudfunctions.net/iris-function

Cold Start (First Request After Idle)
Cold start latency: 3.36 seconds
Cold start includes:
- Container startup
- Runtime initialization
- Model loading
- Service activation

Warm Request (Subsequent Request)
Warm start latency: 0.105 seconds
Warm requests benefit from:
- Reused container instance
- In-memory model
- No rebuild or cold initialization

## Comparative Analysis: Cloud Run vs Cloud Functions

This project evaluated both Google Cloud Run and Google Cloud Functions (Gen 2) for serving a machine learning inference workload using the same Iris classification model.
Cold start benchmarking revealed a meaningful difference between the two platforms. Cloud Run exhibited a cold start latency of approximately 8.9 seconds, while Cloud Functions (Gen 2) exhibited a significantly lower cold start latency of approximately 3.36 seconds. The longer cold start for Cloud Run is attributable to full container initialization, FastAPI server boot time, and model loading. In contrast, Cloud Functions deploys a simpler HTTP handler, resulting in reduced initialization overhead.
Warm request performance was nearly identical across both platforms. Cloud Run averaged approximately 0.11 seconds, while Cloud Functions averaged approximately 0.105 seconds. This similarity is expected because Gen 2 Cloud Functions run on Cloud Run infrastructure and reuse active container instances once initialized.
From an architectural standpoint, Cloud Run provides greater flexibility and container-level control, making it well suited for complex ML services requiring custom environments and reproducibility. Cloud Functions offers faster cold starts and simpler deployment for lightweight inference endpoints but provides less direct infrastructure control.
Overall, Cloud Run is better aligned with production-grade, containerized ML services, while Cloud Functions may be preferable for lightweight HTTP-triggered inference workloads where lower cold start latency is desirable.

# Conclusion
This milestone demonstrates a complete ML serving lifecycle:
-Model training and serialization
-API-based inference service
-Docker containerization
-Artifact Registry image management
-Cloud Run deployment
-Secure HTTPS verification

The deployed service is production-ready and scalable using Google Cloud Run.