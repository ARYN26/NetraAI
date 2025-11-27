"""User model for OTP-based authentication."""
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
import json
from pathlib import Path


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr


class OTPRequest(BaseModel):
    """Schema for requesting OTP."""
    email: EmailStr


class OTPVerify(BaseModel):
    """Schema for verifying OTP."""
    email: EmailStr
    code: str


class UserInDB(UserBase):
    """User schema as stored in database."""
    id: str
    created_at: datetime
    is_active: bool = True


class UserResponse(UserBase):
    """User schema for API responses."""
    id: str
    created_at: datetime
    is_active: bool = True


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[str] = None


class OTPEntry(BaseModel):
    """OTP storage entry."""
    email: str
    code: str
    expires_at: datetime
    used: bool = False


# Simple JSON file-based user storage
USERS_FILE = Path(__file__).parent.parent.parent / "users.json"
OTP_FILE = Path(__file__).parent.parent.parent / "otps.json"


def _load_users() -> dict:
    """Load users from JSON file."""
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_users(users: dict) -> None:
    """Save users to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2, default=str)


def _load_otps() -> dict:
    """Load OTPs from JSON file."""
    if OTP_FILE.exists():
        with open(OTP_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_otps(otps: dict) -> None:
    """Save OTPs to JSON file."""
    with open(OTP_FILE, "w") as f:
        json.dump(otps, f, indent=2, default=str)


def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Get user by email."""
    users = _load_users()
    user_data = users.get(email.lower())
    if user_data:
        return UserInDB(**user_data)
    return None


def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Get user by ID."""
    users = _load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            return UserInDB(**user_data)
    return None


def create_user(email: str) -> UserInDB:
    """Create a new user (OTP-based, no password)."""
    import uuid

    users = _load_users()
    user_id = str(uuid.uuid4())
    now = datetime.utcnow()

    user_in_db = UserInDB(
        id=user_id,
        email=email.lower(),
        created_at=now,
        is_active=True,
    )

    users[email.lower()] = user_in_db.model_dump()
    _save_users(users)

    return user_in_db


def save_otp(email: str, code: str, expires_at: datetime) -> None:
    """Save OTP for email."""
    otps = _load_otps()
    otps[email.lower()] = {
        "email": email.lower(),
        "code": code,
        "expires_at": expires_at.isoformat(),
        "used": False,
    }
    _save_otps(otps)


def get_otp(email: str) -> Optional[dict]:
    """Get OTP entry for email."""
    otps = _load_otps()
    return otps.get(email.lower())


def mark_otp_used(email: str) -> None:
    """Mark OTP as used."""
    otps = _load_otps()
    if email.lower() in otps:
        otps[email.lower()]["used"] = True
        _save_otps(otps)


def delete_otp(email: str) -> None:
    """Delete OTP for email."""
    otps = _load_otps()
    if email.lower() in otps:
        del otps[email.lower()]
        _save_otps(otps)
