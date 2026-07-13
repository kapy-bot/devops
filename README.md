# Todo App — DevOps Learning Project

A small To-Do app (FastAPI + Postgres + React) used as a vehicle to practice
the DevOps toolchain: Docker, GitHub Actions, Terraform, Kubernetes/Helm on
Azure (ACR/AKS). See [PROGRESS.md](./PROGRESS.md) for a phase-by-phase log of
decisions and why they were made.

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
