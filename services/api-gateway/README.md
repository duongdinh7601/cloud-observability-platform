# API Gateway Service

The API Gateway Service is a **backend service** in the Cloud Observability Platform.  
It acts as a single entry point for frontend requests and routes them to the appropriate backend services, such as the Log Service.

---

## Responsibilities

- Route incoming HTTP requests from the frontend to the correct backend service  
- Handle request validation and basic authentication (optional)  
- Aggregate responses from multiple backend services if needed  
- Provide a single, consistent API endpoint for the frontend  

---

## Features

- Request routing to backend services (Log Service, Metrics Service, Alerts Service)  
- Optional request logging for monitoring traffic  
- Handles errors and returns standardized responses to the frontend  

---

## Tech Stack

- **Python + FastAPI** for backend API  
- **Uvicorn** as ASGI server  
- **HTTPX** or `requests` library for service-to-service communication  

---

## Folder Structure

api-gateway/

├── app/ # Application source code

│ ├── main.py # Entry point

│ ├── routes/ # API routes

│ ├── services/ # Service clients (e.g., Log Service client)

│ └── utils/ # Utility functions

├── tests/ # Unit and integration tests

├── Dockerfile # Optional Dockerfile for containerization

└── README.md

---

## Setup Instructions

1. Navigate to the API Gateway folder:
```bash
cd services/api-gateway
```
2. Create virtual environement (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate # on windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start the development server:
```bash
uvicorn app.main:app --reload
```

---

## Notes

- The API Gateway is **modular and scalable**, allowing new services to be added easily
- Supports **frontend-backend separation**, enabling independent scaling of services
- Designed for **future containerization and deployment to Kubernetes**
