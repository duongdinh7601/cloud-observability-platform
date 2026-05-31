# Kubernetes

Kubernetes manifests for the Cloud Observability Platform are organized with Kustomize so shared platform resources stay separate from environment-specific choices.

## Layout

```text
infra/kubernetes/
|-- base/
|   |-- frontend.yaml
|   |-- log-service.yaml
|   |-- postgres.yaml
|   |-- kustomization.yaml
|-- overlays/
|   |-- dev/
|   |   |-- ingress.yaml
|   |   |-- kustomization.yaml
|   |   |-- secrets.yaml
|   |-- prod/
|   |   |-- kustomization.yaml
```

## Base And Overlays

- `base/` defines the shared Kubernetes shape: Deployments, Services, health probes, resource requests/limits, Secrets, and Postgres storage.
- `overlays/dev/` adapts the base for local Docker Desktop Kubernetes by using local image tags such as `frontend:k8s-dev` and `log-service:k8s-dev`, plus a local Ingress host.
- `overlays/prod/` documents the production-intent image shape with GHCR-hosted release images. It is not ready to apply until real release tags and production secret handling are in place.

## Secret Handling

The base manifests reference Kubernetes Secret names but do not own the local secret values.

Current local development behavior:

- `overlays/dev/secrets.yaml` creates local-only Secret values for Docker Desktop Kubernetes.
- `log-service` expects a Secret named `log-service-db` with a `DATABASE_URL` key.
- `postgres` expects a Secret named `postgres-db` with `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` keys.

This keeps the shared base focused on the secret contract while the dev overlay provides disposable local values.

Production direction:

- Do not commit real production credentials to Git.
- Keep the same Secret names and keys as the workload contract.
- Provide production values through a real secret-management workflow, such as External Secrets Operator connected to AWS Secrets Manager, Google Secret Manager, Azure Key Vault, or HashiCorp Vault.

## Local Docker Desktop Kubernetes

Build local images before applying the dev overlay:

```powershell
docker build -t log-service:k8s-dev services/log-service
docker build -t frontend:k8s-dev frontend
```

Apply the local development stack:

```powershell
kubectl apply -k infra/kubernetes/overlays/dev
```

Inspect the running resources:

```powershell
kubectl get pods
kubectl get services
kubectl get pvc
```

## Local Ingress

The dev overlay includes an Ingress for the frontend:

```text
http://cloud-observability.local
```

The Ingress routes browser traffic to the internal `frontend` Service on port `3000`.

Install the ingress-nginx controller before using the Ingress:

```powershell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.15.1/deploy/static/provider/cloud/deploy.yaml
```

Wait for the controller:

```powershell
kubectl get pods -n ingress-nginx
kubectl get services -n ingress-nginx
```

Apply the dev overlay:

```powershell
kubectl apply -k infra/kubernetes/overlays/dev
```

Inspect the Ingress:

```powershell
kubectl get ingress
kubectl describe ingress frontend
```

Add this local hosts entry on Windows:

```text
127.0.0.1 cloud-observability.local
```

The hosts file is located at:

```text
C:\Windows\System32\drivers\etc\hosts
```

Flush DNS if the hostname does not resolve immediately:

```powershell
ipconfig /flushdns
```

Then open:

```text
http://cloud-observability.local
```

Port-forwarding is still useful for quick frontend checks:

```powershell
kubectl port-forward service/frontend 3000:3000
```

Expose the backend API locally when using Swagger UI or direct API calls:

```powershell
kubectl port-forward service/log-service 8000:8000
```

Delete the local stack:

```powershell
kubectl delete -k infra/kubernetes/overlays/dev
```

Deleting the dev stack also deletes the local Postgres PVC declared by the manifests, so local Kubernetes test data may be removed.

## Production Notes

The current Kubernetes setup is production-shaped but not production-final.

Known follow-up areas:

- Replace committed raw Secrets with a real secret-management workflow.
- Replace placeholder production image tags with immutable release tags.
- Decide whether Postgres should be managed outside the cluster.
- Add ingress or gateway routing for public traffic.
- Run database migrations through a Kubernetes Job or CI/CD-controlled migration step before rolling out app pods.
- Add CI/CD automation for image builds, scans, pushes, and deployment.
- Add namespaces, RBAC, NetworkPolicies, container hardening, TLS, and production ingress/cert management.
- Add observability resources such as metrics scraping, dashboards, alerts, and eventually tracing.
- Centralize service-wide JSON logging configuration while keeping container logs one JSON object per line where practical.

## Database Migrations

The `log-service` uses Alembic migrations. Application pods should not create or mutate database tables during startup.

Future production rollout shape:

```text
CI builds log-service image
-> CI pushes immutable image tag
-> CI runs a Kubernetes migration Job with that same image tag
-> Job runs alembic upgrade head
-> Job reads DATABASE_URL from Secret log-service-db
-> CI rolls out the log-service Deployment after the Job succeeds
```

The migration Job should use the same Secret contract as the app:

```text
Secret: log-service-db
Key: DATABASE_URL
```

Because Kubernetes Jobs are run-to-completion resources, CI/CD should either create release-specific Job names or clean up old migration Jobs before creating a new one.
