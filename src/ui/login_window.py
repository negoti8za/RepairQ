"""
Login Window - User authentication with password change enforcement
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDialog, QMessageBox, QCheckBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from src.config import *
from src.services.auth import AuthService
from src.services.database import Database


class LoginWindow(QWidget):
    """Main login interface"""
    
    def __init__(self, switch_to_main_window=None):
        super().__init__()
        self.switch_to_main_window = switch_to_main_window
        self.init_ui()
    
    def init_ui(self):
        """Initialize responsive login UI"""
        self.setWindowTitle(f"{APP_NAME} - Login")
        self.setGeometry(100, 100, LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT)
        self.setMinimumSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT)
        self.setStyleSheet(self._get_stylesheet())
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)
        
        # Spacer top
        main_layout.addSpacing(30)
        
        # Title
        title = QLabel(APP_NAME)
        title_font = QFont(FONT_FAMILY, FONT_SIZE_LARGE, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0078D4;")
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Repair Shop Management System")
        subtitle_font = QFont(FONT_FAMILY, FONT_SIZE_NORMAL)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #605E5C;")
        main_layout.addWidget(subtitle)
        
        # Spacer
        main_layout.addSpacing(30)
        
        # Username
        username_label = QLabel("Username:")
        username_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        main_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumHeight(35)
        self.username_input.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        main_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password:")
        password_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        main_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        self.password_input.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        main_layout.addWidget(self.password_input)
        
        # Remember me
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        main_layout.addWidget(self.remember_checkbox)
        
        # Spacer
        main_layout.addSpacing(15)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(40)
        self.login_button.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL, QFont.Weight.Bold))
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                font-size: 11pt;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QPushButton:pressed {{
                background-color: #004578;
            }}
        """)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #E81123; font-size: 9pt;")
        self.error_label.setWordWrap(True)
        main_layout.addWidget(self.error_label)
        
        # Spacer bottom
        main_layout.addStretch()
        
        # Set layout
        self.setLayout(main_layout)
        
        # Focus on username
        self.username_input.setFocus()
        
        # Connect enter key
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login button click"""
        self.error_label.setText("")
        
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        success, error, user = AuthService.login(username, password)
        
        if not success:
            self.error_label.setText(error or "Login failed")
            self.password_input.clear()
            self.password_input.setFocus()
            return
        
        # Successful login
        # Initialize database and check if password change needed
        Database.initialize()
        
        if not user.get('password_changed') and FORCE_PASSWORD_CHANGE_ON_FIRST_LOGIN:
            # Show password change dialog
            dialog = PasswordChangeDialog(f"Welcome {user.get('first_name', 'User')}!")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                AuthService.change_password(user.get('user_id'), dialog.get_new_password())
                QMessageBox.information(self, "Success", "Password changed successfully!")
                self.switch_to_main_window()
            else:
                self.error_label.setText("Password change required to continue")
                AuthService.logout()
        else:
            self.switch_to_main_window()
    
    def _get_stylesheet(self) -> str:
        """Get global stylesheet"""
        return f"""
            QWidget {{
                background-color: {COLOR_BACKGROUND};
                color: {COLOR_TEXT_PRIMARY};
                font-family: {FONT_FAMILY};
            }}
            QLineEdit {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
                padding: 8px;
                background-color: {COLOR_BACKGROUND};
                color: {COLOR_TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARY};
            }}
            QCheckBox {{
                color: {COLOR_TEXT_PRIMARY};
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: {COLOR_BACKGROUND};
                border: 1px solid {COLOR_BORDER};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLOR_PRIMARY};
                border: 1px solid {COLOR_PRIMARY};
                color: white;
            }}
        """


class PasswordChangeDialog(QDialog):
    """Password change dialog - shown on first login"""
    
    def __init__(self, title="Change Password"):
        super().__init__()
        self.new_password = None
        self.setWindowTitle(title)
        self.setGeometry(400, 300, 400, 300)
        self.setModal(True)
        self.setStyleSheet(LoginWindow(None)._get_stylesheet())
        self.init_ui()
    
    def init_ui(self):
        """Initialize password change dialog"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Message
        message = QLabel("Your password must be changed before continuing.")
        message.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        message.setWordWrap(True)
        layout.addWidget(message)
        
        layout.addSpacing(10)
        
        # New password
        password_label = QLabel("New Password:")
        password_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter new password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        layout.addWidget(self.password_input)
        
        # Confirm password
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
        layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm new password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setMinimumHeight(35)
        layout.addWidget(self.confirm_input)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #E81123; font-size: 9pt;")
        layout.addWidget(self.error_label)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("Change Password")
        ok_button.setMinimumWidth(120)
        ok_button.clicked.connect(self.accept_password)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        self.password_input.setFocus()
    
    def accept_password(self):
        """Validate and accept password"""
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not password:
            self.error_label.setText("Password cannot be empty")
            return
        
        if len(password) < MIN_PASSWORD_LENGTH:
            self.error_label.setText(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
            return
        
        if password != confirm:
            self.error_label.setText("Passwords do not match")
            return
        
        self.new_password = password
        self.accept()
    
    def get_new_password(self) -> str:
        """Get new password"""
        return self.new_password or ""
