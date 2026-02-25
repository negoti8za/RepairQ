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
        self.setWindowTitle(f"{APP_NAME} - Login")
        self.setGeometry(300, 200, 650, 500)
        self.setMinimumSize(650, 500)
        self.init_ui()
    
    def init_ui(self):
        """Initialize modern login UI with Windows 10 style"""
        self.setStyleSheet("""
            QWidget {
                background-color: #FAFAFA;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header banner - gradient style with primary color
        header = QWidget()
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_PRIMARY};
            }}
        """)
        header.setFixedHeight(120)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setSpacing(5)
        
        title = QLabel(APP_NAME)
        title.setFont(QFont(FONT_FAMILY, 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        
        subtitle = QLabel("Repair Shop Management System")
        subtitle.setFont(QFont(FONT_FAMILY, 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        header_layout.addWidget(subtitle)
        
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        
        # Form container
        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(50, 40, 50, 40)
        form_layout.setSpacing(16)
        
        # Username section
        username_label = QLabel("Username")
        username_label.setFont(QFont(FONT_FAMILY, 10, QFont.Weight.Bold))
        username_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")
        self.username_input.setMinimumHeight(40)
        self.username_input.setFont(QFont(FONT_FAMILY, 10))
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid #D2D0CE;
                border-radius: 2px;
                padding: 10px 12px;
                background-color: white;
                color: {COLOR_TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARY};
                background-color: white;
            }}
        """)
        form_layout.addWidget(self.username_input)
        
        # Password section
        password_label = QLabel("Password")
        password_label.setFont(QFont(FONT_FAMILY, 10, QFont.Weight.Bold))
        password_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setFont(QFont(FONT_FAMILY, 10))
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid #D2D0CE;
                border-radius: 2px;
                padding: 10px 12px;
                background-color: white;
                color: {COLOR_TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARY};
                background-color: white;
            }}
        """)
        form_layout.addWidget(self.password_input)
        
        # Error message
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {COLOR_DANGER}; font-size: 9pt;")
        self.error_label.setWordWrap(True)
        self.error_label.setMinimumHeight(30)
        form_layout.addWidget(self.error_label)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setMinimumHeight(42)
        self.login_button.setFont(QFont(FONT_FAMILY, 11, QFont.Weight.Bold))
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border: none;
                border-radius: 2px;
                padding: 10px;
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
        form_layout.addWidget(self.login_button)
        
        form_layout.addStretch()
        form_container.setLayout(form_layout)
        main_layout.addWidget(form_container, 1)
        
        self.setLayout(main_layout)
        
        # Focus on username
        self.username_input.setFocus()
        
        # Connect enter key
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Focus on username
        self.username_input.setFocus()
        
        # Connect enter key
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login button click with error handling"""
        self.error_label.setText("")
        
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        try:
            success, error, user = AuthService.login(username, password)
            
            if not success:
                self.error_label.setText(error or "Login failed")
                self.password_input.clear()
                self.password_input.setFocus()
                return
            
            # Successful login
            # Initialize database
            try:
                Database.initialize()
            except Exception as e:
                print(f"Database initialization error: {e}")
                # Continue anyway if database is already initialized
            
            if not user.get('password_changed') and FORCE_PASSWORD_CHANGE_ON_FIRST_LOGIN:
                # Show password change dialog - but allow skipping  
                dialog = PasswordChangeDialog(f"Welcome {user.get('first_name', 'User')}!")
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    try:
                        AuthService.change_password(user.get('user_id'), dialog.get_new_password())
                        QMessageBox.information(self, "Success", "Password changed successfully!")
                    except Exception as e:
                        self.error_label.setText(f"Password change failed: {str(e)}")
                # Always proceed to main window regardless of password change
                self.switch_to_main_window()
            else:
                try:
                    self.switch_to_main_window()
                except Exception as e:
                    self.error_label.setText(f"Failed to load main window: {str(e)}")
                    print(f"Main window error: {e}")
                    import traceback
                    traceback.print_exc()
                    AuthService.logout()
        except Exception as e:
            self.error_label.setText(f"Login error: {str(e)}")
            print(f"Login error: {e}")
            import traceback
            traceback.print_exc()
    
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
                font-size: {FONT_SIZE_NORMAL}pt;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARY};
            }}
            QLabel {{
                color: {COLOR_TEXT_PRIMARY};
                font-size: {FONT_SIZE_NORMAL}pt;
            }}
            QCheckBox {{
                color: {COLOR_TEXT_PRIMARY};
                spacing: 5px;
                font-size: {FONT_SIZE_NORMAL}pt;
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
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                font-size: {FONT_SIZE_NORMAL}pt;
            }}
            QPushButton:hover {{
                background-color: #005A9E;
            }}
            QPushButton:pressed {{
                background-color: #004578;
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
