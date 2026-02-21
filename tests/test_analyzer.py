import unittest
from aethercode.core.analyzer import ASTAnalyzer, PIIScanner

class TestAnalyzer(unittest.TestCase):
    def test_missing_docstring(self):
        code = """
def my_func():
    pass
"""
        analyzer = ASTAnalyzer()
        issues = analyzer.analyze(code)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['type'], 'missing_docstring')

    def test_has_docstring(self):
        code = """
def my_func():
    \"\"\"This is a docstring.\"\"\"
    pass
"""
        analyzer = ASTAnalyzer()
        issues = analyzer.analyze(code)
        self.assertEqual(len(issues), 0)

    def test_pii_detection(self):
        code = """
AWS_ACCESS_KEY_ID = "AKIA1234567890ABCDEF"
password = "supersecretpassword"
"""
        scanner = PIIScanner()
        issues = scanner.scan(code)
        self.assertEqual(len(issues), 2)
        types = [issue['subtype'] for issue in issues]
        self.assertIn('aws_access_key', types)
        self.assertIn('generic_secret', types)

if __name__ == '__main__':
    unittest.main()
