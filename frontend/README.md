# Frontend Dashboard

The frontend is a Next.js dashboard for browsing and inspecting logs from the Cloud Observability Platform.

It is built as the public-facing entrypoint of the platform and uses same-origin routing to reach backend APIs without exposing backend container details to the browser.

## Responsibilities

- Render the logs dashboard UI
- Fetch paginated log data from the backend
- Keep filters in the URL for shareable state
- Expose a lightweight `/health` endpoint for container readiness

## Tech Stack

- Next.js 15 App Router
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query

## Key Features

- Infinite-style pagination with "Load more"
- Level and service filters
- Debounced service search
- URL-synced filter state
- Skeleton loading and retry UI
- Relative timestamps and copy-to-clipboard actions
- Same-origin API access through Next rewrites

## Architecture Notes

- The browser requests `/api/...` on the frontend origin
- Next rewrites those requests to the internal backend service
- The frontend container exposes `/health` for operational checks
- The production-like frontend image uses a multi-stage Docker build and a stable runtime command

## Local Development

For the full platform, run the repo root Compose files:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

If you want to run the frontend by itself:

```bash
cd frontend
npm install
npm run dev
```

## Frontend Structure

```text
frontend/
|-- src/
|   |-- app/
|   |   |-- health/
|   |   |   |-- route.ts
|   |   |-- logs/
|   |   |   |-- page.tsx
|   |-- components/
|   |-- lib/
|   |   |-- api/
|   |   |-- use-debounced-value.ts
|-- public/
|-- scripts/
|   |-- container_healthcheck.js
|-- Dockerfile
|-- next.config.mjs
|-- package.json
|-- README.md
```
