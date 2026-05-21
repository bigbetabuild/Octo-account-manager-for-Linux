"""
Session management for multi-instance launching
"""

import logging
import subprocess
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import psutil

logger = logging.getLogger(__name__)

@dataclass
class SessionInfo:
    """Information about an active Roblox session"""
    session_id: str
    account_username: str
    process_id: int
    start_time: str
    status: str  # "running", "stopped"
    cpu_percent: float = 0.0
    memory_mb: float = 0.0

class SessionManager:
    """Manages active Roblox instances"""
    
    def __init__(self, roblox_sober_path: str = "roblox-sober"):
        self.roblox_sober_path = roblox_sober_path
        self.active_sessions: Dict[str, SessionInfo] = {}
    
    def launch_account(self, username: str, password: str, session_id: str = None) -> Optional[SessionInfo]:
        """
        Launch Roblox Sober with a specific account
        Returns SessionInfo if successful
        """
        try:
            # Set environment variables for Roblox Sober
            env = os.environ.copy()
            env["ROBLOX_USERNAME"] = username
            env["ROBLOX_PASSWORD"] = password
            
            # Launch Roblox Sober
            process = subprocess.Popen(
                [self.roblox_sober_path],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setpgrp  # Create new process group for multi-instance
            )
            
            session_id = session_id or f"session_{process.pid}"
            session_info = SessionInfo(
                session_id=session_id,
                account_username=username,
                process_id=process.pid,
                start_time=datetime.now().isoformat(),
                status="running"
            )
            
            self.active_sessions[session_id] = session_info
            logger.info(f"Launched Roblox instance for {username} (PID: {process.pid})")
            return session_info
            
        except FileNotFoundError:
            logger.error(f"Roblox Sober not found at: {self.roblox_sober_path}")
            raise
        except Exception as e:
            logger.error(f"Error launching Roblox instance: {e}")
            raise
    
    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """Get information about an active session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        try:
            process = psutil.Process(session.process_id)
            
            if process.is_running():
                session.cpu_percent = process.cpu_percent(interval=0.1)
                session.memory_mb = process.memory_info().rss / (1024 * 1024)
                session.status = "running"
            else:
                session.status = "stopped"
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            session.status = "stopped"
        
        return session
    
    def stop_session(self, session_id: str) -> bool:
        """Stop a specific session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        try:
            process = psutil.Process(session.process_id)
            process.terminate()
            process.wait(timeout=5)
            session.status = "stopped"
            logger.info(f"Stopped session {session_id} (PID: {session.process_id})")
            return True
            
        except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied) as e:
            logger.error(f"Error stopping session: {e}")
            try:
                os.killpg(os.getpgid(session.process_id), 9)
                session.status = "stopped"
                return True
            except:
                return False
    
    def stop_all_sessions(self) -> int:
        """Stop all active sessions"""
        stopped_count = 0
        for session_id in list(self.active_sessions.keys()):
            if self.stop_session(session_id):
                stopped_count += 1
        return stopped_count
    
    def get_all_sessions(self) -> List[SessionInfo]:
        """Get information about all active sessions"""
        return [self.get_session_info(sid) for sid in self.active_sessions.keys()]
    
    def cleanup_dead_sessions(self):
        """Remove references to dead sessions"""
        dead_sessions = []
        for session_id, session in self.active_sessions.items():
            try:
                process = psutil.Process(session.process_id)
                if not process.is_running():
                    dead_sessions.append(session_id)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                dead_sessions.append(session_id)
        
        for session_id in dead_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Cleaned up dead session: {session_id}")
