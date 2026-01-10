# Cloud Observability Platform

A **full-stack, cloud-native observability platform** that demonstrates modern backend and frontend development, containerization, and deployment practices.  

The project is designed for learning and portfolio purposes and includes log ingestion, data storage, and a React frontend for visualization. Future iterations will add monitoring, metrics, and Kubernetes orchestration.

---

## Tech Stack

- **Frontend:** React + TypeScript
- **Backend Services:** Python + FastAPI
- **Database:** PostgreSQL
- **Containerization:** Docker
- **Orchestration (future):** Kubernetes
- **Monitoring (future):** Prometheus + Grafana

---

## Components

| Component        | Purpose                                                                 |
|-----------------|-------------------------------------------------------------------------|
| `frontend/`      | React dashboard for viewing logs and metrics                            |
| `services/`      | Backend services (API gateway, log ingestion, future metrics/alerts)   |
| `infra/`         | Docker and Kubernetes configuration                                     |
| `docs/`          | Architecture, roadmap, and service documentation                        |
| `scripts/`       | Utility scripts for setup or database seeding                           |

---

## Roadmap

1. **Week 1:** Design first backend service (log ingestion)
2. **Week 2:** Implement `POST /logs` and connect to PostgreSQL
3. **Week 3:** Implement `GET /logs` with filters and pagination
4. **Week 4:** Build React frontend dashboard
5. **Week 5:** Containerize services with Docker
6. **Week 6:** Deploy backend to Kubernetes
7. **Week 7+:** Add metrics, alerting, and monitoring
