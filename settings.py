"""Application configuration settings."""

from typing import List
import os


PRODUCTION_ORIGINS = ["https://casecycle.example.com"]


def _get_allowed_origins() -> List[str]:
    """Return a list of allowed origins for CORS.

    In production, only known origins are allowed. For other environments, the
    value is read from the ``ALLOWED_ORIGINS`` environment variable which should
    contain a comma-separated list of origins. If the variable is not set, the
    default development origin is used.
    """

    if os.getenv("ENVIRONMENT") == "production":
        return PRODUCTION_ORIGINS

    raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


# Expose the configured origins as a constant for importers.
ALLOWED_ORIGINS = _get_allowed_origins()

