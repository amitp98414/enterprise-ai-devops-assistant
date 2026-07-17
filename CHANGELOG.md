# Changelog

All notable changes to OpsSage AI are documented in this file.

## [1.1.0] - 2026-07-17

### Added

- X-API-Key authentication for protected AI endpoints.
- Per-API-key in-memory rate limiting.
- `Retry-After` header for rate-limited requests.
- Automated tests for authentication and rate limiting.
- Security configuration examples and documentation.

### Changed

- OpenAI client is initialized only when an AI request is authorized.
- `/chat` and `/agent/run` are now protected endpoints.
- Application version updated to `1.1.0`.

### Security

- Missing or invalid API keys return HTTP `401`.
- Exceeded rate limits return HTTP `429`.
- Disabled AI deployments return HTTP `503`.
- API keys are compared using constant-time comparison.

## [1.0.0] - 2026-07-17

### Added

- Initial OpsSage AI portfolio release.
- FastAPI multi-agent backend.
- Docker Compose deployment.
- GitHub Actions and CircleCI pipelines.
- Prometheus metrics and alert rules.
- Provisioned Grafana monitoring dashboard.
- Public Render deployment and Swagger documentation.
