"""
Account management functionality
"""

import logging
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from src.utils.crypto import CryptoManager
from src.core.config_manager import ConfigManager

logger = logging.getLogger(__name__)

class Account:
    """Represents a Roblox account"""
    
    def __init__(self, username: str, password: str, profile: str = "Default", 
                 account_id: str = None, created_at: str = None, last_used: str = None):
        self.id = account_id or str(uuid.uuid4())
        self.username = username
        self.password = password
        self.profile = profile
        self.created_at = created_at or datetime.now().isoformat()
        self.last_used = last_used or ""
        self.notes = ""
        self.is_active = True
    
    def to_dict(self) -> Dict:
        """Convert account to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "profile": self.profile,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "notes": self.notes,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Account':
        """Create account from dictionary"""
        account = cls(
            username=data.get("username"),
            password=data.get("password"),
            profile=data.get("profile", "Default"),
            account_id=data.get("id"),
            created_at=data.get("created_at"),
            last_used=data.get("last_used")
        )
        account.notes = data.get("notes", "")
        account.is_active = data.get("is_active", True)
        return account

class AccountManager:
    """Manages Roblox accounts"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.crypto_manager = CryptoManager()
        self.accounts: List[Account] = self._load_accounts()
    
    def _load_accounts(self) -> List[Account]:
        """Load accounts from config"""
        accounts_data = self.config_manager.get_accounts()
        accounts = []
        for data in accounts_data:
            try:
                account = Account.from_dict(data)
                # Decrypt password
                account.password = self.crypto_manager.decrypt(account.password)
                accounts.append(account)
            except Exception as e:
                logger.error(f"Error loading account {data.get('username')}: {e}")
        return accounts
    
    def _save_accounts(self):
        """Save accounts to config"""
        accounts_data = []
        for account in self.accounts:
            data = account.to_dict()
            # Encrypt password before saving
            data["password"] = self.crypto_manager.encrypt(account.password)
            accounts_data.append(data)
        self.config_manager.save_accounts(accounts_data)
    
    def add_account(self, username: str, password: str, profile: str = "Default", notes: str = "") -> Account:
        """Add a new account"""
        # Validate inputs
        if not username or not password:
            raise ValueError("Username and password are required")
        
        # Check for duplicate
        if any(acc.username == username for acc in self.accounts):
            raise ValueError(f"Account '{username}' already exists")
        
        account = Account(username, password, profile)
        account.notes = notes
        self.accounts.append(account)
        self._save_accounts()
        logger.info(f"Account added: {username}")
        return account
    
    def update_account(self, account_id: str, **kwargs) -> Optional[Account]:
        """Update an account"""
        account = self.get_account_by_id(account_id)
        if not account:
            return None
        
        for key, value in kwargs.items():
            if hasattr(account, key) and value is not None:
                setattr(account, key, value)
        
        self._save_accounts()
        logger.info(f"Account updated: {account.username}")
        return account
    
    def delete_account(self, account_id: str) -> bool:
        """Delete an account"""
        account = self.get_account_by_id(account_id)
        if not account:
            return False
        
        self.accounts.remove(account)
        self._save_accounts()
        logger.info(f"Account deleted: {account.username}")
        return True
    
    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """Get account by ID"""
        return next((acc for acc in self.accounts if acc.id == account_id), None)
    
    def get_account_by_username(self, username: str) -> Optional[Account]:
        """Get account by username"""
        return next((acc for acc in self.accounts if acc.username == username), None)
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts"""
        return self.accounts
    
    def get_accounts_by_profile(self, profile: str) -> List[Account]:
        """Get accounts in a specific profile"""
        return [acc for acc in self.accounts if acc.profile == profile]
    
    def mark_as_used(self, account_id: str):
        """Mark account as recently used"""
        account = self.get_account_by_id(account_id)
        if account:
            account.last_used = datetime.now().isoformat()
            self._save_accounts()
