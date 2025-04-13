#!/usr/bin/env python3
"""
Main entry point for the AI-powered Terminal
"""
import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QLibraryInfo

from src.ui.main_window import MainWindow

def main():
    """Main application entry point"""
    # Set environment variables to ensure Qt can find its plugins
    os.environ["QT_PLUGIN_PATH"] = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    
    # Create the application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 