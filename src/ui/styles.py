"""
UI style definitions for the application
"""

# Glass background style for the main window
GLASS_BACKGROUND_STYLE = """
    background-color: transparent;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
"""

# Command block style for individual command/output blocks
COMMAND_BLOCK_STYLE = """
    background-color: rgba(22, 22, 35, 0.5);
    border-radius: 8px;
    border: 1px solid rgba(60, 60, 80, 0.2);
    margin: 2px 0px;
"""

# Input container style
INPUT_CONTAINER_STYLE = """
    QWidget#inputContainer {
        background-color: rgba(25, 25, 40, 0.8);
        border-radius: 8px;
        border: 1px solid rgba(100, 100, 140, 0.5);
        padding: 2px;
    }
"""

# Command input style
COMMAND_INPUT_STYLE = """
    background-color: transparent;
    color: rgb(220, 220, 240);
    border: none;
    font-family: 'Cascadia Code', 'Consolas', monospace;
    selection-background-color: rgba(70, 130, 180, 0.5);
"""

# Execute button style
EXECUTE_BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(60, 80, 140, 0.7);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 3px;
        font-weight: 500;
        min-width: 28px;
        min-height: 28px;
    }
    QPushButton:hover {
        background-color: rgba(70, 95, 160, 0.8);
    }
    QPushButton:pressed {
        background-color: rgba(50, 70, 130, 0.9);
    }
"""

# AI toggle button style
AI_BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(40, 40, 55, 0.7);
        color: rgba(180, 180, 220, 0.9);
        border: 1px solid rgba(60, 60, 80, 0.6);
        border-radius: 4px;
        padding: 5px 15px;
        font-weight: 500;
    }
    QPushButton:checked {
        background-color: rgba(40, 90, 70, 0.7);
        color: rgba(150, 230, 180, 0.9);
        border: 1px solid rgba(60, 120, 90, 0.6);
    }
    QPushButton:hover {
        background-color: rgba(50, 50, 65, 0.8);
    }
    QPushButton:checked:hover {
        background-color: rgba(45, 100, 80, 0.8);
    }
"""

# Status bar style
STATUS_BAR_STYLE = """
    background-color: rgba(25, 25, 38, 0.5);
    color: rgba(180, 180, 210, 0.9);
    font-family: 'Segoe UI', sans-serif;
    font-size: 11px;
    padding-left: 10px;
    min-height: 20px;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
"""

# Scrollbar style
SCROLLBAR_STYLE = """
    QScrollBar:vertical {
        background: rgba(30, 30, 45, 0.3);
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: rgba(80, 80, 120, 0.5);
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: rgba(100, 100, 150, 0.6);
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
""" 