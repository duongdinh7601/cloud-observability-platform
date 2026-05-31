# Project Architecture

The Cloud Observability Platform is a full-stack, cloud-native project designed for log ingestion, storage, and visualization. The architecture emphasizes modularity, operational visibility, and production-shaped deployment practices.

---

## Components

| Component        | Purpose                                                                 |
|-----------------|-------------------------------------------------------------------------|
| `frontend/`      | Next.js dashboard for viewing and filtering logs                        |
| `services/`      | Backend services, including the active Log Service and planned API Gateway |
| `infra/`         | Infrastructure configuration, including Kubernetes base manifests and overlays |
| `docs/`          | Documentation and design artifacts                                      |
| `scripts/`       | Utility scripts (DB setup, seed data, automation)                       |

---

## Component Interactions

1. **Frontend**
   - Serves the dashboard as the public-facing app surface
   - Uses same-origin `/api/...` requests from the browser
   - Rewrites API requests internally to the Log Service

2. **Backend Services**
   - `Log Service` receives log entries, validates requests, stores logs and optional metadata, and returns cursor-paginated results
   - `Log Service` emits structured JSON operational logs for non-health HTTP requests and uses `X-Request-ID` for request correlation
   - `API Gateway` is planned for a future phase when the platform has enough services to justify a dedicated backend boundary

3. **Database**
   - PostgreSQL stores logs
   - Alembic owns schema migrations; application startup does not create or mutate tables
   - The current Kubernetes path runs Postgres in-cluster for learning; a managed database remains a production follow-up

4. **Infrastructure**
   - Docker Compose supports local and production-like container workflows
   - Kubernetes runs the platform with Deployments, Services, Secrets, health probes, resource requests/limits, and Postgres storage
   - Kustomize separates shared base manifests from environment-specific overlays
   - Future CI/CD should run database migrations as a controlled step before rolling out new app pods

---

## Runtime Request Path

```text
Browser
-> Next.js frontend
-> /api rewrite to log-service
-> FastAPI Log Service
-> PostgreSQL
```

In Kubernetes, Services provide the stable internal names:

```text
frontend:3000
log-service:8000
postgres:5432
```

## Notes

- Each application service is independently containerized.
- Modular design allows future services such as metrics, alerts, or a gateway to be added deliberately.
- The project favors production-shaped decisions while keeping early implementations understandable.
- The observability phase has started with structured `log-service` request logs and request IDs; next steps include metrics, dashboards, alerts, centralized logging configuration, and eventually tracing.
