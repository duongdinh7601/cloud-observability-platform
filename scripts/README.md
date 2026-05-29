# Scripts

The `scripts/` directory is reserved for shared, repo-level utility scripts.

At the current stage of the project, most operational helper scripts live with the services that use them. For example, service-specific container healthcheck scripts live inside each service directory rather than in this shared folder.

## Intended Use

- Shared setup or bootstrap scripts
- Repository-wide automation tasks
- Developer convenience scripts that are not owned by a single service
- Future CI/CD helper scripts for validation, image build, or deployment workflows when they are shared across services

## Notes

- Keep service-specific scripts close to the service that owns them
- Use this directory when a script is truly shared across the monorepo
- Document new scripts here as the folder grows
- Prefer documented package or service commands first; add scripts here only when they reduce repeated cross-repo work
