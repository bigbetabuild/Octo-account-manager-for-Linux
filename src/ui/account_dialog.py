"""
Account dialogs for adding/editing accounts
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

from src.utils.validators import Validators

class AddAccountDialog(QDialog):
    """Dialog for adding a new account"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Account")
        self.setModal(True)
        self.setGeometry(200, 200, 400, 300)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)
        
        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)
        
        # Profile
        layout.addWidget(QLabel("Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Default", "Alt", "Bot", "Custom"])
        self.profile_combo.setEditable(True)
        layout.addWidget(self.profile_combo)
        
        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        layout.addWidget(self.notes_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("Add Account")
        ok_btn.clicked.connect(self._on_ok)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _on_ok(self):
        """Validate and accept dialog"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not Validators.validate_username(username):
            QMessageBox.warning(self, "Validation Error", 
                              "Invalid username. Must be 3-20 characters (alphanumeric and underscore)")
            return
        
        if not Validators.validate_password(password):
            QMessageBox.warning(self, "Validation Error",
                              "Invalid password. Minimum 6 characters required")
            return
        
        self.accept()
    
    def get_values(self):
        """Get dialog values"""
        return (
            self.username_edit.text().strip(),
            self.password_edit.text(),
            self.profile_combo.currentText(),
            self.notes_edit.toPlainText()
        )

class EditAccountDialog(QDialog):
    """Dialog for editing an existing account"""
    
    def __init__(self, parent=None, account=None):
        super().__init__(parent)
        self.account = account
        self.setWindowTitle("Edit Account")
        self.setModal(True)
        self.setGeometry(200, 200, 400, 300)
        self._setup_ui()
        self._load_values()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_edit = QLineEdit()
        layout.addWidget(self.username_edit)
        
        # Password
        layout.addWidget(QLabel("Password (leave blank to keep current):"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)
        
        # Profile
        layout.addWidget(QLabel("Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Default", "Alt", "Bot", "Custom"])
        self.profile_combo.setEditable(True)
        layout.addWidget(self.profile_combo)
        
        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        layout.addWidget(self.notes_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_btn = QPushButton("Update Account")
        ok_btn.clicked.connect(self._on_ok)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _load_values(self):
        """Load existing account values"""
        if self.account:
            self.username_edit.setText(self.account.username)
            self.password_edit.setText(self.account.password)
            self.profile_combo.setCurrentText(self.account.profile)
            self.notes_edit.setText(self.account.notes)
    
    def _on_ok(self):
        """Validate and accept dialog"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not Validators.validate_username(username):
            QMessageBox.warning(self, "Validation Error",
                              "Invalid username. Must be 3-20 characters (alphanumeric and underscore)")
            return
        
        if password and not Validators.validate_password(password):
            QMessageBox.warning(self, "Validation Error",
                              "Invalid password. Minimum 6 characters required")
            return
        
        self.accept()
    
    def get_values(self):
        """Get dialog values"""
        # If password is empty, keep the original
        password = self.password_edit.text() or self.account.password
        
        return (
            self.username_edit.text().strip(),
            password,
            self.profile_combo.currentText(),
            self.notes_edit.toPlainText()
        )
