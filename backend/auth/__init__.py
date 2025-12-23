"""OctoVision Authentication Module

Provides FastAPI-based user authentication with JWT tokens and role-based access control.
"""

from .main import app, get_current_user, admin_required
from .models import UserRegister, UserLogin, UserResponse, TokenResponse

__all__ = [
    "app",
    "get_current_user",
    "admin_required",
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
]
