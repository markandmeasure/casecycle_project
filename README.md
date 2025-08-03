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
