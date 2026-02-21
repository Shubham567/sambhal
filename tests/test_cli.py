import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import os
from aethercode.cli import main

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.test_file = "cli_test_temp.py"
        with open(self.test_file, "w") as f:
            f.write("def foo():\n    pass\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_scan_command(self, mock_stdout):
        test_args = ["aethercode", "scan", self.test_file]
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Scanning", output)
        self.assertIn("Code Quality Issues", output)
        self.assertIn("missing a docstring", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_fix_command(self, mock_stdout):
        test_args = ["aethercode", "fix", self.test_file]
        with patch.object(sys, 'argv', test_args):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("Attempting to fix", output)
        self.assertIn("Applied fixes", output)

        with open(self.test_file, "r") as f:
            content = f.read()
        self.assertIn('"""TODO: Add docstring."""', content)

if __name__ == '__main__':
    unittest.main()
