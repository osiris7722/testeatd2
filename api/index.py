"""Vercel Serverless entrypoint.

Vercel's Python runtime works best with handlers under /api.
We simply expose the Flask WSGI app from app.py.
"""

from app import app  # noqa: F401
