from typing import List, Dict, Any, Tuple
from aethercode.core.analyzer import run_analysis
from aethercode.core.executor import Executor

class Agent:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.code = None
        self.issues: List[Dict[str, Any]] = []

    def analyze(self) -> Dict[str, List[Dict[str, Any]]]:
        """Runs the analysis on the file."""
        return run_analysis(self.filepath)

    def fix(self) -> str:
        """Applies fixes to the file."""
        analysis_result = self.analyze()
        ast_issues = analysis_result["ast_issues"]

        # Filter issues that can be fixed automatically
        fixable_issues = [issue for issue in ast_issues if issue["type"] == "missing_docstring"]

        if not fixable_issues:
            return "No fixable issues found."

        with open(self.filepath, "r") as f:
            code = f.read()

        executor = Executor(code)
        fixed_code = executor.apply_fixes(fixable_issues)

        with open(self.filepath, "w") as f:
            f.write(fixed_code)

        return f"Applied fixes for {len(fixable_issues)} issues."
