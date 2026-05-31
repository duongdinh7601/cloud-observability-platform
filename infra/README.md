# Infrastructure

The `infra/` directory contains infrastructure artifacts that sit outside the application source code.

Docker Compose files currently live at the repository root, while Kubernetes resources live under `infra/kubernetes/`.

## Current State

- Root-level Compose files drive local development and production-like container workflows.
- `infra/kubernetes/base/` contains shared Kubernetes manifests.
- `infra/kubernetes/overlays/dev/` adapts the base for local Docker Desktop Kubernetes.
- `infra/kubernetes/overlays/prod/` captures production-intent image references for a future release workflow.
- The `log-service` now emits structured JSON request logs to stdout/stderr for container log collection.

## Planned Direction

- Add ingress or gateway-level routing for public traffic.
- Replace committed raw Secrets with a production secret-management workflow.
- Move production image tags to immutable release versions.
- Add CI/CD-driven database migration execution before application rollouts.
- Add platform observability infrastructure for metrics, dashboards, alerts, and tracing.
- Add linting/formatting and validation checks to CI.
- Keep infrastructure concerns separate from service application code.

See [kubernetes/README.md](kubernetes/README.md) for Kubernetes commands and structure.
