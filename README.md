# Seed2Sale — Local Development Quick Start

Seed2Sale is a Django + React application used to manage farmers, products, carts and orders.

This README covers the essential quick start steps for local development and highlights common pitfalls (auth scheme, frontend/backend integration, and seeding).

---

## Backend — Quick start (recommended: Poetry)

1) Install dependencies

```powershell
poetry install
```

Note: If you've updated `pyproject.toml` (for example, new dependencies), run:

```powershell
poetry lock
poetry install
```

2) Run migrations and create DB

```powershell
cd src
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

⚠️ Python version note (Windows): If you are developing on Windows and get errors while installing Pillow (or other compiled packages), make sure Poetry is using a Python version that has prebuilt wheels for those packages. For Pillow, prefer Python 3.12 or 3.11.

Example to switch your Poetry environment to Python 3.12 (after installing it on your system):

```powershell
poetry env use C:\\Path\\To\\Python312\\python.exe
poetry lock
poetry install
```
If you don't yet have Python 3.12 installed, you can download and install it from https://www.python.org/downloads/release/python-3120/. After installation, confirm available interpreters with:

```powershell
py -0p
```

Then point Poetry to the 3.12 interpreter using the `poetry env use` command shown above.

3) (Optional) Create a superuser

```powershell
poetry run python manage.py createsuperuser
```

4) (Optional) Seed demo data

```powershell
poetry run python seed2sale/seed.py
```

5) Run the server

```powershell
poetry run python manage.py runserver
```

If you DO NOT use Poetry, create a virtual environment and install `requirements.txt`:

```powershell
cd src
python -m venv .venv; .\.venv\Scripts\Activate
pip install -r ..\requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Notes:
- DB file `db.sqlite3` is included in the repo — be careful when seeding or resetting databases during development.
- Settings (CORS, JWT, STATIC) are in `src/seed2sale/settings.py`.
- The project looks for static files in `src/static` and repo-root `static/`. If you see a `STATICFILES_DIRS` warning, create a `src/static` folder or adjust `settings.py`.
- If you get a SystemCheckError complaining about `ImageField` (Pillow not installed), install Pillow:

  Poetry:
  ```powershell
  poetry add Pillow
  poetry lock
  poetry install
  ```

  Or venv + pip:
  ```powershell
  pip install Pillow
  ```

---

## Frontend — Quick start

1) Install dependencies and run the dev server:

```powershell
cd frontend
npm install
npm start
```

2) Tailwind (if working with static templates or the global `static/` files):

```powershell
npm run dev  # from repo root builds static/input.css -> static/output.css
# or, inside frontend
cd frontend
npm run dev:css
```

3) If using the static (non-React) HTML files (e.g. `frontend/auth.js`): set the API base `API` in `frontend/auth.js` or set `window.API_BASE` in the page to point to `http://127.0.0.1:8000`.

4) Frontend environment variables
- `REACT_APP_API_URL` (optional) can be used by the React app to point to the API during development.

---

## Authentication & API notes

- The backend uses `rest_framework_simplejwt`. Endpoints of interest:
  - `POST /api/token/` — returns `access` and `refresh` tokens
  - `POST /api/token/refresh/` — refreshes `access` token
  - `GET /api/auth/me/` — returns the current user
  - `POST /api/accounts/token/` — custom token view (email/phone identifier accepts `identifier` & `password`) when `accounts` URLs are included

- The frontend uses the `s2s_token` key in `localStorage` for the access token (see `frontend/src/api/api.js` and static `frontend/auth.js`). All API requests send `Authorization: Bearer <access token>`.

---

## Adding API endpoints (example flow)

To add a new resource (Django REST Framework):
1. Add the model in `src/<app>/models.py`.
2. Add a `Serializer` in `src/<app>/serializers.py`.
3. Add a `ModelViewSet` in `src/<app>/views.py`.
4. Register the ViewSet in `src/seed2sale/urls.py`:

```python
router.register(r'newmodels', NewModelViewSet)
```

5. Make migrations & migrate:

```powershell
cd src
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

---

## Tests

Run Django tests:

```powershell
cd src
poetry run python manage.py test
```

---

## Debugging & Troubleshooting

- CORS: check `CORS_ALLOWED_ORIGINS` and `CORS_ALLOW_ALL_ORIGINS` in `src/seed2sale/settings.py` if the frontend cannot reach API endpoints.
- Auth: verify `localStorage.s2s_token` and make a test curl or fetch using `Bearer` to `GET /api/auth/me/`.
- Duplicates: There were duplicate models earlier — rely on the condensed `src/products/models.py` file.

---

If you want, I can add CI GitHub Actions to run backend tests and a frontend build/lint step for pull requests, or add a `CONTRIBUTING.md` file with PR guidelines.
<!-- duplicate block removed -->

