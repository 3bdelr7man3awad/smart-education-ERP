from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} "
            f"completed in {process_time:.2f}s "
            f"with status {response.status_code}"
        )
        
        return response 