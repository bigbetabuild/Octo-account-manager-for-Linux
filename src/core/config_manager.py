"""
Configuration manager for Roblox Account Manager
Handles all configuration file operations
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import yaml

logger = logging.getLogger(__name__)

@dataclass
class AppConfig:
    """Application configuration"""
    roblox_sober_path: str = "roblox-sober"
    theme: str = "dark"
    auto_launch_roblox: bool = False
    check_updates: bool = True
    remember_sessions: bool = True
    
class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "roblox-account-manager"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.accounts_file = self.config_dir / "accounts.json"
        self.profiles_file = self.config_dir / "profiles.json"
        self.settings_file = self.config_dir / "settings.yaml"
        self.sessions_file = self.config_dir / "sessions.json"
        
        # Create default config files if they don't exist
        self._init_default_files()
    
    def _init_default_files(self):
        """Initialize default configuration files"""
        if not self.settings_file.exists():
            default_config = asdict(AppConfig())
            with open(self.settings_file, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            logger.info("Created default settings file")
        
        if not self.accounts_file.exists():
            with open(self.accounts_file, 'w') as f:
                json.dump({"accounts": []}, f, indent=2)
        
        if not self.profiles_file.exists():
            with open(self.profiles_file, 'w') as f:
                json.dump({"profiles": []}, f, indent=2)
        
        if not self.sessions_file.exists():
            with open(self.sessions_file, 'w') as f:
                json.dump({"sessions": []}, f, indent=2)
    
    def get_settings(self) -> Dict[str, Any]:
        """Load application settings"""
        try:
            with open(self.settings_file, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return asdict(AppConfig())
    
    def save_settings(self, settings: Dict[str, Any]):
        """Save application settings"""
        try:
            with open(self.settings_file, 'w') as f:
                yaml.dump(settings, f, default_flow_style=False)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get_accounts(self) -> list:
        """Load all accounts"""
        try:
            with open(self.accounts_file, 'r') as f:
                data = json.load(f)
                return data.get("accounts", [])
        except Exception as e:
            logger.error(f"Error loading accounts: {e}")
            return []
    
    def save_accounts(self, accounts: list):
        """Save all accounts"""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump({"accounts": accounts}, f, indent=2)
            logger.info("Accounts saved successfully")
        except Exception as e:
            logger.error(f"Error saving accounts: {e}")
    
    def get_profiles(self) -> list:
        """Load all profiles"""
        try:
            with open(self.profiles_file, 'r') as f:
                data = json.load(f)
                return data.get("profiles", [])
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
            return []
    
    def save_profiles(self, profiles: list):
        """Save all profiles"""
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump({"profiles": profiles}, f, indent=2)
            logger.info("Profiles saved successfully")
        except Exception as e:
            logger.error(f"Error saving profiles: {e}")
    
    def get_sessions(self) -> list:
        """Load saved sessions"""
        try:
            with open(self.sessions_file, 'r') as f:
                data = json.load(f)
                return data.get("sessions", [])
        except Exception as e:
            logger.error(f"Error loading sessions: {e}")
            return []
    
    def save_sessions(self, sessions: list):
        """Save sessions"""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump({"sessions": sessions}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving sessions: {e}")
