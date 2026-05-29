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
- Optional structured metadata stored as PostgreSQL `JSONB`
- Alembic migration workflow for the log schema
- Integration tests with dependency overrides, a separate test database, guarded reset, and Alembic-based schema setup

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

Status: Complete for current scope

Goals:

- Containerize the full stack
- Separate development and production-like runtime behavior
- Add operational health surfaces to both application services

Key outcomes:

- Shared `docker-compose.yml` plus `docker-compose.dev.yml` and `docker-compose.prod.yml`
- Backend readiness and liveness endpoints
- Backend container healthcheck
- Frontend same-origin API routing through Next rewrites
- Frontend multi-stage Docker image
- Frontend `/health` route and container healthcheck
- Production-like Compose path with a single public frontend entrypoint

Production follow-ups:

- Additional container hardening
- Clearer platform documentation
- More explicit deployment-oriented configuration boundaries

## Phase 4 - Kubernetes Deployment

Status: Complete for current local/dev scope

Goals:

- Translate the container model into Kubernetes resources
- Introduce Services, Deployments, and ingress-level routing

Key outcomes so far:

- Local Docker Desktop Kubernetes deployment for frontend, log-service, and Postgres
- Kustomize base plus dev/prod overlay structure
- ClusterIP Services for internal service discovery
- Readiness and liveness probes for frontend and log-service
- Resource requests and limits for all current workloads
- Postgres PVC for local Kubernetes storage
- Dev overlay with local Docker Desktop image tags
- Prod overlay with production-intent GHCR image names and placeholder release tags
- Local Ingress for `http://cloud-observability.local`
- Log-service schema creation moved out of application startup and into Alembic migrations
- Alembic migration files moved to `services/log-service/migrations/`

Next likely improvements:

- Move raw committed Secrets to a safer secret workflow
- Replace placeholder production image tags with immutable release tags
- Revisit Postgres as managed infrastructure or a StatefulSet
- Add Kubernetes/CI migration execution workflow for deployment automation
- Add namespaces, RBAC, NetworkPolicies, TLS, production ingress/cert management, and container hardening

## Phase 5 - Database Migration Deployment Strategy

Status: Planned for Kubernetes/CI

Goals:

- Run database migrations as a controlled deployment step
- Avoid app pods mutating schema during startup
- Ensure app code and schema migrations come from the same release artifact

Planned shape:

- Build and push the `log-service` image with an immutable release tag
- Run a Kubernetes migration Job using the same image tag
- Inject `DATABASE_URL` from the `log-service-db` Secret
- Stop the rollout if the migration Job fails
- Roll out the `log-service` Deployment only after migrations succeed
- Use release-specific Job names or CI cleanup because Kubernetes Jobs are run-to-completion resources

## Phase 6 - Platform Observability

Status: Planned

Goals:

- Add self-observability to the platform
- Monitor the platform with metrics and dashboards

Potential scope:

- Structured service logs
- Request logging with method, path, status, duration, and request ID
- Prometheus metrics
- Grafana dashboards
- Service monitoring and alerting
- OpenTelemetry tracing once multiple services justify it

## Phase 7 - CI/CD and Quality Automation

Status: Planned

Goals:

- Automate validation, image builds, and deployment
- Add repeatable quality checks across backend and frontend

Potential scope:

- Backend tests and future linting/formatting with Ruff or Black
- Frontend linting and formatting with ESLint and Prettier
- Container image builds and scans
- Push immutable images to GHCR
- Apply migrations and roll out Kubernetes manifests
- Verify rollout health

## Phase 8 - Platform Expansion

Status: Planned

Goals:

- Expand beyond the initial log-service-focused architecture
- Introduce additional internal services when the platform design justifies them

Potential scope:

- API gateway
- Metrics service
- Alerts or rules service
- Shared platform-level contracts
