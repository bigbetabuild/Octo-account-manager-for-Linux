"""
Input validation utilities
"""

import re
import logging

logger = logging.getLogger(__name__)

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate Roblox username format"""
        if not username:
            return False
        # Roblox usernames are 3-20 characters, alphanumeric and underscore
        if len(username) < 3 or len(username) > 20:
            return False
        return bool(re.match(r"^[a-zA-Z0-9_]+$", username))
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength"""
        if not password:
            return False
        if len(password) < 6:
            return False
        return True
    
    @staticmethod
    def validate_profile_name(profile_name: str) -> bool:
        """Validate profile name"""
        if not profile_name:
            return False
        if len(profile_name) > 50:
            return False
        return bool(re.match(r"^[a-zA-Z0-9_\-\s]+$", profile_name))
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename"""
        return re.sub(r"[^a-zA-Z0-9_\-.]", "", filename)
