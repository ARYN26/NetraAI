"""Rate limiting configuration with proxy support."""
from slowapi import Limiter
from slowapi.util import get_remote_address


def get_real_client_ip(request) -> str:
    """
    Get the real client IP address from behind a proxy.

    Railway, Render, and other cloud platforms use reverse proxies
    that set the X-Forwarded-For header. We need to trust this header
    to rate limit by actual client IP, not proxy IP.

    Security note: Only trust X-Forwarded-For in production environments
    where we know requests come through a trusted proxy.
    """
    # Check for forwarded header (set by Railway/Render proxies)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs: "client, proxy1, proxy2"
        # The first IP is the original client
        client_ip = forwarded_for.split(",")[0].strip()
        return client_ip

    # Check for X-Real-IP (alternative header used by some proxies)
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    # Fallback to direct connection IP (for local development)
    return get_remote_address(request)


# Rate limiter instance - shared across the application
# Uses custom key function for proxy compatibility
limiter = Limiter(key_func=get_real_client_ip)
