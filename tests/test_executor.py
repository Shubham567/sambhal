import unittest
from aethercode.core.executor import Executor
from aethercode.core.analyzer import ASTAnalyzer

class TestExecutor(unittest.TestCase):
    def test_fix_missing_docstring(self):
        code = """
def func1():
    pass

def func2():
    print("hello")
"""
        analyzer = ASTAnalyzer()
        issues = analyzer.analyze(code)

        # Filter only missing_docstring
        docstring_issues = [i for i in issues if i['type'] == 'missing_docstring']
        self.assertEqual(len(docstring_issues), 2)

        executor = Executor(code)
        fixed_code = executor.apply_fixes(docstring_issues)

        expected_code = """
def func1():
    \"\"\"TODO: Add docstring.\"\"\"
    pass

def func2():
    \"\"\"TODO: Add docstring.\"\"\"
    print("hello")
"""
        self.assertEqual(fixed_code.strip(), expected_code.strip())

    def test_fix_missing_docstring_indentation(self):
        code = """
class MyClass:
    def nested_func(self):
        pass
"""
        analyzer = ASTAnalyzer()
        issues = analyzer.analyze(code)
        docstring_issues = [i for i in issues if i['type'] == 'missing_docstring']
        self.assertEqual(len(docstring_issues), 1)

        executor = Executor(code)
        fixed_code = executor.apply_fixes(docstring_issues)

        expected_code = """
class MyClass:
    def nested_func(self):
        \"\"\"TODO: Add docstring.\"\"\"
        pass
"""
        self.assertEqual(fixed_code.strip(), expected_code.strip())

if __name__ == '__main__':
    unittest.main()
