"""
Login window - PyQt6 UI for user authentication
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from services.database import Database
from ui.main_window import MainWindow
from ui.styles import get_stylesheet


class LoginWindow(QMainWindow):
    """Login window for RepairQ application"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the login window UI"""
        self.setWindowTitle("RepairQ - Login")
        self.setGeometry(100, 100, 400, 300)
        self.setMinimumSize(400, 300)
        
        # Set stylesheet
        self.setStyleSheet(get_stylesheet())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 40, 30, 40)
        
        # Title
        title = QLabel("RepairQ")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Desktop Application")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        main_layout.addWidget(subtitle)
        
        # Spacer
        main_layout.addSpacing(20)
        
        # Username field
        username_layout = QVBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 10))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumHeight(40)
        self.username_input.setFont(QFont("Arial", 10))
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        main_layout.addLayout(username_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setFont(QFont("Arial", 10))
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)
        
        # Spacer
        main_layout.addSpacing(10)
        
        # Login button
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumHeight(45)
        self.login_button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.login_button.setStyleSheet(
            "background-color: #0078d4; color: white; border: none; border-radius: 4px;"
        )
        self.login_button.clicked.connect(self.on_login_clicked)
        button_layout.addWidget(self.login_button)
        main_layout.addLayout(button_layout)
        
        # Spacer
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        
        # Focus on username field
        self.username_input.setFocus()
        
        # Allow Enter key to login
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(self.on_login_clicked)
    
    def on_login_clicked(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Validation Error", 
                              "Please enter both username and password.")
            return
        
        # Authenticate
        result = Database.authenticate_user(username, password)
        
        if result['authenticated']:
            # Login successful
            self.main_window = MainWindow(result)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", 
                               "Invalid username or password.")
            self.password_input.clear()
            self.username_input.setFocus()
