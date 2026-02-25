"""
PyQt6 Stylesheets - Modern Windows 10/11 styling
"""


def get_stylesheet() -> str:
    """Get the application stylesheet"""
    return """
    QMainWindow {
        background-color: #f3f3f3;
    }
    
    QWidget {
        background-color: #f3f3f3;
        color: #1a1a1a;
    }
    
    QLineEdit {
        background-color: white;
        border: 1px solid #d0d0d0;
        border-radius: 4px;
        padding: 8px;
        color: #1a1a1a;
        font-size: 10pt;
    }
    
    QLineEdit:focus {
        border: 2px solid #0078d4;
        padding: 7px;
    }
    
    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px;
        font-weight: bold;
        font-size: 10pt;
    }
    
    QPushButton:hover {
        background-color: #107c10;
    }
    
    QPushButton:pressed {
        background-color: #005a9e;
    }
    
    QLabel {
        color: #1a1a1a;
    }
    
    QTabWidget::pane {
        border: 1px solid #d0d0d0;
    }
    
    QTabBar::tab {
        background-color: #e0e0e0;
        color: #1a1a1a;
        padding: 8px 20px;
        border: 1px solid #d0d0d0;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        border-bottom: 3px solid #0078d4;
    }
    
    QTableWidget {
        background-color: white;
        alternate-background-color: #f7f7f7;
        border: 1px solid #d0d0d0;
    }
    
    QHeaderView::section {
        background-color: #e0e0e0;
        color: #1a1a1a;
        padding: 5px;
        border: 1px solid #d0d0d0;
    }
    
    QMessageBox {
        background-color: #f3f3f3;
    }
    
    QMessageBox QLabel {
        color: #1a1a1a;
    }
    
    QMessageBox QPushButton {
        min-width: 80px;
        min-height: 30px;
    }
    """
