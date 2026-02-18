# Milestone 2 – Deployment Runbook



## 1. Service Overview

This project is a Dockerized Python Flask ML API.
The application exposes:

- `/health` – health check endpoint
- `/predict` – prediction endpoint

The container image is automatically built and pushed via GitHub Actions CI/CD.

Image location:
ghcr.io/aoki3-ctrl/milestone2-app:v1.0.0



## 2. Prerequisites

Before running the service, ensure you have:

- Docker installed
- Internet access to pull the container image
- Port 5000 available locally

Verify Docker:

```bash
docker --version
```


## 3. Pull the Container Image

```
docker pull ghcr.io/aoki3-ctrl/milestone2-app:v1.0.0
```


## 4. Run the Container

```
docker run -p 5000:5000 ghcr.io/aoki3-ctrl/milestone2-app:v1.0.0
```
The service will start on:

http://localhost:5000

## 5. Validate Service Health

Health check:
```
curl http://localhost:5000/health
```
Expected response:


{"status":"healthy"}
Test prediction endpoint (example):

```
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"feature1": 1, "feature2": 2}'
```


## 6. CI/CD & Versioning Strategy

The GitHub Actions pipeline performs:

Run unit tests using pytest

Build multi-stage Docker image

Tag image using semantic versioning (vMAJOR.MINOR.PATCH)

Push image to GitHub Container Registry (GHCR)

Workflow location:
.github/workflows/build.yml

Current version:
v1.0.0


