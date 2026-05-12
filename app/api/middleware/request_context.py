"""Request context helpers."""

from __future__ import annotations

from app.core.constants import REQUEST_ID_HEADER
from app.core.security import generate_request_id

try:
    from starlette.middleware.base import BaseHTTPMiddleware
except ImportError:  # pragma: no cover - API is optional
    BaseHTTPMiddleware = object


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):  # pragma: no cover - thin integration wrapper
        request_id = request.headers.get(REQUEST_ID_HEADER, generate_request_id())
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
