"""
Cryptography utilities for secure credential storage
"""

import logging
from cryptography.fernet import Fernet
from pathlib import Path

logger = logging.getLogger(__name__)

class CryptoManager:
    """Handles encryption and decryption of credentials"""
    
    def __init__(self):
        self.key_file = Path.home() / ".config" / "roblox-account-manager" / ".key"
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self) -> bytes:
        """Load existing key or create new one"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            # Secure file permissions (read/write for owner only)
            self.key_file.touch(mode=0o600)
            with open(self.key_file, 'wb') as f:
                f.write(key)
            logger.info("Created new encryption key")
            return key
    
    def encrypt(self, data: str) -> str:
        """Encrypt a string"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
