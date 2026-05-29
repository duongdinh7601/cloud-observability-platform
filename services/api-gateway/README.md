# API Gateway

The API Gateway is a planned service for a future phase of the Cloud Observability Platform.

It is not part of the active Compose stack yet, but the directory exists as a placeholder for when the platform grows beyond a direct frontend-to-service routing model.

## Planned Responsibilities

- Provide a single backend entrypoint for multiple internal services
- Centralize cross-cutting concerns such as authentication, request policy, and service routing
- Support future service expansion beyond the current log-service-only architecture

## Current Status

- Directory scaffold exists
- Service is not implemented yet
- Service is not part of current container orchestration
- The current request path uses the Next.js frontend rewrite directly to `log-service`
- A gateway should only be added when the platform has enough backend services or cross-cutting policy needs to justify it

## Future Direction

If the platform grows to include metrics, alerts, or additional internal services, the gateway may become the place to consolidate:

- routing
- auth and authorization
- request shaping
- shared response policies
- rate limiting, API keys, or tenant-aware routing
