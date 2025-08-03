"""Application configuration settings."""

from typing import List
import os


def _get_allowed_origins() -> List[str]:
    """Return a list of allowed origins for CORS.

    The value is read from the ``ALLOWED_ORIGINS`` environment variable, which
    should contain a comma-separated list of origins. If the variable is not
    set, the default development origin is used.
    """

    raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


# Expose the configured origins as a constant for importers.
ALLOWED_ORIGINS = _get_allowed_origins()

