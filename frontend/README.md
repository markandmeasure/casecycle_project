# CaseCycle Frontend

This React application communicates with the CaseCycle FastAPI backend to list
and create opportunities.

## Development

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server (requires the backend running on
   `http://127.0.0.1:8000`):
   ```bash
   npm run dev
   ```

The app is served at `http://localhost:5173` and proxies API requests to the
backend.

## Interface

- Opportunities are fetched from `/opportunities/` using `skip` and `limit`
  parameters. Prev/Next buttons allow paging through results.
- A textarea accepts JSON to create a new opportunity. Required fields include
  `title`, `market_description`, `tam_estimate`, `growth_rate`,
  `consumer_insight`, and `hypothesis`. Numeric values are validated.
- Errors such as invalid JSON, missing fields, or network failures display an
  inline message (e.g., "Invalid JSON format" or "Unable to fetch
  opportunities").

