# Todo App

A To-Do app (FastAPI + Postgres + React), containerized with Docker and
deployed to Azure (ACR/AKS) via Terraform, GitHub Actions, and Kubernetes/Helm.
See [PROGRESS.md](./PROGRESS.md) for a log of infrastructure decisions and why
they were made.

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (docs at /docs)
- Postgres: localhost:5432 (only exposed for local debugging)

## Project layout

```
backend/     FastAPI To-Do API
frontend/    React (Vite) UI, served by nginx in production/compose
terraform/   (Phase 3) ACR/AKS provisioning
k8s/         (Phase 4) Kubernetes manifests / Helm chart
.github/     (Phase 2) CI/CD workflows
docs/        Longer-form notes as the project grows
```
