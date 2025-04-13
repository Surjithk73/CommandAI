"""
Client for interacting with the Llama model via OpenRouter API
"""
import os
import json
import requests
import re
from dotenv import load_dotenv

class LlamaClient:
    """
    Client for interacting with the Llama model via OpenRouter
    """
    def __init__(self):
        """Initialize the client with API key and settings"""
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment variables
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in .env file.")
        
        # OpenRouter API settings
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.3-70b-instruct:free"  # Use Llama 3.3 70B model
        
        # Headers for API request
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://warp-cmd-ai.example.com",  # Replace with actual domain if any
            "X-Title": "AI-Powered CMD"
        }
    
    def get_command(self, natural_language_query, current_directory):
        """
        Get command(s) from the AI model based on a natural language query
        
        Args:
            natural_language_query (str): The user's query in natural language
            current_directory (str): The current working directory
            
        Returns:
            list: A list of commands to execute
        """
        # Build system prompt
        system_prompt = self._build_system_prompt(current_directory)
        
        # Make API request to OpenRouter
        response = self._make_api_request(system_prompt, natural_language_query)
        
        if not response:
            return None
            
        # Extract commands from response
        return self._extract_commands(response)
    
    def _build_system_prompt(self, current_directory):
        """Build the system prompt with current context"""
        return (
            "You are an advanced AI assistant integrated into a modern Windows command-line interface. "
            "Your primary function is to interpret user's natural language queries and convert them into valid "
            "Windows CMD commands.\n\n"
            
            "Guidelines:\n"
            "1. When responding, ONLY return the exact CMD command(s) that should be executed.\n"
            "2. If multiple commands are needed, return each command on a new line.\n"
            "3. Do not include explanations, markdown formatting, or any other text.\n"
            "4. For complex tasks requiring multiple steps, break them down into separate commands.\n"
            "5. If a task cannot be completed with CMD commands, return 'echo Cannot complete this task with CMD commands.'\n\n"
            
            f"The current working directory is: {current_directory}\n"
            "The operating system is: Windows\n\n"
            
            "Examples:\n"
            "User: 'Show me all text files in this folder'\n"
            "Response: dir *.txt\n\n"
            
            "User: 'Create a backup of my documents folder'\n"
            "Response: xcopy /s /i /y \"C:\\Users\\username\\Documents\" \"C:\\Users\\username\\Documents_Backup\"\n\n"
            
            "User: 'Find all files containing the word important'\n"
            "Response: findstr /s /i \"important\" *.*\n\n"
            
            "Remember, output ONLY the command(s) with no additional text or formatting."
        )
    
    def _make_api_request(self, system_prompt, user_query):
        """
        Make a request to the OpenRouter API
        
        Args:
            system_prompt (str): The system prompt with instructions
            user_query (str): The user's natural language query
            
        Returns:
            str: The model's response text
        """
        # Prepare request data
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        }
        
        try:
            # Make API request following the provided code pattern
            response = requests.post(
                url=self.api_url,
                headers=self.headers,
                data=json.dumps(data)
            )
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                # Extract response content
                if "choices" in result and len(result["choices"]) > 0:
                    message = result["choices"][0]["message"]
                    if "content" in message:
                        return message["content"].strip()
            
            # If we reach here, something went wrong
            error_message = f"API request failed: {response.status_code}"
            try:
                error_message += f" - {response.json().get('error', {}).get('message', '')}"
            except:
                error_message += f" - {response.text}"
                
            raise Exception(error_message)
                
        except Exception as e:
            raise Exception(f"Error while calling OpenRouter API: {str(e)}")
    
    def _extract_commands(self, response_text):
        """
        Extract commands from the AI response
        
        Args:
            response_text (str): The AI's response text
            
        Returns:
            list: A list of commands
        """
        # Clean response and split by lines
        lines = response_text.strip().split('\n')
        
        # Remove markdown code blocks if present
        if lines and (lines[0].startswith('```') or lines[0] == '```cmd' or lines[0] == '```powershell'):
            lines = lines[1:]
        if lines and lines[-1] == '```':
            lines = lines[:-1]
        
        # Filter out empty lines and lines that appear to be comments or explanations
        commands = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                commands.append(line)
        
        return commands 