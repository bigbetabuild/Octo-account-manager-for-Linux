"""
Dark theme stylesheet for the application
"""

def get_dark_stylesheet() -> str:
    """Return dark theme stylesheet"""
    return """
    QMainWindow {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    QLabel {
        color: #ffffff;
    }
    
    QLineEdit, QTextEdit, QComboBox, QSpinBox {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
        padding: 4px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
        border: 1px solid #0d7377;
        background-color: #2d2d2d;
    }
    
    QPushButton {
        background-color: #0d7377;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 6px 12px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #14919b;
    }
    
    QPushButton:pressed {
        background-color: #0a5962;
    }
    
    QPushButton:disabled {
        background-color: #444444;
        color: #888888;
    }
    
    QListWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
    }
    
    QListWidget::item:selected {
        background-color: #0d7377;
    }
    
    QListWidget::item:hover {
        background-color: #3d3d3d;
    }
    
    QTableWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3d3d3d;
        gridline-color: #3d3d3d;
    }
    
    QTableWidget::item:selected {
        background-color: #0d7377;
    }
    
    QHeaderView::section {
        background-color: #3d3d3d;
        color: #ffffff;
        padding: 4px;
        border: none;
    }
    
    QTabWidget::pane {
        border: 1px solid #3d3d3d;
    }
    
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #ffffff;
        padding: 6px 20px;
        border-right: 1px solid #3d3d3d;
    }
    
    QTabBar::tab:selected {
        background-color: #0d7377;
    }
    
    QTabBar::tab:hover {
        background-color: #3d3d3d;
    }
    
    QDialog {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    QMessageBox {
        background-color: #1e1e1e;
    }
    
    QMessageBox QLabel {
        color: #ffffff;
    }
    
    QScrollBar:vertical {
        background-color: #2d2d2d;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #0d7377;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #14919b;
    }
    """
