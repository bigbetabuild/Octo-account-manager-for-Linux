"""
Roblox Account Manager for Linux
Multi-instance account manager with GUI
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui.main_window import RobloxAccountManagerApp
import logging

def setup_logging():
    """Configure application logging"""
    log_dir = Path.home() / ".config" / "roblox-account-manager"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Roblox Account Manager for Linux")
    
    app = RobloxAccountManagerApp()
    sys.exit(app.run())
