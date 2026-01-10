# Infrastructure

The `infra/` folder contains all the **infrastructure configurations** for the Cloud Observability Platform.  
This includes Docker for local development and Kubernetes manifests for production-like deployment.

---

## Responsibilities

- Provide containerization for backend and frontend services  
- Enable local development with Docker Compose  
- Define Kubernetes manifests for scaling and deployment in cloud environments  
- Support reproducible and modular infrastructure setup  

---

## Folder Structure

infra/

├── docker/ # Docker and docker-compose files for local development

│ ├── Dockerfile # Base Dockerfile for services

│ └── docker-compose.yml # Local development environment

├── kubernetes/ # Kubernetes manifests for services

│ ├── log-service.yaml # Deployment & Service for Log Service

│ ├── api-gateway.yaml # Deployment & Service for API Gateway

│ └── frontend.yaml # Deployment & Service for React frontend

└── README.md

---

## Docker (Local Development)

1. Navigate to the `docker` folder:  
```bash
cd infra/docker
```
2. Build Docker images for all services:
```bash
docker-compose build
```
3. Start all services:
```bash
docker-compose up
```
Services will run locally and communicate through the Docker netowrk.

---

## Kubernetes (Production/Cloud Deployment)

1. Ensure you have access to a Kubernetes cluster (local: Minikube, kind; or cloud: EKS, GKE, AKS)
2. Apply the manifests for each service:
```bash
kubectl apply -f infra/kubernetes/log-service.yaml
kubectl apply -f infra/kubernetes/api-gateway.yaml
kubectl apply -f infra/kubernetes/frontend.yaml
```
3. Check the status of pods and services:
```bash
kubectl get pods
kubectl get svc
```

## Notes

- Docker Compose is for **local development** only
- Kubernetes manifests are designed for **scalable, production-like deployments**
- The infrastructure is **modular**, allowing for new services (metrics, alerts) to be added easily
- Environment variables and secrets should be managed securely using `.env` files or Kubernetes Secrets
