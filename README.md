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

# Warm Start (Subsequent Request)
![Cloud Run Warm Start](screenshots/cloudrun-warm-start.png)
Warm request latency: 112 milliseconds (subsequent requests)

The cold start latency reflects container startup, image initialization, and application boot time. 
The warm requests benefit from an already running container and in-memory model, resulting in significantly lower latency.



# Step 7: Cloud Functions Deployment Attempt
A deployment attempt was made using Google Cloud Functions (Gen 2).  
However, deployment failed due to organization-level IAM restrictions on the
Cloud Build service account associated with an NIH-managed Google Cloud project.

The error indicates missing permissions for:
`roles/cloudbuild.builds.builder`

This restriction is enforced at the organizational level and cannot be modified
by project users. This behavior is expected in enterprise and government-managed
Google Cloud environments.

![Cloud Function IAM Error](screenshots/cloud-function-permission-error.png)

# Benchmarking Cold Start vs Warm Latency (Cloud Functions)
Cloud Functions cold and warm latency could not be benchmarked because deployment was blocked by organization level IAM restrictions on the Cloud Build service account in this NIH managed Google Cloud project.

## Comparative Analysis: Cloud Run vs Cloud Functions

This project evaluated Google Cloud Run and Google Cloud Functions as serverless platforms for deploying a machine learning inference service, with emphasis on deployment feasibility, runtime behavior, and performance characteristics.

Cloud Run provided greater flexibility and control by allowing the application and model to be packaged into a Docker container. This made dependency management, environment reproducibility, and eager model loading straightforward. Cold start latency for Cloud Run was observed to be relatively high (~8–9 seconds) due to container startup and model initialization; however, warm requests completed in approximately 110 milliseconds, demonstrating efficient reuse of the running container and in-memory model. This behavior is well suited for production ML inference workloads where consistent, low latency performance is required after initialization.

Cloud Functions follows a more abstracted, function based execution model that relies on managed build pipelines and service accounts. In this project, deployment of a Cloud Functions (Gen 2) service was blocked by organization-level IAM restrictions on the Cloud Build service account in an NIH managed Google Cloud environment. As a result, cold and warm latency measurements for Cloud Functions could not be collected. This limitation highlights a practical challenge of using Cloud Functions in enterprise or government managed environments, where IAM constraints can restrict deployment flexibility.

Overall, Cloud Run proved to be the more suitable platform for this use case, offering greater operational control, predictable runtime behavior, and strong warm-start performance for machine learning inference. While Cloud Functions may be appropriate for lightweight, event-driven workloads, Cloud Run is better aligned with the requirements of containerized ML services in secure, production-oriented environments.

# Notes on IAM Restrictions
Public unauthenticated invocation could not be enabled due to organizational IAM restrictions associated with an NIH-managed Google Cloud account. Authenticated invocation was used instead, which is a standard approach in secure production environments.

# Conclusion
This milestone demonstrates a complete ML serving lifecycle:
-Model training and serialization
-API-based inference service
-Docker containerization
-Artifact Registry image management
-Cloud Run deployment
-Secure HTTPS verification

The deployed service is production-ready and scalable using Google Cloud Run.