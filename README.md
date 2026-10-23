# AI Workforce Platform

Professional starter monorepo for building a multi-tenant SaaS that provides AI-driven agents and retrieval-augmented workflows.

Repository: https://github.com/0xyz-exe/AI-Workforce-Platform

## Screenshots

### Agent Marketplace & Workflow Orchestration
![Agent marketplace](docs/screenshots/01_agent_marketplace.png)

### Multi-Tenant Workspace & RAG Pipelines
![RAG pipelines](docs/screenshots/02_rag_pipeline.png)

### Background Tasks & Worker Queue Monitoring
![Worker queue](docs/screenshots/03_task_queue.png)

### MinIO Object Storage & Vector Indexing
![Storage & vectors](docs/screenshots/04_storage_vectors.png)

## Overview

This repository contains a full-stack reference implementation with a Next.js frontend and a FastAPI backend. It is optimized for local development using Docker Compose and structured to be extended toward production deployments.

Core capabilities
- Multi-tenant data model and repository patterns
- RAG pipelines backed by Qdrant
- Background processing with Redis and Celery
- S3-compatible object storage with MinIO

## Tech Stack

- Frontend: Next.js (TypeScript), Tailwind CSS
- Backend: FastAPI (Python 3.12), SQLAlchemy, Alembic
- Database: PostgreSQL
- Vector DB: Qdrant
- Cache / Broker: Redis (+ Celery)
- Object storage: MinIO (S3)
- Orchestration: Docker & Docker Compose

## Quickstart (Local)

1. Copy and edit environment variables:

	```powershell
	copy .env.example .env
	# edit .env and fill required values
	```

2. Build and start the stack:

	```powershell
	docker compose up -d --build
	```

3. Verify running services in your browser or with `docker compose ps`:

	- Frontend: http://localhost:3000
	- Backend OpenAPI: http://localhost:8000/docs
	- MinIO Console: http://localhost:9001

4. Stop the stack:

	```powershell
	docker compose down
	```

Notes
- Ensure `.env` exists (copy from `.env.example`) before running Compose.
- If host ports conflict (for example `6379`), stop the local service or adjust the port mapping in `docker-compose.yml`.

## Development

- Frontend (development):

  ```powershell
  cd web
  npm install
  npm run dev
  ```

- Backend (development):

  ```powershell
  cd backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8000
  ```

## Current Status

- Frontend: production build completed successfully (static pages generated).
- Backend: code compiles (`python -m compileall app`).
- Docker Compose: full stack verified locally (api, web, postgres, qdrant, minio, redis are running).

Before publishing
- Remove or rotate any real secrets from `.env` and confirm no sensitive data is committed.
- Add or confirm `LICENSE` file to match your intended project license.

## Contributing

- Open issues for bugs or feature requests.
- Use the standard fork → branch → PR workflow. Include a clear description and, where applicable, tests or reproduction steps.

