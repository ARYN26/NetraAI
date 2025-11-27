"""Authentication service - OTP-based authentication with JWT."""
import random
import string
from datetime import datetime, timedelta
from typing import Optional

from cachetools import TTLCache
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from app.config import settings
from app.models.user import (
    UserInDB,
    TokenData,
    get_user_by_email,
    get_user_by_id,
    create_user as db_create_user,
    save_otp,
    get_otp,
    delete_otp,
)
from app.services.email_service import send_otp_email
from app.services.audit_logger import audit


# Track failed OTP attempts per email (max 5 before lockout, 1 hour TTL)
_failed_attempts: TTLCache = TTLCache(maxsize=10000, ttl=3600)


# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/verify-otp", auto_error=False)


def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return "".join(random.choices(string.digits, k=6))


def request_otp(email: str) -> bool:
    """
    Generate and send OTP to email.

    Returns True if OTP was sent successfully.
    """
    # Generate OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)

    # Save OTP to storage
    save_otp(email, otp_code, expires_at)

    # Send email
    success = send_otp_email(email, otp_code)

    if success:
        logger.info(f"OTP sent to {email}")
    else:
        logger.error(f"Failed to send OTP to {email}")

    return success


def verify_otp(email: str, code: str, ip: str = "unknown") -> Optional[UserInDB]:
    """
    Verify OTP code for email.

    Returns the user if OTP is valid, None otherwise.
    Creates new user if they don't exist.
    Tracks failed attempts and locks out after 5 failures.
    """
    email_lower = email.lower()

    # Check if locked out due to too many failed attempts
    attempts = _failed_attempts.get(email_lower, 0)
    if attempts >= 5:
        audit.log_lockout(email, ip)
        audit.log_suspicious_activity("OTP_BRUTE_FORCE", ip, f"email={email}")
        logger.warning(f"Account locked out: {email} (too many failed attempts)")
        return None

    otp_entry = get_otp(email)

    if not otp_entry:
        logger.warning(f"No OTP found for {email}")
        _failed_attempts[email_lower] = attempts + 1
        audit.log_auth_attempt(email, False, ip)
        return None

    # Check if already used
    if otp_entry.get("used", False):
        logger.warning(f"OTP already used for {email}")
        _failed_attempts[email_lower] = attempts + 1
        audit.log_auth_attempt(email, False, ip)
        return None

    # Check if expired
    expires_at = datetime.fromisoformat(otp_entry["expires_at"])
    if datetime.utcnow() > expires_at:
        logger.warning(f"OTP expired for {email}")
        delete_otp(email)
        _failed_attempts[email_lower] = attempts + 1
        audit.log_auth_attempt(email, False, ip)
        return None

    # Check code
    if otp_entry["code"] != code:
        logger.warning(f"Invalid OTP code for {email}")
        _failed_attempts[email_lower] = attempts + 1
        audit.log_auth_attempt(email, False, ip)
        return None

    # OTP is valid - delete it and clear failed attempts
    delete_otp(email)
    _failed_attempts.pop(email_lower, None)

    # Get or create user
    user = get_user_by_email(email)
    if not user:
        user = db_create_user(email)
        logger.info(f"Created new user: {email}")

    audit.log_auth_attempt(email, True, ip)
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[UserInDB]:
    """Get the current user from the JWT token."""
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        token_data = TokenData(user_id=user_id)
    except JWTError:
        return None

    user = get_user_by_id(token_data.user_id)
    return user


async def get_current_active_user(
    current_user: Optional[UserInDB] = Depends(get_current_user)
) -> UserInDB:
    """Get the current active user (required authentication)."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
