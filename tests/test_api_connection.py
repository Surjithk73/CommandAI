"""
Test the connection to the OpenRouter API with Llama model
"""
import os
import sys
import unittest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ai.llama_client import LlamaClient

def test_api_connection():
    """Test the connection to the OpenRouter API"""
    print("Testing connection to OpenRouter API with Llama model...")
    try:
        # Initialize the client
        client = LlamaClient()
        print("Client initialized successfully")
        
        # Test a simple query
        test_query = "Show me all files in the current directory"
        print(f"Sending test query: '{test_query}'")
        
        # Get commands from the model
        commands = client.get_command(test_query, os.getcwd())
        
        # Print the commands
        if commands:
            print("Received commands:")
            for cmd in commands:
                print(f"  - {cmd}")
            print("API connection successful!")
        else:
            print("No commands received from the model")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("API connection failed")

if __name__ == "__main__":
    test_api_connection() 