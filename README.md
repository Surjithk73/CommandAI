# AI-Powered Terminal

A modern command-line interface with AI capabilities, featuring a sleek glass-effect UI inspired by Warp.dev.

## Features

- Modern glass-effect UI with a clean terminal interface
- AI mode for natural language command processing
- Integrated with a local terminal for executing commands
- Elegant command history display

## Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-powered-terminal.git
   cd ai-powered-terminal
   ```

2. Install dependencies:
   ```
   pip install PyQt6==6.5.0 PyQt6-Qt6==6.5.0 PyQt6-sip
   ```

   Note: Specific versions are recommended to avoid DLL issues on Windows.

3. Run the application:
   ```
   python run.py
   ```

## Troubleshooting

### DLL Loading Issues with PyQt6

If you encounter a DLL loading error like:

```
ImportError: DLL load failed while importing QtWidgets: The specified procedure could not be found.
```

Try these solutions:

1. Reinstall PyQt6 with matched versions:
   ```
   pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip
   pip install PyQt6==6.5.0
   pip install PyQt6-Qt6==6.5.0
   ```

2. If you have multiple Python installations, ensure you're using the correct one.

3. Make sure your system has the latest Microsoft Visual C++ Redistributable packages installed.

### Application Not Starting

If the application doesn't start:

1. Verify Python version compatibility:
   ```
   python --version
   ```

2. Check for import errors by running:
   ```
   python -c "import PyQt6.QtWidgets"
   ```

3. Look for error messages in the terminal output.

## Usage

- **Regular Mode**: Type standard command line commands
- **AI Mode**: Toggle the AI button to enable natural language processing
- Commands are executed in your system's terminal
- Results are displayed in the terminal output area

## License

[MIT License](LICENSE) 