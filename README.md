# SmrtSummary

SmrtSummary turns long CCTV footage into a visual scanline report. It samples video frames, builds a vertical slice that highlights changing patterns over time, and lets you jump to event timestamps instead of scrubbing through hours of video.

**Live demo:** https://smrtsummary.herokuapp.com/

## How it works

1. Upload a video (MP4, AVI, MOV, MKV, WMV).
2. A background worker extracts up to 500 frames with OpenCV and stores them as compressed NumPy arrays.
3. Pick a horizontal scanline on the interactive canvas to generate a summary image.
4. Click timestamps on the summary to inspect individual frames.

## Architecture

| Layer | Stack |
|-------|-------|
| Backend | Django 4.2, django-ninja REST API, PostgreSQL |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Jobs | django-rq + Redis (falls back to synchronous processing locally) |
| Media | AWS S3 via django-storages (falls back to local `media/` in dev) |
| Static | WhiteNoise |
| Deploy | Heroku (web + worker dynos) |

### Routes

| Path | Purpose |
|------|---------|
| `/` | Public landing page (Django templates) |
| `/app/` | React SPA — dashboard, upload, scanline, summary |
| `/api/` | JSON API (auth, videos, processing status) |
| `/dashboard/` | Legacy server-rendered views (still available) |
| `/accounts/` | Session-based auth (login, register, logout) |
| `/health/` | Health check endpoint |

## Project layout

```
SmrtSummary/
├── manage.py
├── requirements.txt          # Python deps
├── requirements-dev.txt      # + coverage for tests
├── Procfile                  # web, worker, release migrate
├── runtime.txt               # Python 3.10.2
├── Aptfile                   # OpenCV system libs (Heroku)
├── frontend/                 # React SPA (Vite)
├── SmrtSummary/              # Django project (settings, urls)
├── dashboard/                # Video model, API, processing services
├── accounts/                 # Auth views
├── pages/                    # Landing page
├── templates/                # Django HTML templates
└── SmrtSummary/static/       # Tailwind CSS + built frontend assets
```

## Local development

### Prerequisites

- Python 3.10.2
- Node.js 20+
- PostgreSQL
- Redis (optional — without it, video processing runs inline)

### Setup

```bash
git clone https://github.com/husseinshaltout/SmrtSummary.git
cd SmrtSummary

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements-dev.txt
```

Create a PostgreSQL database and export connection vars (or rely on defaults in `settings.py`):

```bash
export DB_NAME=smrtsummarydb
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

### Frontend

Build the React app into `SmrtSummary/static/frontend/` (served by Django at `/app/`):

```bash
npm ci --prefix frontend
npm run build --prefix frontend
```

For hot reload during frontend work, run Vite separately (proxies API calls to Django):

```bash
npm run dev --prefix frontend
```

Rebuild landing-page Tailwind CSS after editing `SmrtSummary/static/src/input.css`:

```bash
npm ci
npm run build-css
```

### Background worker

When `REDIS_URL` is set, uploads are processed asynchronously:

```bash
export REDIS_URL=redis://localhost:6379/0
python manage.py rqworker default
```

Without Redis, processing runs synchronously in the web process.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SECRET_KEY` | Production | Django secret key |
| `DJANGO_DEBUG` | No | `True` (default) or `False` |
| `DATABASE_URL` | Heroku | Full Postgres URL (overrides `DB_*` vars) |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | No | Local Postgres connection |
| `AWS_ACCESS_KEY_ID` | S3 | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | S3 | AWS credentials |
| `AWS_STORAGE_BUCKET_NAME` | S3 | S3 bucket name |
| `AWS_S3_REGION_NAME` | S3 | AWS region |
| `AWS_URL` | S3 | S3 bucket base URL |
| `AWS_S3_SIGNED_URL_EXPIRY` | No | Signed URL TTL in seconds (default `3600`) |
| `REDIS_URL` | No | Redis connection for background jobs |
| `ALLOWED_HOSTS` | No | Comma-separated hostnames |
| `CSRF_TRUSTED_ORIGINS` | No | Comma-separated origins for CSRF |
| `SENTRY_DSN` | No | Sentry error reporting |
| `LOG_LEVEL` | No | Logging level (default `INFO`) |

When AWS credentials are absent, media files are stored locally under `media/`.

## Tests

```bash
npm ci --prefix frontend && npm run build --prefix frontend
npm ci && npm run build-css

export DJANGO_SETTINGS_MODULE=SmrtSummary.test_settings
export DJANGO_SECRET_KEY=ci-secret-key
python manage.py migrate --noinput
python manage.py collectstatic --noinput
coverage run manage.py test && coverage report -i
```

CI runs on push/PR to `develop` and `master`, with deploy to Heroku on push to `master`.

## Deployment

Heroku needs three process types (see `Procfile`):

- **web** — gunicorn
- **worker** — `rqworker` for video processing
- **release** — migrations on deploy

Add the Heroku Postgres and Redis add-ons, set AWS env vars for S3 media storage, and configure `DJANGO_SECRET_KEY` with `DJANGO_DEBUG=False`.

## Authors

- [@husseinshaltout](https://github.com/husseinshaltout)

## License

[MIT](https://choosealicense.com/licenses/mit/)
