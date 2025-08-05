"""
API routes package
Contains all FastAPI route handlers for different endpoints
"""

from . import wallet, kyc, assets, rewards, mirror

__all__ = ["wallet", "kyc", "assets", "rewards", "mirror"]
