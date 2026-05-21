"""
Main application window and UI
"""

import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QTabWidget, QLabel,
    QDialog, QSpinBox, QComboBox, QMessageBox, QProgressBar,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QColor
from datetime import datetime

from src.core.account_manager import AccountManager
from src.core.session_manager import SessionManager
from src.core.config_manager import ConfigManager
from src.ui.account_dialog import AddAccountDialog, EditAccountDialog
from src.ui.styles import get_dark_stylesheet

logger = logging.getLogger(__name__)

class RobloxAccountManagerApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.account_manager = AccountManager()
        self.config_manager = ConfigManager()
        
        settings = self.config_manager.get_settings()
        self.session_manager = SessionManager(
            roblox_sober_path=settings.get("roblox_sober_path", "roblox-sober")
        )
        
        self.setWindowTitle("Roblox Account Manager for Linux")
        self.setGeometry(100, 100, 1200, 700)
        
        self._setup_ui()
        self._setup_timers()
        self._load_accounts()
        
        # Apply dark theme
        self.setStyleSheet(get_dark_stylesheet())
    
    def _setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left panel - Account list
        left_layout = QVBoxLayout()
        
        left_layout.addWidget(QLabel("Accounts"))
        self.account_list = QListWidget()
        self.account_list.itemSelectionChanged.connect(self._on_account_selected)
        left_layout.addWidget(self.account_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Account")
        add_btn.clicked.connect(self._on_add_account)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self._on_edit_account)
        self.edit_btn = edit_btn
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._on_delete_account)
        self.delete_btn = delete_btn
        button_layout.addWidget(delete_btn)
        
        left_layout.addLayout(button_layout)
        
        # Right panel - Tabs
        right_layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        
        # Quick Launch Tab
        self.quick_launch_tab = QWidget()
        self._setup_quick_launch_tab()
        self.tabs.addTab(self.quick_launch_tab, "Quick Launch")
        
        # Sessions Tab
        self.sessions_tab = QWidget()
        self._setup_sessions_tab()
        self.tabs.addTab(self.sessions_tab, "Active Sessions")
        
        # Settings Tab
        self.settings_tab = QWidget()
        self._setup_settings_tab()
        self.tabs.addTab(self.settings_tab, "Settings")
        
        right_layout.addWidget(self.tabs)
        
        # Add panels to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
    
    def _setup_quick_launch_tab(self):
        """Setup quick launch tab"""
        layout = QVBoxLayout()
        self.quick_launch_tab.setLayout(layout)
        
        layout.addWidget(QLabel("Account Details"))
        
        self.account_info_label = QLabel("Select an account to see details")
        layout.addWidget(self.account_info_label)
        
        layout.addWidget(QLabel("Launch Options"))
        
        layout.addWidget(QLabel("Number of instances:"))
        self.instance_spin = QSpinBox()
        self.instance_spin.setMinimum(1)
        self.instance_spin.setMaximum(10)
        self.instance_spin.setValue(1)
        layout.addWidget(self.instance_spin)
        
        launch_btn = QPushButton("Launch Selected Account")
        launch_btn.clicked.connect(self._on_launch_account)
        layout.addWidget(launch_btn)
        
        launch_all_btn = QPushButton("Launch All Accounts")
        launch_all_btn.clicked.connect(self._on_launch_all)
        layout.addWidget(launch_all_btn)
        
        layout.addStretch()
    
    def _setup_sessions_tab(self):
        """Setup sessions tab"""
        layout = QVBoxLayout()
        self.sessions_tab.setLayout(layout)
        
        layout.addWidget(QLabel("Active Sessions"))
        
        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(5)
        self.sessions_table.setHorizontalHeaderLabels(
            ["Account", "PID", "Status", "CPU %", "Memory (MB)"]
        )
        layout.addWidget(self.sessions_table)
        
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._update_sessions_display)
        button_layout.addWidget(refresh_btn)
        
        stop_btn = QPushButton("Stop Selected")
        stop_btn.clicked.connect(self._on_stop_session)
        self.stop_session_btn = stop_btn
        button_layout.addWidget(stop_btn)
        
        stop_all_btn = QPushButton("Stop All")
        stop_all_btn.clicked.connect(self._on_stop_all_sessions)
        button_layout.addWidget(stop_all_btn)
        
        layout.addLayout(button_layout)
    
    def _setup_settings_tab(self):
        """Setup settings tab"""
        layout = QVBoxLayout()
        self.settings_tab.setLayout(layout)
        
        layout.addWidget(QLabel("Roblox Sober Path"))
        self.roblox_path_edit = QComboBox()
        self.roblox_path_edit.addItems([
            "roblox-sober",
            "/usr/bin/roblox-sober",
            "/usr/local/bin/roblox-sober",
            "~/.local/bin/roblox-sober"
        ])
        layout.addWidget(self.roblox_path_edit)
        
        save_settings_btn = QPushButton("Save Settings")
        save_settings_btn.clicked.connect(self._on_save_settings)
        layout.addWidget(save_settings_btn)
        
        layout.addStretch()
    
    def _load_accounts(self):
        """Load and display accounts"""
        self.account_list.clear()
        accounts = self.account_manager.get_all_accounts()
        
        for account in accounts:
            item = QListWidgetItem(account.username)
            item.setData(Qt.ItemDataRole.UserRole, account.id)
            self.account_list.addItem(item)
    
    def _on_account_selected(self):
        """Handle account selection"""
        current_item = self.account_list.currentItem()
        if current_item:
            account_id = current_item.data(Qt.ItemDataRole.UserRole)
            account = self.account_manager.get_account_by_id(account_id)
            
            if account:
                info_text = f"""
Account: {account.username}
Profile: {account.profile}
Created: {account.created_at}
Last Used: {account.last_used or 'Never'}
Notes: {account.notes}
                """
                self.account_info_label.setText(info_text)
                self.edit_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
        else:
            self.account_info_label.setText("Select an account to see details")
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def _on_add_account(self):
        """Open add account dialog"""
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password, profile, notes = dialog.get_values()
            try:
                self.account_manager.add_account(username, password, profile, notes)
                self._load_accounts()
                QMessageBox.information(self, "Success", f"Account '{username}' added successfully!")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
            except Exception as e:
                logger.error(f"Error adding account: {e}")
                QMessageBox.critical(self, "Error", f"Failed to add account: {str(e)}")
    
    def _on_edit_account(self):
        """Open edit account dialog"""
        current_item = self.account_list.currentItem()
        if not current_item:
            return
        
        account_id = current_item.data(Qt.ItemDataRole.UserRole)
        account = self.account_manager.get_account_by_id(account_id)
        
        if account:
            dialog = EditAccountDialog(self, account)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                username, password, profile, notes = dialog.get_values()
                try:
                    self.account_manager.update_account(
                        account_id,
                        username=username,
                        password=password,
                        profile=profile,
                        notes=notes
                    )
                    self._load_accounts()
                    QMessageBox.information(self, "Success", "Account updated successfully!")
                except Exception as e:
                    logger.error(f"Error updating account: {e}")
                    QMessageBox.critical(self, "Error", f"Failed to update account: {str(e)}")
    
    def _on_delete_account(self):
        """Delete selected account"""
        current_item = self.account_list.currentItem()
        if not current_item:
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{current_item.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            account_id = current_item.data(Qt.ItemDataRole.UserRole)
            if self.account_manager.delete_account(account_id):
                self._load_accounts()
                QMessageBox.information(self, "Success", "Account deleted successfully!")
    
    def _on_launch_account(self):
        """Launch selected account"""
        current_item = self.account_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select an account to launch")
            return
        
        account_id = current_item.data(Qt.ItemDataRole.UserRole)
        account = self.account_manager.get_account_by_id(account_id)
        
        if account:
            num_instances = self.instance_spin.value()
            try:
                for i in range(num_instances):
                    self.session_manager.launch_account(
                        account.username,
                        account.password,
                        f"session_{account.id}_{i}"
                    )
                
                self.account_manager.mark_as_used(account_id)
                QMessageBox.information(
                    self, "Success",
                    f"Launched {num_instances} instance(s) for {account.username}"
                )
                self._update_sessions_display()
            except Exception as e:
                logger.error(f"Error launching account: {e}")
                QMessageBox.critical(self, "Error", f"Failed to launch: {str(e)}")
    
    def _on_launch_all(self):
        """Launch all accounts"""
        accounts = self.account_manager.get_all_accounts()
        if not accounts:
            QMessageBox.warning(self, "Warning", "No accounts to launch")
            return
        
        try:
            for account in accounts:
                self.session_manager.launch_account(account.username, account.password)
            
            QMessageBox.information(
                self, "Success",
                f"Launched {len(accounts)} account(s)"
            )
            self._update_sessions_display()
        except Exception as e:
            logger.error(f"Error launching accounts: {e}")
            QMessageBox.critical(self, "Error", f"Failed to launch: {str(e)}")
    
    def _update_sessions_display(self):
        """Update the sessions table"""
        self.session_manager.cleanup_dead_sessions()
        sessions = self.session_manager.get_all_sessions()
        
        self.sessions_table.setRowCount(0)
        
        for session in sessions:
            if session:
                row = self.sessions_table.rowCount()
                self.sessions_table.insertRow(row)
                
                self.sessions_table.setItem(row, 0, QTableWidgetItem(session.account_username))
                self.sessions_table.setItem(row, 1, QTableWidgetItem(str(session.process_id)))
                self.sessions_table.setItem(row, 2, QTableWidgetItem(session.status))
                self.sessions_table.setItem(row, 3, QTableWidgetItem(f"{session.cpu_percent:.1f}%"))
                self.sessions_table.setItem(row, 4, QTableWidgetItem(f"{session.memory_mb:.1f}"))
    
    def _on_stop_session(self):
        """Stop selected session"""
        current_row = self.sessions_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a session to stop")
            return
        
        # Get session from table
        account_name = self.sessions_table.item(current_row, 0).text()
        pid = int(self.sessions_table.item(current_row, 1).text())
        
        # Find and stop the session
        for session_id, session in self.session_manager.active_sessions.items():
            if session.process_id == pid:
                if self.session_manager.stop_session(session_id):
                    QMessageBox.information(self, "Success", f"Stopped session for {account_name}")
                    self._update_sessions_display()
                break
    
    def _on_stop_all_sessions(self):
        """Stop all active sessions"""
        if not self.session_manager.active_sessions:
            QMessageBox.warning(self, "Warning", "No active sessions to stop")
            return
        
        reply = QMessageBox.question(
            self, "Confirm",
            "Stop all active sessions?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            count = self.session_manager.stop_all_sessions()
            QMessageBox.information(self, "Success", f"Stopped {count} session(s)")
            self._update_sessions_display()
    
    def _on_save_settings(self):
        """Save application settings"""
        try:
            settings = self.config_manager.get_settings()
            settings["roblox_sober_path"] = self.roblox_path_edit.currentText()
            self.config_manager.save_settings(settings)
            
            # Update session manager
            self.session_manager.roblox_sober_path = settings["roblox_sober_path"]
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
    
    def _setup_timers(self):
        """Setup periodic update timers"""
        self.sessions_update_timer = QTimer()
        self.sessions_update_timer.timeout.connect(self._update_sessions_display)
        self.sessions_update_timer.start(2000)  # Update every 2 seconds
    
    def run(self):
        """Run the application"""
        self.show()
        return QApplication.instance().exec()
