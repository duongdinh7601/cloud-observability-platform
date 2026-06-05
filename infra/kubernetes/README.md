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
|   |   |-- grafana.yaml
|   |   |-- ingress.yaml
|   |   |-- kustomization.yaml
|   |   |-- prometheus.yaml
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

## Local Prometheus

The dev overlay includes a lightweight Prometheus Deployment for local learning and metrics verification.

It uses:

- `prometheus-config` ConfigMap for `prometheus.yml`
- `prom/prometheus:v2.53.4`
- a `ClusterIP` Service named `prometheus`
- a scrape target of `log-service:8000` with `metrics_path: /metrics`

Apply the dev overlay:

```powershell
kubectl apply -k infra/kubernetes/overlays/dev
```

Open Prometheus locally with port-forwarding:

```powershell
kubectl port-forward service/prometheus 9090:9090
```

Then open:

```text
http://127.0.0.1:9090
```

Useful queries:

```text
up{job="log-service"}
log_service_http_requests_total
log_service_http_request_duration_seconds_count
log_service_logs_ingested_total
```

If `up{job="log-service"}` is `0`, check the Prometheus target error under **Status -> Targets**. A `404` usually means the Kubernetes `log-service:k8s-dev` image is stale and needs to be rebuilt.

Successful `POST /logs` ingestion in Kubernetes depends on the database schema being migrated. Until the migration Job strategy is implemented, the ingestion counter may remain `0` in cluster even when Prometheus scraping is healthy.

## Local Grafana

The dev overlay includes a lightweight Grafana Deployment for local dashboard exploration.

It uses:

- `grafana-datasources` ConfigMap for datasource provisioning
- `grafana/grafana:11.1.0`
- a `ClusterIP` Service named `grafana`
- a provisioned Prometheus datasource pointing to `http://prometheus:9090`

Apply the dev overlay:

```powershell
kubectl apply -k infra/kubernetes/overlays/dev
```

Open Grafana locally with port-forwarding:

```powershell
kubectl port-forward service/grafana 3000:3000
```

Then open:

```text
http://127.0.0.1:3000
```

For local development, the default Grafana login is typically:

```text
admin / admin
```

Grafana may require a password change after first login. Production credentials must not be committed to Git; use Kubernetes Secrets, external secret management, SSO, or managed Grafana depending on the final production monitoring choice.

Useful starter Explore query:

```text
up{job="log-service"}
```

Starter dashboard panels:

```text
HTTP Requests In Last 5 Minutes
sum by (method, path, status_code) (
  increase(log_service_http_requests_total[5m])
)
```

```text
HTTP Request Rate
sum by (method, path, status_code) (
  rate(log_service_http_requests_total[5m])
)
```

```text
Server Errors In Last 5 Minutes
sum by (method, path, status_code) (
  increase(log_service_http_requests_total{status_code=~"5.."}[5m])
)
```

```text
p95 Request Latency
histogram_quantile(
  0.95,
  sum by (le, method, path) (
    rate(log_service_http_request_duration_seconds_bucket[5m])
  )
)
```

```text
Logs Ingested In Last 5 Minutes
increase(log_service_logs_ingested_total[5m])
```

Use broad discovery queries such as `{__name__=~"log_service_.*"}` only for exploration. Dashboard panels should use specific metric names so helper series such as `*_created` do not appear as misleading large values.

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
- Replace the lightweight dev Prometheus/Grafana setup with production monitoring such as kube-prometheus-stack, Prometheus Operator, Grafana Operator, managed Prometheus, or managed Grafana.
- Move Grafana admin credentials and other sensitive monitoring configuration into Secrets or external secret management.
- Provision Grafana dashboards as code once the dashboard design stabilizes.
- Add alerts and eventually tracing.
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

### Local Dev Recovery: Existing Table Without Alembic History

Older local Kubernetes databases may have a `logs` table that was created before Alembic owned schema changes. In that case, `alembic upgrade head` can fail with `relation "logs" already exists` because Alembic has no version history and tries to create the initial table again.

For local development only, if the existing table matches the first migration shape, stamp the database at the baseline revision and then upgrade:

```powershell
kubectl port-forward service/postgres 5434:5432
```

From `services/log-service` in another terminal:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:5434/logs"
alembic stamp 2e3e3bad4dcc
alembic upgrade head
```

`alembic stamp` records migration history without changing tables. It should be treated as a recovery tool, not the normal production migration path.
