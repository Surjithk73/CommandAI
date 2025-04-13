"""
Client for interacting with ElevenLabs speech-to-text API
"""
import os
import json
import requests
import tempfile
import base64
from dotenv import load_dotenv

class ElevenLabsClient:
    """
    Client for interacting with ElevenLabs speech-to-text API
    """
    def __init__(self, api_key=None):
        """Initialize the client with API key"""
        # Load environment variables
        load_dotenv()
        
        # Get API key from parameter or environment variables
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key not found. Please set ELEVENLABS_API_KEY in .env file.")
        
        # ElevenLabs API settings
        self.stt_url = "https://api.elevenlabs.io/v1/speech-to-text"
        
        # Headers for API request
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }
    
    def speech_to_text(self, audio_data):
        """
        Convert speech to text using ElevenLabs API
        
        Args:
            audio_data (bytes): The audio data as bytes
            
        Returns:
            str: The transcribed text
        """
        try:
            # Validate audio data
            if not audio_data or len(audio_data) == 0:
                raise ValueError("No audio data provided - empty byte array")
            
            # Make API request directly with the bytes data instead of creating a file
            headers = {"xi-api-key": self.api_key}
            
            # Send audio_data directly in the request with correct parameter names
            files = {
                'file': ('audio.wav', audio_data, 'audio/wav'),
                'model_id': (None, 'scribe_v1')
            }
            
            # Make API request
            response = requests.post(
                url=self.stt_url,
                headers=headers,
                files=files
            )
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                return result.get("text", "")
            
            # If we reach here, something went wrong
            error_message = f"API request failed: {response.status_code}"
            try:
                error_json = response.json()
                error_message += f" - {error_json}"
            except:
                error_text = response.text
                error_message += f" - {error_text}"
                
            raise Exception(error_message)
                
        except Exception as e:
            raise Exception(f"Error while calling ElevenLabs API: {str(e)}") 