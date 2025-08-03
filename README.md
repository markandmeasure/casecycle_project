# CaseCycle Project

CaseCycle combines a FastAPI backend with a React frontend for collecting and
reviewing market opportunities.

## Quick Start

### Backend

Start the API server:

```bash
uvicorn main:app --reload
```

The service listens on `http://127.0.0.1:8000`. Setting
`ENVIRONMENT=development` loads sample opportunities on startup, or run the
population script manually:

```bash
python populate_sample_data.py
```

### Frontend

In a separate terminal, launch the React app:

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server runs at `http://localhost:5173` and proxies API requests to
the backend.

## Expected Workflow

1. Start the backend and ensure the database contains sample data.
2. Run the frontend and open `http://localhost:5173` in a browser.
3. Browse existing opportunities, add new ones via the JSON form, and paginate
   through the list.
4. Use the `/prompt/{id}` endpoint to generate a text prompt for a specific
   opportunity.

## API Endpoints

- `GET /` – basic root endpoint returning `{"status": "ok"}`.
- `GET /healthcheck` – database connectivity check.
- `POST /users/` – create a user.
- `GET /users/` – list users.
- `POST /opportunities/` – create an opportunity.
- `GET /opportunities/` – list opportunities using `skip` and `limit`
  parameters for pagination.
- `GET /prompt/{opportunity_id}` – render a template-based prompt for the
  specified opportunity.

## Sample Data

`populate_sample_data.py` seeds the database with two example opportunities.
The script is idempotent, so it can be run repeatedly without creating
duplicates.

### API endpoints

The backend exposes a simple REST API for working with opportunities:

- `GET /opportunities/` – list opportunities.
- `POST /opportunities/` – create a new opportunity.
- `GET /opportunities/{id}` – retrieve a single opportunity.
- `PUT /opportunities/{id}` / `PATCH /opportunities/{id}` – update an existing opportunity.
- `DELETE /opportunities/{id}` – remove an opportunity.

## Deployment

Docker images are provided for both services. Build and start everything with Docker Compose:

```bash
docker compose build
docker compose up
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

To build individual images without starting containers:

```bash
# Backend
docker build -t casecycle-backend .

# Frontend
docker build -t casecycle-frontend ./frontend
```

## Deployment

Docker images are provided for both services. Build and start everything with Docker Compose:

```bash
docker compose build
docker compose up
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

To build individual images without starting containers:

```bash
# Backend
docker build -t casecycle-backend .

# Frontend
docker build -t casecycle-frontend ./frontend
```

## Troubleshooting

If the frontend displays “Unable to fetch opportunities,” ensure the backend is
running and `curl http://127.0.0.1:8000/opportunities/` returns a JSON array.
Check browser developer tools for request details and confirm no other process
is using port 8000.

