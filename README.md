# Cloud Observability Platform

A full-stack observability platform built to demonstrate production-minded engineering across backend, frontend, and deployment workflows.

The current platform centers on a log ingestion service, a Next.js dashboard, and a deployment model that can run through Docker Compose or local Kubernetes. The project is intentionally learning-first and production-shaped: simpler choices are used when they make concepts clear, then revisited as the platform matures.

## Tech Stack

- Frontend: Next.js 15, React 18, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query
- Backend: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, psycopg v3
- Database: PostgreSQL 16
- Containerization: Docker, Docker Compose
- Orchestration: Kubernetes, Kustomize
- Future platform work: structured service logs, Prometheus, Grafana, CI/CD, stronger secret management

## Repository Layout

| Path | Purpose |
| --- | --- |
| `frontend/` | Next.js logs dashboard and frontend container image |
| `services/log-service/` | FastAPI log ingestion and retrieval service |
| `services/api-gateway/` | Placeholder for a future gateway service |
| `docs/` | Architecture notes, service docs, and roadmap |
| `infra/` | Infrastructure artifacts, including Kubernetes base manifests and overlays |
| `scripts/` | Shared repo-level utility script area |

## Container Architecture

- The frontend is the single public entrypoint in the production-like Compose path.
- The frontend reaches the backend through same-origin routing, so the browser does not call the backend directly.
- The backend API and PostgreSQL database stay internal to the container network in the production-like deployment model.
- Both application services expose health endpoints and container healthchecks so readiness is explicit at the service boundary.

## Kubernetes Architecture

- Kubernetes manifests live under `infra/kubernetes/`.
- `base/` contains shared Deployments, Services, health probes, resource requests/limits, Secrets, and Postgres storage.
- `overlays/dev/` uses local Docker Desktop image tags for hands-on Kubernetes testing.
- `overlays/prod/` documents the production-intent image shape for future GHCR release images.
- The Kubernetes request path mirrors the Compose model: browser to frontend, frontend rewrite to `log-service`, log-service to `postgres`.
- Database schema changes are managed through Alembic. A future CI/CD migration step should run migrations through a Kubernetes Job before rolling out new app pods.

## Run Modes

- `docker-compose.yml` defines the shared internal service topology and common runtime wiring.
- `docker-compose.dev.yml` adds local developer behavior such as host port publishing, source mounts, and frontend hot reload.
- `docker-compose.prod.yml` adds production-like operational behavior, exposing only the frontend and applying restart policies.

### Local Development

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### Production-Like Compose Path

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

### Local Kubernetes Path

```bash
docker build -t log-service:k8s-dev services/log-service
docker build -t frontend:k8s-dev frontend
kubectl apply -k infra/kubernetes/overlays/dev
```

Expose the frontend locally:

```bash
kubectl port-forward service/frontend 3000:3000
```

## Current Progress

- Phase 1: Backend log service - complete
- Phase 2: Frontend logs dashboard - complete
- Phase 3: Container maturity and production-like Compose path - complete for the current scope
- Phase 4: Kubernetes deployment foundations - complete for the current local/dev scope
- Phase 5: Database migration workflow - complete locally and in tests; Kubernetes/CI execution strategy planned
- Phase 6: Platform observability with structured logs, metrics, Prometheus, and Grafana - planned

## Current Production-Shaped Follow-Ups

- Add a Kubernetes/CI migration execution strategy using a run-to-completion Job.
- Replace placeholder production image tags with immutable release tags.
- Add CI/CD for tests, linting, image build, scanning, registry push, migration execution, and rollout verification.
- Replace local Kubernetes Secrets with External Secrets Operator plus a cloud secret manager or Vault.
- Decide on managed Postgres versus in-cluster Postgres for production.
- Add structured logs, metrics, dashboards, alerts, and eventually distributed tracing.
- Add Python and frontend linting/formatting automation.

See [docs/roadmap.md](docs/roadmap.md) for the phase-based roadmap.
