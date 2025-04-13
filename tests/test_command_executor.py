"""
Tests for the CommandExecutor class
"""
import os
import sys
import unittest
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from command.executor import CommandExecutor

class TestCommandExecutor(unittest.TestCase):
    """Tests for CommandExecutor"""
    
    def setUp(self):
        self.executor = CommandExecutor()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
    
    def test_simple_command_execution(self):
        """Test simple command execution"""
        output, success, new_dir = self.executor.execute_command("echo Hello World", self.test_dir)
        self.assertTrue(success)
        self.assertIn("Hello World", output)
        self.assertIsNone(new_dir)
    
    def test_dangerous_command_block(self):
        """Test that dangerous commands are blocked"""
        output, success, new_dir = self.executor.execute_command("rm -rf /", self.test_dir)
        self.assertFalse(success)
        self.assertIn("blocked for safety", output)
        self.assertIsNone(new_dir)
    
    def test_directory_change(self):
        """Test directory change command"""
        parent_dir = str(Path(self.test_dir).parent)
        output, success, new_dir = self.executor.execute_command("cd ..", self.test_dir)
        self.assertTrue(success)
        self.assertEqual(new_dir, parent_dir)
    
    def test_directory_change_to_nonexistent(self):
        """Test directory change to nonexistent directory"""
        output, success, new_dir = self.executor.execute_command("cd /path/does/not/exist", self.test_dir)
        self.assertFalse(success)
        self.assertIn("cannot find", output.lower())
        self.assertIsNone(new_dir)

if __name__ == "__main__":
    unittest.main() 