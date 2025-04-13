"""
Main window for the AI-Powered Command Line Interface with modern glass UI 
inspired by Warp.dev
"""
import os
import time
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel, QSplitter,
    QStatusBar, QMessageBox, QFrame, QScrollArea,
    QGraphicsBlurEffect, QGraphicsOpacityEffect, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QTextCursor, QLinearGradient, 
    QPainter, QBrush, QPainterPath, QPixmap, QIcon
)
from PyQt6.QtWidgets import QApplication

from src.command.executor import CommandExecutor
from src.ai.llama_client import LlamaClient
from src.ai.elevenlabs_client import ElevenLabsClient
from src.ui.audio_recorder import AudioRecorder
from src.ui.resources import get_app_icon
from src.ui.styles import (
    GLASS_BACKGROUND_STYLE, COMMAND_BLOCK_STYLE, 
    INPUT_CONTAINER_STYLE, COMMAND_INPUT_STYLE,
    EXECUTE_BUTTON_STYLE, AI_BUTTON_STYLE,
    STATUS_BAR_STYLE, SCROLLBAR_STYLE
)

# Voice button style
VOICE_BUTTON_STYLE = """
    QPushButton {
        border: 1px solid rgba(100, 100, 255, 0.5);
        border-radius: 4px;
        padding: 3px;
        background-color: rgba(30, 30, 70, 0.6);
        color: rgb(180, 180, 255);
        font-size: 12px;
        font-weight: bold;
        min-width: 28px;
        min-height: 28px;
        max-width: 28px;
        max-height: 28px;
    }
    QPushButton:hover {
        background-color: rgba(50, 50, 90, 0.7);
        border: 1px solid rgba(130, 130, 255, 0.9);
    }
    QPushButton:pressed {
        background-color: rgba(80, 80, 120, 0.8);
    }
"""

# Recording button style
RECORDING_BUTTON_STYLE = """
    QPushButton {
        border: 1px solid rgba(255, 100, 100, 0.5);
        border-radius: 4px;
        padding: 3px;
        background-color: rgba(70, 30, 30, 0.6);
        color: rgb(255, 180, 180);
        font-size: 12px;
        font-weight: bold;
        min-width: 28px;
        min-height: 28px;
        max-width: 28px;
        max-height: 28px;
    }
    QPushButton:hover {
        background-color: rgba(90, 50, 50, 0.7);
        border: 1px solid rgba(255, 130, 130, 0.9);
    }
    QPushButton:pressed {
        background-color: rgba(120, 80, 80, 0.8);
    }
"""

class CommandBlock(QFrame):
    """A command block that displays input and output with a modern UI"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Styling with glass effect
        self.setObjectName("commandBlock")
        self.setStyleSheet(COMMAND_BLOCK_STYLE)
        
        # Add blur effect
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(0.5)  # Subtle blur
        
        # Add opacity effect for glass-like appearance
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.98)  # Very subtle transparency
        
        # Set the combined effects
        self.setGraphicsEffect(self.opacity_effect)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 8, 12, 8)
        self.layout.setSpacing(6)
        
        # Header with timestamp and indicator
        self.header = QWidget()
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 2)
        
        self.timestamp = QLabel(time.strftime("~ (%H:%M:%S)"))
        self.timestamp.setStyleSheet("color: rgba(160, 170, 210, 0.7); font-size: 11px;")
        self.header_layout.addWidget(self.timestamp)
        
        self.header_layout.addStretch()
        
        self.layout.addWidget(self.header)
        
        # Command input display
        self.command_display = QLabel()
        self.command_display.setStyleSheet("""
            font-family: 'Cascadia Code', 'Consolas', monospace;
            color: rgb(230, 230, 250);
            font-size: 13px;
            font-weight: 500;
            padding: 2px 0px;
        """)
        self.layout.addWidget(self.command_display)
        
        # Command output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("""
            border: none;
            background-color: transparent;
            color: rgb(210, 210, 225);
            font-family: 'Cascadia Code', 'Consolas', monospace;
            font-size: 12px;
            padding: 0px;
            selection-background-color: rgba(70, 130, 180, 0.4);
        """)
        self.layout.addWidget(self.output_display)
        
        # Hide output initially - will show when there's content
        self.output_display.setVisible(False)
        self.output_display.setFixedHeight(0)
    
    def paintEvent(self, event):
        """Custom paint event to add glass effect and borders"""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw a subtle highlight at the top for glass effect
        highlight_gradient = QLinearGradient(0, 0, 0, 15)
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 25))
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.fillRect(1, 1, self.width() - 2, 15, highlight_gradient)
    
    def set_command(self, command, is_ai=False):
        """Set the command input text"""
        prompt = "<span style='color:rgba(120,230,170,0.95);'>AI</span>" if is_ai else ">"
        self.command_display.setText(f"{prompt} {command}")
        
    def add_output(self, text, color=None):
        """Add output text to the command block"""
        # Make output visible if it was hidden
        if not self.output_display.isVisible():
            self.output_display.setVisible(True)
            
        # Format text with color if specified
        if color:
            text = f"<span style='color:{color};'>{text}</span>"
            self.output_display.insertHtml(text + "<br>")
        else:
            self.output_display.insertPlainText(text + "\n")
            
        # Adjust height based on content
        doc_height = self.output_display.document().size().height()
        self.output_display.setFixedHeight(min(doc_height + 10, 300))  # Limit height

class GlassBackgroundWidget(QWidget):
    """Widget that creates a glass effect background"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Make the window transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet(GLASS_BACKGROUND_STYLE)
        
    def showEvent(self, event):
        """Apply blur effect when the window is shown"""
        # Import BlurWindow here to apply blur effect
        try:
            from BlurWindow.blurWindow import blur
            # Apply blur to the window (works on Windows)
            if hasattr(self.window(), 'windowHandle') and self.window().windowHandle():
                blur(self.window().windowHandle().winId(), Dark=True)  # Use Dark mode for more intense blur
        except ImportError:
            print("BlurWindow library not found. Install with: pip install BlurWindow")
        except Exception as e:
            print(f"Blur effect could not be applied: {e}")
        
        super().showEvent(event)
        
    def paintEvent(self, event):
        """Add subtle glass-like visuals without specific colors"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create a fully transparent dark backdrop with rounded corners
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 50)))  # Slightly more darkening for contrast
        painter.drawRoundedRect(self.rect(), 12, 12)
        
        # Add a very subtle frosted glass highlight at the top
        highlight_gradient = QLinearGradient(0, 0, 0, 30)
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 25))  # More visible highlight
        highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        # Create a rounded rect path for the highlight - fix the QRect to QRectF conversion
        highlight_rect = QRectF(self.rect())  # Convert QRect to QRectF
        highlight_rect.setHeight(30)
        path = QPainterPath()
        path.addRoundedRect(highlight_rect, 12, 12)
        
        painter.fillPath(path, highlight_gradient)
        
        # Let the OS compositor do the rest of the work with BlurWindow
        super().paintEvent(event)

class MainWindow(QMainWindow):
    """
    Main application window with terminal-like interface and AI assistant
    with modern UI inspired by Warp.dev
    """
    def __init__(self):
        super().__init__()
        self.command_executor = CommandExecutor()
        # Initialize AI client later when needed
        self.llama_client = None  
        self.elevenlabs_client = None
        self.audio_recorder = None
        self.current_directory = os.getcwd()
        self.is_recording = False
        
        # Set window flags for transparency and blur
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self._init_ui()
        
        # Add window dragging support
        self._drag_position = None
    
    def _init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Warp Clone")
        self.resize(900, 600)  # Keep default size, but we'll optimize the proportions
        
        # Set application icon if available
        self.setWindowIcon(get_app_icon())
        
        # Set up the central widget with glass background
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        
        # Create glass background widget (parent it to central widget)
        self.glass_background = GlassBackgroundWidget(self.central_widget)
        self.glass_background.lower()  # Place behind all other widgets
        
        # Ensure glass background is properly sized with the window
        self.glass_background.setGeometry(0, 0, self.width(), self.height())
        
        # Create header with current directory and window controls
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(10, 5, 10, 5)
        
        # Current directory display
        self.current_dir_label = QLabel(os.getcwd())
        self.current_dir_label.setStyleSheet("""
            color: rgba(220, 220, 255, 1.0);
            font-size: 13px;
            font-weight: bold;
            padding: 5px;
            background-color: rgba(40, 40, 60, 0.4);
            border-radius: 4px;
        """)
        
        # AI mode toggle button
        self.ai_button = QPushButton("AI")
        self.ai_button.setCheckable(True)
        self.ai_button.setStyleSheet(AI_BUTTON_STYLE)
        self.ai_button.toggled.connect(self._toggle_ai_mode)
        
        # Minimize button for the frameless window
        self.minimize_button = QPushButton("−")
        self.minimize_button.setStyleSheet("""
            QPushButton {
                color: rgba(220, 220, 255, 1.0);
                background-color: rgba(60, 60, 80, 0.4);
                border: none;
                font-size: 20px;
                font-weight: bold;
                min-width: 30px;
                min-height: 30px;
                border-radius: 15px;
                padding: 0;
                margin-right: 5px;
            }
            QPushButton:hover {
                background-color: rgba(80, 120, 180, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(60, 100, 160, 0.9);
                color: white;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)
        
        # Close button for the frameless window
        self.close_button = QPushButton("×")
        self.close_button.setStyleSheet("""
            QPushButton {
                color: rgba(220, 220, 255, 1.0);
                background-color: rgba(60, 60, 80, 0.4);
                border: none;
                font-size: 20px;
                font-weight: bold;
                min-width: 30px;
                min-height: 30px;
                border-radius: 15px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: rgba(255, 80, 80, 0.7);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(220, 60, 60, 0.9);
                color: white;
            }
        """)
        self.close_button.clicked.connect(self.close)
        
        # Add buttons to header layout
        self.header_layout.addWidget(self.current_dir_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.ai_button)
        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.close_button)
        
        # Add header to main layout
        self.main_layout.addLayout(self.header_layout)
        
        # Continuous Terminal output area
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        terminal_style = """
            background-color: rgba(20, 20, 35, 0.75);
            border-radius: 8px;
            border: 1px solid rgba(80, 80, 120, 0.6);
            color: rgb(240, 240, 255);
            font-family: 'Cascadia Code', 'Consolas', monospace;
            font-size: 12px;
            padding: 10px;
            selection-background-color: rgba(70, 130, 180, 0.4);
        """
        self.terminal_output.setStyleSheet(terminal_style)
        
        # Ensure monospace font and proper text formatting
        document_font = QFont("Cascadia Code", 12)
        document_font.setStyleHint(QFont.StyleHint.Monospace)
        self.terminal_output.document().setDefaultFont(document_font)
        self.terminal_output.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        # Apply scrollbar styles separately
        scrollbar = self.terminal_output.verticalScrollBar()
        scrollbar.setStyleSheet(SCROLLBAR_STYLE)
        
        self.terminal_output.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.main_layout.addWidget(self.terminal_output, 1)
        
        # Input section at bottom
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 8, 0, 0)
        input_layout.setSpacing(8)
        
        # Create a container for the command input
        self.input_container = QWidget()
        self.input_container.setObjectName("inputContainer")
        self.input_container.setStyleSheet(INPUT_CONTAINER_STYLE)
        self.input_layout = QHBoxLayout(self.input_container)
        self.input_layout.setContentsMargins(10, 8, 10, 8)  # Slightly more vertical padding
        self.input_layout.setSpacing(8)
        
        # Prompt label showing > or AI>
        self.prompt_label = QLabel(">")
        self.prompt_label.setStyleSheet("color: rgba(220, 220, 240, 0.9); font-family: 'Cascadia Code', monospace; font-size: 14px;")
        self.prompt_label.setFixedWidth(30)  # Slightly wider for better appearance
        self.input_layout.addWidget(self.prompt_label)
        
        # Command input
        self.command_input = QLineEdit()
        self.command_input.setStyleSheet(COMMAND_INPUT_STYLE)
        self.command_input.setPlaceholderText("Enter a command...")
        self.command_input.setMinimumHeight(36)  # Make input field taller
        self.command_input.returnPressed.connect(self._on_command_entered)
        self.input_layout.addWidget(self.command_input)
        
        # Voice button - square and placed next to the command input
        # Initially hidden, will be shown only in AI mode
        self.voice_button = QPushButton("🎤")
        self.voice_button.setStyleSheet(VOICE_BUTTON_STYLE)
        self.voice_button.setToolTip("Click to record voice command")
        self.voice_button.clicked.connect(self._toggle_voice_recording)
        self.voice_button.setVisible(False)  # Hidden initially
        self.input_layout.addWidget(self.voice_button)
        
        # Execute button
        self.execute_button = QPushButton("▶")
        self.execute_button.setStyleSheet(EXECUTE_BUTTON_STYLE)
        self.execute_button.clicked.connect(self._on_command_entered)
        self.input_layout.addWidget(self.execute_button)
        
        input_layout.addWidget(self.input_container)
        
        self.main_layout.addWidget(input_widget)
        
        # Status bar with a modern look
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(STATUS_BAR_STYLE)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Welcome message
        self._display_welcome_message()
        
        # Set focus to command input
        self.command_input.setFocus()
    
    def _display_welcome_message(self):
        """Display welcome message in terminal output"""
        # Make sure we start with a clear terminal
        self.terminal_output.clear()
        
        # Add welcome message with strong colors for visibility
        self._append_to_terminal("<span style='color:#99FF99;font-weight:bold;'>AI</span>", 
                               "<span style='font-weight:bold;'>Welcome to AI-Powered Terminal</span>")
        self._append_to_terminal("", "Type commands directly or enable AI Mode for natural language processing.", "#99FF99")
        self._append_to_terminal("", f"Current directory: {self.current_directory}", "#AADDFF")
        self._append_to_terminal("", "")
    
    def _append_to_terminal(self, prompt, text, color=None):
        """Add text to the terminal output area"""
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)
        
        # Add HTML line with prompt and text
        html_line = ""
        
        if prompt:
            # Add prompt
            html_line += f"{prompt} "
            
        # For directory listings and command output, preserve formatting
        if "\n" in text or "  " in text:  # Directory listings often have multiple spaces and newlines
            # Pre-tag preserves whitespace formatting
            if color:
                html_line += f"<pre style='color:{color}; margin:0;'>{text}</pre>"
            else:
                html_line += f"<pre style='margin:0;'>{text}</pre>"
        else:
            # For regular messages
            if color:
                html_line += f"<span style='color:{color};'>{text}</span><br>"
            else:
                html_line += f"{text}<br>"
        
        self.terminal_output.insertHtml(html_line)
        
        # Ensure new content is visible by scrolling to bottom
        self.terminal_output.verticalScrollBar().setValue(
            self.terminal_output.verticalScrollBar().maximum()
        )
        
        # Force update
        QApplication.processEvents()
    
    @pyqtSlot()
    def _on_command_entered(self):
        """Process entered command"""
        command = self.command_input.text().strip()
        if not command:
            return
        
        # Clear input field
        self.command_input.clear()
        
        # Display command in terminal
        is_ai_mode = self.ai_button.isChecked()
        prompt = "<span style='color:#89D287;'>AI&gt;</span>" if is_ai_mode else "&gt;"
        self._append_to_terminal(prompt, command)
        
        # Process with AI or directly execute
        if is_ai_mode:
            self._process_with_ai(command)
        else:
            self._execute_command(command)
        
        # Set focus back to input
        self.command_input.setFocus()
    
    def _execute_command(self, command):
        """Execute a command directly"""
        result, success, new_directory = self.command_executor.execute_command(command, self.current_directory)
        
        # Update current directory if it changed
        if new_directory and new_directory != self.current_directory:
            self.current_directory = new_directory
            self.current_dir_label.setText(os.getcwd())
        
        # Display result in terminal
        if success:
            if result:
                # Special handling for directory listings (dir, ls, etc.)
                is_dir_listing = command.strip().lower() in ["dir", "ls"] or command.startswith("dir ") or command.startswith("ls ")
                
                if is_dir_listing:
                    # Format directory listings with a color accent for directories
                    formatted_output = self._format_directory_listing(result)
                    self._append_to_terminal("", formatted_output)
                else:
                    self._append_to_terminal("", result)
        else:
            self._append_to_terminal("", result, "#FF6E6E")
        
        return result, success
    
    def _format_directory_listing(self, output):
        """Format directory listing output to highlight directories"""
        formatted_output = ""
        lines = output.split('\n')
        
        for line in lines:
            # Check if this line represents a directory (checking for <DIR> for Windows)
            if '<DIR>' in line:
                # Add blue color for directories
                formatted_parts = line.split('<DIR>', 1)
                formatted_line = f"{formatted_parts[0]}<span style='color:#80BFFF;font-weight:bold;'>&lt;DIR&gt;</span>{formatted_parts[1]}"
                formatted_output += formatted_line + "\n"
            # For file listings, we could add more formatting here
            else:
                formatted_output += line + "\n"
                
        return formatted_output
    
    def _process_with_ai(self, natural_language_command):
        """Process command using AI"""
        # Initialize AI client if not already done
        if not self.llama_client:
            try:
                self.llama_client = LlamaClient()
                self._append_to_terminal("<span style='color:#89D287;'>AI</span>", "AI assistant initialized", "#89D287")
                self._append_to_terminal("", "AI assistant is ready to process natural language commands", "#89D287")
            except Exception as e:
                self._append_to_terminal("<span style='color:#89D287;'>AI</span>", "AI initialization failed", "#FF6E6E")
                self.ai_button.setChecked(False)
                return
        
        # Process the command with AI
        self._append_to_terminal("", "Processing with AI...", "#6E9EFF")
        
        try:
            # Get command from AI
            ai_commands = self.llama_client.get_command(
                natural_language_command, 
                self.current_directory
            )
            
            if not ai_commands:
                self._append_to_terminal("", "AI couldn't process the command", "#FF6E6E")
                return
            
            # Display and execute AI-generated commands
            self._append_to_terminal("", "AI suggests the following command(s):", "#6E9EFF")
            
            for cmd in ai_commands:
                cmd_text = f"$ {cmd}"
                self._append_to_terminal("", cmd_text, "#6EDDDD")
                result, success = self._execute_command(cmd)
                
        except Exception as e:
            self._append_to_terminal("", f"AI error: {str(e)}", "#FF6E6E")
    
    @pyqtSlot(bool)
    def _toggle_ai_mode(self, enabled):
        """Toggle between AI mode and regular command mode"""
        if enabled:
            # Always show voice button when AI mode is enabled
            self.voice_button.setVisible(True)
            
            # Only initialize Llama client if not already done
            if not self.llama_client:
                try:
                    self.llama_client = LlamaClient()
                    self.command_input.setPlaceholderText("Enter a natural language command...")
                    self.command_input.clear()
                    self.status_bar.showMessage("AI Mode Enabled - Enter natural language commands", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "AI Client Error", f"Could not initialize AI client: {str(e)}")
                    self.ai_button.setChecked(False)
                    return
            
            # Always update the UI for AI mode
            self.prompt_label.setText("AI>")
            self.prompt_label.setStyleSheet("color: #89D287; font-family: 'Cascadia Code', monospace; font-size: 14px;")
            self.command_input.setPlaceholderText("Enter a natural language command...")
            self.status_bar.showMessage("AI Mode Enabled", 3000)
        else:
            self.command_input.setPlaceholderText("Enter a command...")
            self.status_bar.showMessage("Command Mode Enabled", 3000)
            self.prompt_label.setText(">")
            self.prompt_label.setStyleSheet("color: rgba(220, 220, 240, 0.9); font-family: 'Cascadia Code', monospace; font-size: 14px;")
            # Hide voice button when AI mode is disabled
            self.voice_button.setVisible(False)
            # Stop recording if in progress
            if self.is_recording:
                self._stop_recording()
    
    def _toggle_voice_recording(self):
        """Toggle voice recording on/off when the voice button is clicked"""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """Start recording audio"""
        # Initialize ElevenLabs client and audio recorder if needed
        if not self.elevenlabs_client:
            try:
                # Get API key from environment or use the provided one
                api_key = os.getenv("ELEVENLABS_API_KEY", "sk_e6e033d67b90982b466dc33a6d4bcd9335d3e9876d1936cd")
                self.elevenlabs_client = ElevenLabsClient(api_key=api_key)
            except Exception as e:
                QMessageBox.critical(self, "Voice Client Error", f"Could not initialize ElevenLabs client: {str(e)}")
                return
                
        if not self.audio_recorder:
            try:
                self.audio_recorder = AudioRecorder(self)
                self.audio_recorder.recording_finished.connect(self._process_voice_input)
            except Exception as e:
                QMessageBox.critical(self, "Audio Recorder Error", f"Could not initialize audio recorder: {str(e)}")
                return
        
        # Change button appearance to stop icon and style
        self.voice_button.setText("⏹")
        self.voice_button.setToolTip("Click to stop recording")
        self.voice_button.setStyleSheet(RECORDING_BUTTON_STYLE)
        
        self.is_recording = True
        self.status_bar.showMessage("Recording... Click stop button to finish", 0)
        self.audio_recorder.start_recording()
    
    def _stop_recording(self):
        """Stop recording audio"""
        if not self.audio_recorder or not self.is_recording:
            return
        
        # Change button appearance back to microphone icon
        self.voice_button.setText("🎤")
        self.voice_button.setToolTip("Click to record voice command")
        self.voice_button.setStyleSheet(VOICE_BUTTON_STYLE)
        
        self.is_recording = False
        self.status_bar.showMessage("Processing audio...", 0)
        self.audio_recorder.stop_recording()
    
    @pyqtSlot(bytes)
    def _process_voice_input(self, audio_data):
        """Process the recorded audio using ElevenLabs STT"""
        if not audio_data or len(audio_data) == 0:
            self.status_bar.showMessage("No audio data received. Please try again.", 3000)
            self._append_to_terminal("", "No audio data received from recorder", "#FF6E6E")
            return
            
        if not self.elevenlabs_client:
            self.status_bar.showMessage("Voice processing error: No ElevenLabs client", 3000)
            return
            
        try:
            # Convert speech to text
            self.status_bar.showMessage("Converting speech to text...", 0)
                
            text = self.elevenlabs_client.speech_to_text(audio_data)
            
            if not text:
                self.status_bar.showMessage("No speech detected", 3000)
                return
                
            # Display the text in the input field
            self.command_input.setText(text)
            self.status_bar.showMessage(f"Voice input: {text}", 3000)
            
            # Process the text as a command (AI mode is automatically enabled with voice)
            self._process_with_ai(text)
            
        except Exception as e:
            error_msg = str(e)
            self.status_bar.showMessage(f"Voice processing error", 5000)
            
            # Log the full error to the terminal
            self._append_to_terminal("", f"Voice processing error: {error_msg}", "#FF6E6E")
            
            # Display a more user-friendly message in the dialog
            QMessageBox.warning(self, "Voice Processing Error", 
                               "Could not process voice input. Please try again or check your internet connection.")
            
            # Reset the voice button state
            self.voice_button.setText("🎤")
            self.voice_button.setToolTip("Click to record voice command")
            self.voice_button.setStyleSheet(VOICE_BUTTON_STYLE)
            self.is_recording = False
    
    def closeEvent(self, event):
        """Handle application closing"""
        event.accept()

    def resizeEvent(self, event):
        """Handle resize events to keep glass background sized to window"""
        if hasattr(self, 'glass_background'):
            self.glass_background.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
        
    def mousePressEvent(self, event):
        """Enable dragging the window from any point"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Move the window when dragging"""
        if self._drag_position is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        """Reset drag position when mouse is released"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = None
            event.accept() 