import ast
import re
from typing import List, Dict, Any, Tuple

class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Checks if a function has a docstring."""
        if not ast.get_docstring(node):
            self.issues.append({
                "type": "missing_docstring",
                "message": f"Function '{node.name}' is missing a docstring.",
                "line": node.lineno,
                "node": node
            })
        self.generic_visit(node)

    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """Parses the code and runs the AST visitor."""
        self.issues = []
        try:
            tree = ast.parse(code)
            self.visit(tree)
        except SyntaxError as e:
            self.issues.append({
                "type": "syntax_error",
                "message": f"Syntax error: {e}",
                "line": e.lineno,
            })
        return self.issues

class PIIScanner:
    # Regex patterns for potential secrets (simplified for demonstration)
    PATTERNS = {
        "aws_access_key": r"AKIA[0-9A-Z]{16}",
        "private_key": r"-----BEGIN PRIVATE KEY-----",
        "generic_secret": r"(password|secret|token|key)\s*=\s*['\"][A-Za-z0-9+/=]{8,}['\"]",
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    }

    def scan(self, code: str) -> List[Dict[str, Any]]:
        issues = []
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern_name, pattern in self.PATTERNS.items():
                match = re.search(pattern, line)
                if match:
                    issues.append({
                        "type": "pii_detection",
                        "subtype": pattern_name,
                        "message": f"Potential {pattern_name} detected.",
                        "line": i,
                        "match": match.group(0)
                    })
        return issues

def run_analysis(filepath: str) -> Dict[str, List[Dict[str, Any]]]:
    with open(filepath, "r") as f:
        code = f.read()

    ast_analyzer = ASTAnalyzer()
    ast_issues = ast_analyzer.analyze(code)

    pii_scanner = PIIScanner()
    pii_issues = pii_scanner.scan(code)

    return {
        "ast_issues": ast_issues,
        "pii_issues": pii_issues
    }
