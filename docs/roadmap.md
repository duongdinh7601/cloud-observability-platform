# Project Roadmap

This roadmap tracks the platform by phases instead of calendar weeks so progress can stay realistic and sustainable.

## Phase 1 - Backend Log Service

Status: Complete

Goals:

- Build the FastAPI log service
- Model log data with Pydantic and SQLAlchemy
- Support log ingestion and retrieval

Key outcomes:

- `POST /logs`
- `GET /logs`
- Cursor pagination with stable ordering
- Filtering by level, service, and time range
- Integration tests with dependency overrides and a separate test database

## Phase 2 - Frontend Logs Dashboard

Status: Complete

Goals:

- Build a production-minded logs dashboard in Next.js
- Support filtering, pagination, and resilient loading states

Key outcomes:

- Logs dashboard with App Router
- TanStack Query data fetching
- URL-synced filters
- Debounced search
- Empty, loading, and error states

## Phase 3 - Container Architecture and Production-Like Runtime

Status: In Progress

Goals:

- Containerize the full stack
- Separate development and production-like runtime behavior
- Add operational health surfaces to both application services

Key outcomes so far:

- Shared `docker-compose.yml` plus `docker-compose.dev.yml` and `docker-compose.prod.yml`
- Backend readiness and liveness endpoints
- Backend container healthcheck
- Frontend same-origin API routing through Next rewrites
- Frontend multi-stage Docker image
- Frontend `/health` route and container healthcheck
- Production-like Compose path with a single public frontend entrypoint

Next likely improvements:

- Additional container hardening
- Clearer platform documentation
- More explicit deployment-oriented configuration boundaries

## Phase 4 - Kubernetes Deployment

Status: Planned

Goals:

- Translate the container model into Kubernetes resources
- Introduce Services, Deployments, and ingress-level routing

Potential scope:

- Deploy frontend and log-service to a cluster
- Add ConfigMaps and Secrets
- Explore scaling behavior and health probe mapping

## Phase 5 - Platform Observability

Status: Planned

Goals:

- Add self-observability to the platform
- Monitor the platform with metrics and dashboards

Potential scope:

- Prometheus metrics
- Grafana dashboards
- Service monitoring and alerting

## Phase 6 - Platform Expansion

Status: Planned

Goals:

- Expand beyond the initial log-service-focused architecture
- Introduce additional internal services when the platform design justifies them

Potential scope:

- API gateway
- Metrics service
- Alerts or rules service
- Shared platform-level contracts
