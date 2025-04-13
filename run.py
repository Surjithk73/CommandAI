#!/usr/bin/env python3
"""
Runner script for the AI-Powered Command Line Interface
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import and run main
from src.main import main

if __name__ == "__main__":
    main() 