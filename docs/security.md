# Security Notes

This document tracks security-related decisions and follow-ups for the Cloud Observability Platform.

## Image Scanning

GitHub Actions builds the backend and frontend Docker images in CI and scans them with Trivy.

Current scan behavior:

- Images are built with local CI tags:
  - `log-service:ci`
  - `frontend:ci`
- Trivy scans `HIGH` and `CRITICAL` vulnerabilities.
- Scans use `ignore-unfixed: true` to focus on findings with available fixes.
- Scans are currently report-only with `exit-code: "0"`.

The current goal is visibility and baseline tracking. CI should not fail on image scan findings until the baseline is reviewed and remediation policy is deliberate.

## Current Baseline

Baseline source: latest reviewed GitHub Actions `container-builds` output on the Phase 7 image scanning work.

### `log-service:ci`

Summary:

- `HIGH`: 3
- `CRITICAL`: 0

Primary source:

- Python package dependency

Known findings:

| Package | Installed | Severity | Fixed Version | Notes |
| --- | --- | --- | --- | --- |
| `starlette` | `0.35.1` | HIGH | `0.40.0`, `1.1.0`, `1.3.1` depending on CVE | Comes through the FastAPI/Starlette dependency chain. Remediation should be coordinated with FastAPI compatibility testing. |

Tracked CVEs:

- `CVE-2024-47874`
- `CVE-2026-48818`
- `CVE-2026-54283`

Likely remediation path:

- Review current FastAPI and Starlette compatibility.
- Upgrade FastAPI if needed so the resolved Starlette version reaches fixed versions.
- Run backend Ruff checks, tests, Alembic migration commands where relevant, and Docker image scan again.

### `frontend:ci`

Summary:

- Debian OS packages:
  - `HIGH`: 4
  - `CRITICAL`: 2
- Node package findings:
  - `HIGH`: 36
  - `CRITICAL`: 1

Primary sources:

- Debian packages in the Node base image
- Node/npm packages in the frontend image

Known Debian package findings:

| Package | Installed | Severity | Fixed Version | Notes |
| --- | --- | --- | --- | --- |
| `libcap2` | `1:2.66-4+deb12u2+b2` | HIGH | `1:2.66-4+deb12u3` | Base image operating system package. |
| `libgnutls30` | `3.7.9-2+deb12u6` | CRITICAL/HIGH | `3.7.9-2+deb12u7` | Base image operating system package with multiple findings. |

Tracked Debian CVEs:

- `CVE-2026-4878`
- `CVE-2026-33845`
- `CVE-2026-42010`
- `CVE-2026-33846`
- `CVE-2026-3833`
- `CVE-2026-42009`

Known Node package examples:

- `brace-expansion`
- `cross-spawn`
- `glob`
- `ip-address`
- `minimatch`
- `next`
- `tar`

Likely remediation path:

- Review whether findings come from application dependencies, transitive dependencies, or packages bundled in the Node runtime image.
- Prioritize Next.js findings because Next is directly part of the frontend runtime.
- Consider updating the Node base image tag or digest if fixed Debian packages are available in newer image builds.
- Avoid running broad dependency update commands blindly; dependency upgrades should be reviewed and verified with `npm run lint`, `npm run build`, Docker image builds, and Trivy scans.

## Remediation Priority

Recommended order:

1. Frontend image critical findings.
2. Direct frontend runtime dependency findings, especially Next.js.
3. Backend Starlette/FastAPI dependency findings.
4. Remaining transitive package findings.
5. Enforcement policy after the baseline is reduced.

## Future Enforcement Policy

Current status:

- Report-only scans.

Potential future policy:

- Fail CI on fixable `CRITICAL` vulnerabilities first.
- After critical findings are controlled, consider failing on fixable `HIGH` and `CRITICAL` vulnerabilities.
- Document any accepted risk or temporary exception with a reason, owner, and review date.

Production follow-ups:

- Pin production image tags immutably.
- Consider image digest pinning for base images.
- Add a documented exception process for vulnerabilities that cannot be fixed immediately.
- Revisit runtime image hardening, non-root users, smaller images, and dependency separation.
