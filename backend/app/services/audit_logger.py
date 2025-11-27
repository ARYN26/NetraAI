"""Security audit logging service."""
from datetime import datetime
from loguru import logger


class AuditLogger:
    """Centralized security audit logging for tracking auth events and suspicious activity."""

    @staticmethod
    def log_auth_attempt(email: str, success: bool, ip: str = "unknown"):
        """Log authentication attempts (OTP verification)."""
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"AUTH_ATTEMPT | {status} | email={email} | ip={ip} | time={datetime.utcnow().isoformat()}")

    @staticmethod
    def log_otp_request(email: str, ip: str = "unknown"):
        """Log OTP code requests."""
        logger.info(f"OTP_REQUEST | email={email} | ip={ip} | time={datetime.utcnow().isoformat()}")

    @staticmethod
    def log_rate_limit(endpoint: str, ip: str):
        """Log rate limit violations."""
        logger.warning(f"RATE_LIMIT_EXCEEDED | endpoint={endpoint} | ip={ip} | time={datetime.utcnow().isoformat()}")

    @staticmethod
    def log_suspicious_activity(activity: str, ip: str = "unknown", details: str = ""):
        """Log suspicious activities like brute force attempts."""
        logger.warning(f"SUSPICIOUS | {activity} | ip={ip} | details={details} | time={datetime.utcnow().isoformat()}")

    @staticmethod
    def log_lockout(email: str, ip: str = "unknown"):
        """Log account lockouts due to too many failed attempts."""
        logger.warning(f"ACCOUNT_LOCKOUT | email={email} | ip={ip} | time={datetime.utcnow().isoformat()}")


# Global audit logger instance
audit = AuditLogger()
