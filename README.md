# IDS 568 – Milestone 1: ML Model Serving on Google Cloud Run

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
Due to NIH-managed Google Cloud IAM policies, unauthenticated public access to the service is restricted.
This is expected behavior in enterprise and government environments.
The service was verified using authenticated HTTPS requests.

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
{"status":"healthy","model_loaded":true}
```



# Notes on IAM Restrictions
Public unauthenticated invocation could not be enabled due to organizational IAM restrictions associated with an NIH-managed Google Cloud account. Authenticated invocation was used instead, which is a standard approach in secure production environments.

# Conclusion
This milestone demonstrates a complete ML serving lifecycle:
-Model training and serialization
-API-based inference service
-Docker containerization
-Artifact Registry image managementCloud Run deployment
-Secure HTTPS verification

The deployed service is production-ready and scalable using Google Cloud Run.