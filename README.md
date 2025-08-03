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
