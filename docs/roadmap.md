# Project Roadmap

This document outlines the **development and learning plan** for the Cloud Observability Platform.

---

## Phase 1: Week 1
- Design the Log Service (API endpoints, data model)
- Create folder structure and documentation

## Phase 2: Week 2
- Implement `POST /logs` endpoint in FastAPI
- Connect to PostgreSQL for log storage
- Validate incoming log entries

## Phase 3: Week 3
- Implement `GET /logs` endpoint
- Add filtering (time range, severity, service_name)
- Add pagination for query results

## Phase 4: Week 4
- Build React frontend dashboard
- Display log entries with tables and charts
- Connect frontend to backend API

## Phase 5: Week 5
- Containerize backend and frontend with Docker
- Use docker-compose for local development

## Phase 6: Week 6
- Deploy services to Kubernetes (Pods, Services, ConfigMaps)
- Test scaling and service discovery

## Phase 7: Week 7+
- Add metrics and alerting services
- Implement Prometheus + Grafana monitoring
- Continuous improvement and performance tuning
