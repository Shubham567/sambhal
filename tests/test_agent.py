import unittest
import os
from aethercode.core.agent import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_temp.py"
        with open(self.test_file, "w") as f:
            f.write("def foo():\n    pass\n")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_analyze(self):
        agent = Agent(self.test_file)
        issues = agent.analyze()
        self.assertIn("ast_issues", issues)
        self.assertIn("pii_issues", issues)
        self.assertEqual(len(issues["ast_issues"]), 1)
        self.assertEqual(issues["ast_issues"][0]["type"], "missing_docstring")

    def test_fix(self):
        agent = Agent(self.test_file)
        result = agent.fix()
        self.assertIn("Applied fixes", result)

        with open(self.test_file, "r") as f:
            content = f.read()

        self.assertIn('"""TODO: Add docstring."""', content)

if __name__ == '__main__':
    unittest.main()
