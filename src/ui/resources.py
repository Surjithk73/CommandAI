"""
Resource utilities for the application
"""

import os
import base64
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen, QBrush
from PyQt6.QtCore import Qt, QSize

def get_app_icon():
    """Returns a QIcon for the application"""
    if not hasattr(get_app_icon, "_icon"):
        # Create a simple icon instead of using base64 data
        icon = QIcon()
        
        # Create a simple pixmap with a terminal icon
        size = QSize(64, 64)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # Draw a simple terminal icon
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw terminal background
        painter.setBrush(QBrush(QColor(50, 50, 70)))
        painter.setPen(QPen(QColor(80, 80, 120), 2))
        painter.drawRoundedRect(4, 4, 56, 56, 8, 8)
        
        # Draw terminal title bar
        painter.setBrush(QBrush(QColor(80, 100, 160)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(4, 4, 56, 10, 4, 4)
        
        # Draw command prompt
        painter.setPen(QPen(QColor(100, 220, 150), 2))
        painter.drawText(10, 30, "$>")
        
        # Draw blinking cursor
        painter.setBrush(QBrush(QColor(220, 220, 240)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(24, 26, 8, 2)
        
        painter.end()
        
        # Create icon from pixmap
        icon.addPixmap(pixmap)
        get_app_icon._icon = icon
        
    return get_app_icon._icon 