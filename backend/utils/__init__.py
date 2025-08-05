"""
Utilities package
Contains configuration, authentication, and helper utilities
"""

from .config import settings

# Import auth functions only when needed to avoid circular imports
# from .auth import (
#     verify_password, get_password_hash, create_access_token,
#     verify_token, get_current_user, get_current_active_user,
#     get_current_kyc_verified_user, create_user_token
# )

__all__ = [
    "settings"
]
