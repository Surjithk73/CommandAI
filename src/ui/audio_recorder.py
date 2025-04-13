"""
Audio recorder for capturing voice input
"""
import io
import wave
import numpy as np
import pyaudio
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class AudioRecorderThread(QThread):
    """Thread for recording audio without blocking the UI"""
    finished = pyqtSignal(bytes)
    
    def __init__(self, channels=1, rate=44100, chunk=1024, format_type=pyaudio.paInt16):
        super().__init__()
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.format = format_type
        self._running = False
        self.frames = []
    
    def run(self):
        """Record audio from microphone"""
        self.frames = []
        p = pyaudio.PyAudio()
        
        try:
            # Open stream
            stream = p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self._running = True
            
            # Start recording
            while self._running:
                try:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    self.frames.append(data)
                except IOError:
                    # Just continue in case of overflow
                    continue
                except Exception:
                    break
            
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            
        except Exception:
            pass
        finally:
            # Make sure PyAudio is always terminated
            p.terminate()
            
            # Convert frames to bytes and emit signal
            audio_data = self._frames_to_wav()
            self.finished.emit(audio_data)
    
    def stop(self):
        """Stop the recording"""
        self._running = False
    
    def _frames_to_wav(self):
        """Convert frames to WAV bytes using in-memory processing"""
        # Create in-memory buffer instead of a temporary file
        buffer = io.BytesIO()
        
        # Check if we have any frames
        if not self.frames:
            return b''  # Return empty bytes instead of None
        
        # Initialize PyAudio to get format info
        p = pyaudio.PyAudio()
        
        # Write directly to the in-memory buffer
        wf = wave.open(buffer, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        
        # Join all frames into one byte stream
        audio_bytes = b''.join(self.frames)
        
        wf.writeframes(audio_bytes)
        wf.close()
        p.terminate()
        
        # Get the buffer content
        buffer.seek(0)
        wav_data = buffer.read()
        buffer.close()
        
        return wav_data

class AudioRecorder(QObject):
    """Audio recorder for capturing voice input"""
    recording_finished = pyqtSignal(bytes)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recorder_thread = None
    
    def start_recording(self):
        """Start recording audio"""
        if self.recorder_thread and self.recorder_thread.isRunning():
            self.stop_recording()
        
        self.recorder_thread = AudioRecorderThread()
        self.recorder_thread.finished.connect(self.recording_finished)
        self.recorder_thread.start()
        
    def stop_recording(self):
        """Stop recording audio"""
        if self.recorder_thread and self.recorder_thread.isRunning():
            self.recorder_thread.stop()
            self.recorder_thread.wait()  # Wait for thread to finish 