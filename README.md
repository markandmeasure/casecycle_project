# CaseCycle Project

This repository contains a FastAPI backend and a React frontend.

## Frontend

The React app resides in the `frontend` directory. It includes a single page with a **Fetch Opportunities** button that requests `/opportunities` from the backend.

### Development

```bash
cd frontend
npm install
npm run dev
```

## Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Once the server reports `Uvicorn running on http://127.0.0.1:8000`, check that
it is serving the health endpoint in another terminal:

```bash
curl http://127.0.0.1:8000/healthcheck
```

If this returns `{"status": "ok"}`, the backend is running correctly. A 404
usually means another process is still bound to port 8000 or the server was
started from a different directory. You can look for lingering processes with
`lsof -i:8000` and stop them before restarting `uvicorn`.

### Sample data

Populate the database with example opportunities:

```bash
python populate_sample_data.py
```

Running the script is safe to repeat; each opportunity is upserted so duplicates
are not created. Alternatively, the script runs automatically when the server
starts if the ``ENVIRONMENT`` environment variable is set to ``development``:

```bash
ENVIRONMENT=development uvicorn main:app --reload
```

### API endpoints

The backend exposes a simple REST API for working with opportunities:

- `GET /opportunities/` – list opportunities.
- `POST /opportunities/` – create a new opportunity.
- `GET /opportunities/{id}` – retrieve a single opportunity.
- `PUT /opportunities/{id}` / `PATCH /opportunities/{id}` – update an existing opportunity.
- `DELETE /opportunities/{id}` – remove an opportunity.

## Troubleshooting

### Frontend shows "Unable to fetch opportunities"

This message appears when the request to `/opportunities/` fails or returns
something other than JSON.

1. Verify the backend is running and `curl http://127.0.0.1:8000/opportunities/`
   returns a JSON array.
2. Check the browser developer tools (Network tab) for the request details.
   A 404 usually means the server was started from the wrong directory or a
   proxy is misconfigured.
3. Make sure no leftover `uvicorn` processes are using port 8000; stop them with
   `lsof -i:8000` followed by `kill <PID>` if needed.
