# Infrastructure

The `infra/` directory is reserved for infrastructure artifacts that sit outside the application source code.

At the current stage of the project, the active Docker Compose files live at the repository root, while `infra/` is primarily a placeholder for future Kubernetes and infrastructure-specific assets.

## Current State

- Root-level Compose files drive local development and production-like container workflows
- `infra/docker/` is reserved for future Docker-related infrastructure assets if the platform grows beyond the current layout
- `infra/kubernetes/` is reserved for future manifests and deployment resources

## Planned Direction

- Add Kubernetes manifests for frontend, log-service, and supporting infrastructure
- Add production deployment resources such as ConfigMaps, Secrets, and ingress definitions
- Keep infrastructure concerns separate from service application code
