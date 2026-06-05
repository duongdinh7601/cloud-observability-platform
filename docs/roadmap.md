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

Status: In Progress

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

### Phase 6.1 - Structured Operational Logs

Status: Complete for the first `log-service` slice

Goal:

- Make `log-service` emit machine-readable logs about its own runtime behavior.

Completed scope:

- Added FastAPI middleware for request logging
- Emits one JSON log line per non-health request
- Includes method, path, status code, duration, and error context when applicable
- Keeps logs on stdout/stderr so Docker and Kubernetes can collect them
- Skips high-frequency health probe logs to reduce noise

Production follow-ups:

- Standardize JSON log fields across services
- Replace the temporary middleware-local log handler with centralized service-wide JSON logging configuration
- Consider filtering or downgrading noisy browser/CORS paths such as `/favicon.ico` and `OPTIONS`
- Decide later whether the platform should ingest its own operational logs

### Phase 6.2 - Request IDs

Status: Complete for `log-service` handled HTTP responses

Goal:

- Correlate operational logs from the same request.

Completed scope:

- Accept an incoming `X-Request-ID` header when present
- Generate a request ID when one is missing
- Return the request ID in the response headers
- Include the request ID in operational logs

Future scope:

- Pass request IDs through frontend-to-backend calls where appropriate
- Add tests for request ID log/header behavior when logging becomes a stronger service contract
- Decide whether centralized exception handling should attach `X-Request-ID` to unhandled error responses

### Phase 6.3 - Metrics Endpoint

Status: Complete for the first `log-service` slice

Goal:

- Expose aggregate service health signals.

Completed scope:

- Add Prometheus-compatible metrics
- Expose a `/metrics` endpoint
- Track request count
- Track request duration
- Track error count
- Track log ingestion count

Production follow-ups:

- Decide whether to exclude `/metrics` from request logs/request metrics, or filter it in dashboards, if scrape traffic becomes noisy
- Add tests for metrics output and ingestion counter behavior when metrics become a stronger service contract
- Add Kubernetes scrape configuration in the next observability phase

### Phase 6.4 - Kubernetes Metrics Scraping

Status: Complete for local/dev Prometheus

Goal:

- Prepare local Kubernetes to collect service metrics.

Completed scope:

- Added a dev-overlay Prometheus Deployment, ConfigMap, and ClusterIP Service
- Configured Prometheus to scrape `log-service:8000` at `/metrics`
- Verified `up{job="log-service"}` and `log_service_http_requests_total` in the Prometheus UI
- Kept the setup local/dev focused instead of adding production Prometheus Operator complexity

Production follow-ups:

- Choose kube-prometheus-stack, Prometheus Operator, or managed monitoring for production
- Add scrape annotations or ServiceMonitor resources depending on the chosen stack
- Decide whether `/metrics` scrape traffic should be excluded from request metrics or filtered in dashboards
- Run Kubernetes database migrations before relying on ingestion metrics from `POST /logs` in cluster

### Phase 6.5 - Grafana Dashboards

Status: Complete for local/dev Grafana foundation

Goal:

- Visualize platform behavior.

Completed scope:

- Added a dev-overlay Grafana Deployment, datasource ConfigMap, and ClusterIP Service
- Provisioned Grafana with a Prometheus datasource at `http://prometheus:9090`
- Verified Grafana can query Prometheus data from local Kubernetes
- Built the first dashboard manually so PromQL queries and panel choices can be learned before codifying them
- Added starter panels for recent request volume, request rate, server errors, p95 latency, and logs ingested

Dashboard queries explored:

- `increase(log_service_http_requests_total[5m])` for local recent request volume
- `rate(log_service_http_requests_total[5m])` for request throughput
- `increase(log_service_http_requests_total{status_code=~"5.."}[5m])` for recent server errors
- `histogram_quantile(0.95, ...)` over `log_service_http_request_duration_seconds_bucket` for p95 latency
- `increase(log_service_logs_ingested_total[5m])` for recent successful log ingestion

Remaining dashboard scope:

- Health and readiness status
- More polished panel legends, units, and layout

Production follow-ups:

- Replace lightweight dev Grafana with kube-prometheus-stack, Grafana Operator, managed Grafana, or another production monitoring choice
- Move Grafana admin credentials and sensitive configuration into Kubernetes Secrets or external secret management
- Add auth, TLS, RBAC, and controlled ingress before exposing Grafana outside local dev
- Provision dashboards as code after the first dashboard design stabilizes
- Add Kubernetes/CI migrations before relying on ingestion metrics in deployed environments

### Phase 6.6 - Alerts

Status: Complete for local/dev Prometheus alert foundation

Goal:

- Detect platform problems automatically.

Completed scope:

- Added a dev Prometheus alert rules file through the `prometheus-config` ConfigMap
- Configured Prometheus to load `/etc/prometheus/alert_rules.yml`
- Added `LogServiceTargetDown` for `up{job="log-service"} == 0`
- Used `for: 2m` to avoid alerting immediately on a single missed scrape
- Verified the alert lifecycle through pending, firing, and inactive states

Potential future alerts:

- High 5xx rate
- High request latency
- Postgres readiness failures
- Unexpected ingestion volume drops once normal ingestion baselines are known

Production follow-ups:

- Move from ConfigMap-embedded dev rules to Prometheus Operator `PrometheusRule` resources or managed alert rules
- Add Alertmanager or a managed notification path
- Tune severity levels and `for:` durations based on real behavior
- Add runbook links in alert annotations
- Avoid noisy ingestion-volume alerts until expected traffic patterns are known

### Phase 6.7 - Tracing

Goal:

- Follow requests across service boundaries once the platform has enough services to justify distributed tracing.

Planned scope:

- Add OpenTelemetry instrumentation
- Trace frontend-to-backend request paths where practical
- Expand tracing when additional backend services are introduced

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
