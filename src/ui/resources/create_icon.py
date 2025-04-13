"""
Script to generate an enter arrow icon
"""
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap

def create_enter_arrow_icon():
    # Create a transparent pixmap
    size = QSize(64, 64)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # Create painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Draw arrow
    pen = QPen(QColor("#89b4fa"))
    pen.setWidth(4)
    painter.setPen(pen)
    
    # Create path for curved arrow
    path = QPainterPath()
    path.moveTo(48, 20)  # Start at top right
    path.lineTo(20, 20)  # Line to left
    path.lineTo(20, 44)  # Line down
    path.lineTo(48, 44)  # Line right
    
    # Arrow head
    arrow_head = QPainterPath()
    arrow_head.moveTo(42, 36)  # Start at bottom
    arrow_head.lineTo(48, 44)  # Diagonal to tip
    arrow_head.lineTo(42, 52)  # Diagonal to bottom
    
    # Draw paths
    painter.drawPath(path)
    painter.drawPath(arrow_head)
    
    painter.end()
    
    # Save the image
    pixmap.save("src/ui/resources/enter_arrow.png")
    
if __name__ == "__main__":
    app = QApplication([])
    create_enter_arrow_icon()
    print("Icon created successfully") 