# Progress Log

A running record of what's been built and *why*, phase by phase. Meant to be
skimmable before an interview — each decision below is something you should
be able to explain out loud.

## Phase 1: Containerization (done)

### The app
A minimal To-Do REST API (FastAPI + SQLAlchemy + Postgres) with a React
(Vite) frontend. Deliberately simple — the point of this project is the
DevOps tooling around it, not the app itself.

### Repo structure
`backend/` and `frontend/` are siblings, not nested — each gets its own
Dockerfile, and later its own CI job and Helm chart, so keeping them as
independent top-level units mirrors how they'll be built/deployed
independently. `terraform/`, `k8s/`, `.github/workflows/` exist now as empty
folders (with `.gitkeep`) so the repo shape is stable across phases — later
phases add files, not new top-level structure.

### Backend Dockerfile — key decisions
- **`python:3.12-slim` base**, not `alpine`. Alpine's musl libc breaks or
  slows down builds of C-extension packages like `psycopg2` — `slim` is the
  standard middle ground between image size and compatibility.
- **Multi-stage build**: a `builder` stage creates a venv and installs
  dependencies (needs no build tools since `psycopg2-binary` ships
  precompiled wheels, but the pattern matters for any package that doesn't);
  the `runtime` stage copies only the venv and app code onto a clean base.
  Nothing used only to *build* the app ships in the image that *runs* it.
- **Non-root user** (`appuser`): if the app process is ever compromised, it
  isn't running as root inside the container.
- **Dependency layer before app code layer**: `requirements.txt` is copied
  and installed before the rest of the source is copied, so Docker's build
  cache reuses the dependency-install layer on every code-only change —
  faster rebuilds.

### Frontend Dockerfile — key decisions
- **Multi-stage build**: stage 1 (`node:20-alpine`) runs `npm install` +
  `npm run build`; stage 2 serves only the static output. Node, npm, and
  `node_modules` (100s of MB) never reach the image that serves traffic —
  only the built `dist/` folder does.
- **`nginxinc/nginx-unprivileged`** instead of plain `nginx`. The official
  `nginx` image binds port 80 and runs as root by default; making it rootless
  takes extra config. The unprivileged variant already runs as a non-root
  user on port 8080 out of the box.
- **Same-origin API calls via nginx reverse proxy**: the frontend calls
  `/api/...` (a relative path); nginx forwards anything under `/api/` to the
  `backend` container. This avoids CORS entirely in the compose setup — the
  browser only ever talks to one origin. Vite's dev server proxy (in
  `vite.config.js`) mirrors this same behavior for local `npm run dev`, so
  the frontend code never needs to know which environment it's running in.

### docker-compose.yml — key decisions
- **`depends_on` with `condition: service_healthy`**, not a plain
  `depends_on`. Plain `depends_on` only waits for the container to *start*,
  not for Postgres to actually be ready to accept connections — a real
  source of flaky "connection refused" errors on first boot. The healthcheck
  (`pg_isready`) makes `backend` wait until the DB can actually serve
  queries.
- **Named volume (`db_data`)** for Postgres data, so `docker compose down`
  (without `-v`) doesn't wipe your local data between restarts.
- **`.env` / `.env.example`**: real values go in `.env` (gitignored);
  `.env.example` documents which variables are required without leaking
  actual credentials into git history.

### Deliberately deferred (not built yet)
- CI (`.github/workflows/`) — Phase 2.
- Terraform for ACR/AKS provisioning — Phase 3.
- CD, K8s manifests/Helm — Phase 4.
- Observability, security hardening (image scanning, secrets management,
  network policies) — later phase.
- Alembic migrations for the DB schema — `Base.metadata.create_all()` is
  used for now since there's only one table and no migration history to
  manage yet.
