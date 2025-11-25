# Copilot/AI Agent Instructions — Seed2Sale

This file gives targeted, actionable instructions to AI coding agents working in this repository.

## Quick architectural summary
- Backend: Django project in `src/` (entry: `src/manage.py`, settings: `src/seed2sale/settings.py`). Uses Django REST Framework and `rest_framework_simplejwt` for token auth.
- Frontend: React app in `frontend/` (CRA) and server runs on port 3000 during dev. Static assets and Tailwind CSS builds are in `static/`.
- Data flow: Frontend calls backend JSON endpoints under `/api/*` defined in `src/seed2sale/urls.py`. Some older frontend code references legacy endpoints (see `frontend/src/api/auth.js`).

## Important files / entry points
- Backend:
  - `src/manage.py` (runserver, migrations, tests)
  - `src/seed2sale/settings.py` (CORS, REST_FRAMEWORK defaults, AUTH_USER_MODEL, STATIC settings)
  - `src/seed2sale/urls.py` (API router registration and JWT endpoints)
  - `src/seed2sale/seed.py` (helper to populate sample data)
  - Apps: `src/accounts/`, `src/api/`, `src/products/`, `src/orders/`, `src/cart/`, `src/warehouse/`, `src/logistics/`.
- Frontend:
  - `frontend/src/api/api.js` — central fetch helper and token storage
  - `frontend/src/api/*` — collection of API helpers (auth.js, products.js, etc.)
  - `frontend/package.json` — scripts: `start`, `build`, `dev:css` for Tailwind
  - Root `package.json` for Tailwind CSS used by Django templates
  - `frontend/auth.js` and `frontend/src/context/AuthContext.jsx` are older/non-React helpers but still used by static templates (they use localStorage.s2s_token now).

## Dev workflows & commands
- Backend (recommended):
  - Setup (Poetry):
    - `poetry install` from project root
    - `cd src`; `poetry run python manage.py makemigrations` to create new migrations after model changes
    - `cd src`; `poetry run python manage.py migrate` to run migrations
    - `poetry run python manage.py runserver` to start the Django dev server
  - If not using Poetry: create a venv and use pip:
    - `cd src`
    - `python -m venv .venv` ; `.\.venv\Scripts\activate` (Windows PowerShell)
    - `pip install -r requirements.txt` (if present) or `pip install django djangorestframework djangorestframework-simplejwt django-cors-headers` before running `manage.py` commands
  - Seed data (local dev): `cd src` then `python seed2sale/seed.py` (runs using Django settings)
  - Run tests: `cd src` then `python manage.py test` (runs Django tests)
  - Create superuser: `cd src` then `python manage.py createsuperuser` to access `/admin/`.
  - Collect static for production: `cd src` then `python manage.py collectstatic --noinput`.

- Frontend (React):
  - `cd frontend` then `npm install` (or `yarn`) to install deps
  - `npm start` to run the dev server (localhost:3000)
  - `npm run build` to build the production bundle
  - Tailwind dev/build (if working on CSS outside `frontend`): root `package.json` has `dev` and `build` scripts — run `npm run dev` or `npm run build` from the repository root.

## Authentication & API notes (really important)
- Backend uses `rest_framework_simplejwt` token auth. Endpoints:
  - `POST /api/token/` — get JWT pair
  - `POST /api/token/refresh/` — refresh
  - `POST /api/accounts/token/` — custom Email/Phone token view (accepts identifier + password) if Accounts URLs are included
  - `GET /api/auth/me/` — returns current user
- Default DRF permission is `IsAuthenticated` (see `settings.py`). Many API views will be protected unless their view/classes use `permissions.AllowAny`.
 - Frontend `frontend/src/api/api.js` uses localStorage key `s2s_token` and stores token strings. `apiFetch()` by default sets the `Authorization` header to `Bearer <token>` — align with backend (SimpleJWT).
  - When touching auth flows, align the frontend to use `Bearer` (SimpleJWT) or add a token view supporting conventional `Token` header.
  - For example, update `frontend/src/api/api.js` to use `Authorization: Bearer ${token}` if you expect JWT.

## When adding API endpoints
- Add the endpoint in the corresponding app (models, serializers, viewsets). Register the viewset in `src/seed2sale/urls.py` using `router.register(r'myresource', MyViewSet)` so the API router exposes `/api/myresource/`.
- Follow existing serializer and ViewSet patterns in `src/api/views.py`.
- Respect DRF default permissions: add `permission_classes = [AllowAny]` on public endpoints or explicitly set `IsAuthenticated`.

Example: Add a new model `src/products/models.py` -> Add serializer in `src/products/serializers.py` -> Add ModelViewSet in `src/products/views.py` -> Register in `src/seed2sale/urls.py` using `router.register(r'newmodels', NewModelViewSet)` -> Run `poetry run python manage.py makemigrations` and `poetry run python manage.py migrate`.

## Project-specific conventions and quirks
- `AUTH_USER_MODEL` is `accounts.User` — use `settings.AUTH_USER_MODEL` when referencing the user model in migrations and ForeignKey relationships.
- `static/` contains Tailwind CSS source and output. You’ll often re-run the tailwind build (root `npm run dev`) when changing styles used by Django templates.
- There are duplicated/older files in places (e.g., duplicate definitions in `products/models.py` and multiple ways of auth in frontend) — prefer the code used by `src/seed2sale/urls.py` (ViewSets under `api` app) as the authoritative API surface.
- Keep seeds: `src/seed2sale/seed.py` helps quickly set up demo data. Use it for local development but do not seed on production without review.
- SQLite DB (`db.sqlite3`) exists in repo; be cautious when seeding or resetting in development — the DB file is checked in.

## Debugging tips
- Backend logs: `python manage.py runserver` prints server logs to console. Increase verbosity if needed.
- Replicating frontend/back-end: run frontend dev server (`npm start`) and backend (`python manage.py runserver`) in separate terminals.
- If CORS or auth errors appear, confirm `CORS_ALLOWED_ORIGINS` in `settings.py` and the `Authorization` header scheme (Bearer vs Token).

## Quick PR guidance for AI agents
- When adding an endpoint or changing the DB schema: add serializer, migration and tests under the app; register ViewSet or URL in `src/seed2sale/urls.py`.
- When editing frontend API code, update `frontend/src/api/api.js` and adjust code in `frontend/src/api/*` helpers for authentication and endpoint URLs.
- Add a small integration test (Django test + optional front-end test) that covers your change in the lowest-cost manner.

## Where to look for examples
- Examples of API ViewSet patterns: `src/api/views.py`.
- Models and DRF mapping: `src/products/models.py`, `src/products/serializers.py`.
- Example frontend API pattern: `frontend/src/api/api.js`, `frontend/src/api/auth.js`.
- Seed script: `src/seed2sale/seed.py`.

---
If you need me to expand on a particular area (CI/Release, Docker, frontend-backend auth reconciliation, or to add a CONTRIBUTING.md), say which piece and I’ll add a follow-up PR with focused recommendations.
