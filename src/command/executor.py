"""
Command executor for running system commands
"""
import os
import subprocess
import shlex
import re

class CommandExecutor:
    """
    Handles execution of system commands with safety checks and special command handling
    """
    
    # Commands that can change the current directory
    DIRECTORY_COMMANDS = ['cd', 'chdir', 'pushd', 'popd']
    
    # Commands that should be blocked for safety
    BLOCKED_COMMANDS = [
        'rm -rf /', 'rmdir /s /q c:', 'format', 'del /f /s /q',
        # Add more dangerous commands here
    ]
    
    def execute_command(self, command, current_directory):
        """
        Execute a command and return the result
        
        Args:
            command (str): The command to execute
            current_directory (str): The current working directory
            
        Returns:
            tuple: (output, success, new_directory)
                - output: The command output or error message
                - success: Boolean indicating if command succeeded
                - new_directory: New directory if changed, or None
        """
        # Safety check
        if self._is_dangerous_command(command):
            return (
                "Command blocked for safety reasons. Please use a less destructive alternative.",
                False,
                None
            )
        
        # Handle directory change commands specially
        if self._is_directory_command(command):
            return self._handle_directory_command(command, current_directory)
        
        # Handle exit command
        if command.strip().lower() in ['exit', 'quit']:
            return "Use the window close button to exit the application.", True, None
        
        # Execute the command
        try:
            # Run in the specified directory
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=current_directory
            )
            
            stdout, stderr = process.communicate(timeout=30)
            
            if process.returncode == 0:
                return stdout.strip(), True, None
            else:
                return f"Error: {stderr.strip()}", False, None
                
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds", False, None
        except Exception as e:
            return f"Failed to execute command: {str(e)}", False, None
    
    def _is_dangerous_command(self, command):
        """Check if a command is potentially dangerous"""
        command_lower = command.lower()
        
        # Check against blocked commands
        for blocked in self.BLOCKED_COMMANDS:
            if blocked in command_lower:
                return True
        
        # Check for suspicious patterns
        danger_patterns = [
            r'rm\s+-rf\s+[/\\]',           # rm -rf / or similar
            r'rmdir\s+/s\s+/q\s+[c-zC-Z]:', # rmdir /s /q drive:
            r'format\s+[c-zC-Z]:',         # format drive:
            r'del\s+/[fFqQsS]+\s+[/\\]'    # del with dangerous flags
        ]
        
        for pattern in danger_patterns:
            if re.search(pattern, command_lower):
                return True
        
        return False
    
    def _is_directory_command(self, command):
        """Check if command is one that changes directories"""
        cmd_parts = shlex.split(command, posix=False)
        if not cmd_parts:
            return False
            
        base_cmd = cmd_parts[0].lower()
        return base_cmd in self.DIRECTORY_COMMANDS
    
    def _handle_directory_command(self, command, current_directory):
        """Handle commands that change directory"""
        cmd_parts = shlex.split(command, posix=False)
        base_cmd = cmd_parts[0].lower()
        
        # Simple cd command
        if base_cmd == 'cd' or base_cmd == 'chdir':
            # 'cd' alone shows current directory
            if len(cmd_parts) == 1:
                return current_directory, True, None
            
            # 'cd ..' or other paths
            try:
                # Get the target directory
                target = ' '.join(cmd_parts[1:])
                
                # Handle quotes that might be left in the path
                target = target.strip('"\'')
                
                # Resolve the new path
                if os.path.isabs(target):
                    new_dir = target
                else:
                    new_dir = os.path.normpath(os.path.join(current_directory, target))
                
                # Check if directory exists
                if os.path.isdir(new_dir):
                    return f"Changed directory to: {new_dir}", True, new_dir
                else:
                    return f"The system cannot find the path specified: {target}", False, None
            except Exception as e:
                return f"Error changing directory: {str(e)}", False, None
        
        # pushd and popd would need a directory stack, which we don't implement here
        return f"Command {base_cmd} not fully implemented.", False, None 