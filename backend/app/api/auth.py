"""Authentication API routes - OTP-based."""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from loguru import logger

from app.config import settings
from app.models.user import OTPRequest, OTPVerify, UserResponse, Token, UserInDB
from app.services.audit_logger import audit
from app.services.rate_limiter import limiter
from app.services.auth_service import (
    request_otp,
    verify_otp,
    create_access_token,
    get_current_active_user,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


class OTPResponse(BaseModel):
    """Response for OTP request."""
    message: str
    email: str


@router.post("/request-otp", response_model=OTPResponse)
@limiter.limit("5/minute")  # Max 5 OTP requests per minute per IP
async def send_otp(request: Request, data: OTPRequest):
    """
    Request an OTP code to be sent to email.

    The code will expire in 5 minutes.
    Rate limited to 5 requests per minute per IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    audit.log_otp_request(data.email, client_ip)
    logger.info(f"OTP requested for: {data.email}")

    success = request_otp(data.email)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification code. Please check email configuration."
        )

    return OTPResponse(
        message="Verification code sent to your email",
        email=data.email
    )


@router.post("/verify-otp", response_model=Token)
@limiter.limit("10/minute")  # Max 10 verification attempts per minute per IP
async def verify_otp_code(request: Request, data: OTPVerify):
    """
    Verify OTP code and return JWT access token.

    If user doesn't exist, they will be created automatically.
    Rate limited to 10 attempts per minute per IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"OTP verification attempt for: {data.email}")

    user = verify_otp(data.email, data.code, client_ip)

    if not user:
        logger.warning(f"Invalid OTP for: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification code",
        )

    logger.success(f"User authenticated: {user.email}")

    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Get current authenticated user's information.

    Requires valid JWT token.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        is_active=current_user.is_active,
    )
