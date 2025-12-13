"""Rate limiting configuration with proxy support."""
import os
from slowapi import Limiter
from slowapi.util import get_remote_address


# Only trust proxy headers in production (behind Railway/Render/etc.)
# In development, use direct connection IP to prevent spoofing
TRUST_PROXY_HEADERS = os.getenv("ENVIRONMENT", "development").lower() == "production"


def get_real_client_ip(request) -> str:
    """
    Get the real client IP address, with proxy header support in production.

    Security considerations:
    - In development: Only use direct connection IP (X-Forwarded-For can be spoofed)
    - In production: Trust X-Forwarded-For because Railway/Render proxies set it

    Railway and Render strip/override X-Forwarded-For, so we can trust the first IP.
    """
    if TRUST_PROXY_HEADERS:
        # Production: trust proxy headers (Railway/Render set these securely)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For format: "client, proxy1, proxy2"
            # The first IP is the original client
            client_ip = forwarded_for.split(",")[0].strip()
            # Basic validation: must look like an IP
            if client_ip and "." in client_ip or ":" in client_ip:
                return client_ip

        # Check for X-Real-IP (alternative header)
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            clean_ip = real_ip.strip()
            if clean_ip and "." in clean_ip or ":" in clean_ip:
                return clean_ip

    # Development or fallback: use direct connection IP
    return get_remote_address(request)


# Rate limiter instance - shared across the application
# Uses custom key function for proxy compatibility
limiter = Limiter(key_func=get_real_client_ip)
