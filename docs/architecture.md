# Project Architecture

The Cloud Observability Platform is a **full-stack, cloud-native project** designed for log ingestion, storage, and visualization. The architecture emphasizes modularity, scalability, and production-style practices.

---

## Components

| Component        | Purpose                                                                 |
|-----------------|-------------------------------------------------------------------------|
| `frontend/`      | React dashboard for viewing logs and metrics                            |
| `services/`      | Backend services, including API Gateway and Log Service                 |
| `infra/`         | Infrastructure configurations (Docker for local dev, Kubernetes later) |
| `docs/`          | Documentation and design artifacts                                      |
| `scripts/`       | Utility scripts (DB setup, seed data, automation)                       |

---

## Component Interactions

1. **Frontend**  
   - Sends HTTP requests to the backend API (API Gateway / Log Service)  
   - Receives JSON responses for logs or metrics

2. **Backend Services**  
   - `Log Service` receives log entries, validates, and stores them in PostgreSQL  
   - `API Gateway` routes requests between frontend and backend services

3. **Database**  
   - PostgreSQL stores logs  
   - Indexed for efficient querying

4. **Infrastructure**  
   - Docker handles local development  
   - Kubernetes handles production-like deployment (future)

---

## Notes

- Each service is **independently deployable**  
- Modular design allows easy addition of new services (metrics, alerts)  
- Designed to mirror **real-world production systems**
