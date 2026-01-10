# Project Roadmap

This document outlines the **development and learning plan** for the Cloud Observability Platform.

---

## Phase 1: Week 1 – Backend Skeleton

**Goals:**  
- Implement FastAPI skeleton for Log Service  
- Define Pydantic models for request/response  
- Connect to PostgreSQL  
- Implement `POST /logs` endpoint  

**Tasks:**  
- `app/main.py` → FastAPI app, DB connection setup  
- `schemas.py` → LogEntry Pydantic model  
- `routes.py` → Add `POST /logs` route  
- Test endpoint with Postman/curl  

**Learning Focus:** FastAPI, Pydantic, PostgreSQL, REST API basics  

---

## Phase 2: Week 2 – GET Endpoint & Filtering

**Goals:**  
- Implement `GET /logs` endpoint with filters and pagination  

**Tasks:**  
- Add query parameters: `start_time`, `end_time`, `level`, `service_name`, `page`, `limit`  
- Implement database queries  
- Test filtering, pagination, and responses  

**Learning Focus:** SQL queries, API testing, response formatting  

---

## Phase 3: Week 3 – Frontend Setup

**Goals:**  
- Set up React frontend  
- Fetch logs from Log Service  
- Display logs in table with pagination  

**Tasks:**  
- Initialize React project (`frontend/`)  
- Create `LogsTable` component  
- `api.ts` → API service calls to backend  

**Learning Focus:** React, TypeScript, Axios/fetch, table UI  

---

## Phase 4: Week 4 – Frontend Forms & Filters

**Goals:**  
- Add log submission form (`POST /logs`)  
- Add filtering options in frontend  

**Tasks:**  
- `LogForm` component → submit new logs  
- Filters: date range, severity, service  
- Connect filters to `GET /logs`  

**Learning Focus:** React forms, state management, frontend-backend integration  

---

## Phase 5: Week 5 – Docker Containerization

**Goals:**  
- Containerize backend and frontend  
- Enable local dev with Docker Compose  

**Tasks:**  
- Write Dockerfiles for each service  
- Create `docker-compose.yml`  
- Test local containers and networking  

**Learning Focus:** Docker, Docker Compose, multi-service local dev  

---

## Phase 6: Week 6 – API Gateway & Kubernetes

**Goals:**  
- Implement API Gateway routing requests  
- Deploy services to Kubernetes (optional)  

**Tasks:**  
- API Gateway (`services/api-gateway`) → route to Log Service  
- Kubernetes manifests → Pods, Services, ConfigMaps  
- Test scaling and inter-service communication  

**Learning Focus:** FastAPI routing, Kubernetes basics, scaling  

---

## Phase 7: Week 7+ – Monitoring & Expansion

**Goals:**  
- Add Metrics & Alerting services  
- Integrate Prometheus + Grafana  
- Continuous improvement and performance tuning  

**Tasks:**  
- Create new backend services for metrics/alerts  
- Connect to Prometheus/Grafana  
- Performance testing and logging improvements  

**Learning Focus:** Observability, monitoring, alerts, production-grade design

Connect to Prometheus/Grafana

Performance testing and logging improvements

Learning Focus: Observability, monitoring, alerts, production-grade design
