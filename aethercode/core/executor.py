import ast
from typing import List, Dict, Any

class Executor:
    def __init__(self, code: str):
        self.code = code
        self.lines = code.splitlines()

    def apply_fixes(self, issues: List[Dict[str, Any]]) -> str:
        """Applies fixes for the given issues."""
        # Sort issues by line number in reverse order to avoid shifting line numbers
        issues.sort(key=lambda x: x['line'], reverse=True)

        for issue in issues:
            if issue['type'] == 'missing_docstring':
                self._fix_missing_docstring(issue)
            # Add more fixers here

        return "\n".join(self.lines)

    def _fix_missing_docstring(self, issue: Dict[str, Any]):
        """Adds a placeholder docstring to a function."""
        node = issue.get('node')

        # If node is not available (e.g. issues loaded from JSON), fall back to heuristic
        if not node or not isinstance(node, ast.AST) or not hasattr(node, 'body') or not node.body:
             # Fallback logic removed for safety as per review.
             # We only support fixing if we have the AST node to ensure correctness.
             return

        body_start_node = node.body[0]

        # Check for one-liner: def foo(): pass
        if node.lineno == body_start_node.lineno:
            # Skip one-liners for now to avoid complexity/breakage
            return

        # Determine insertion point (0-indexed)
        # We insert before the first statement of the body.
        insert_lineno = body_start_node.lineno - 1

        # Determine indentation
        # col_offset gives the column offset of the node (indentation)
        indentation = " " * body_start_node.col_offset

        docstring = f'{indentation}"""TODO: Add docstring."""'

        # Check if insert_lineno is valid
        if 0 <= insert_lineno <= len(self.lines):
            self.lines.insert(insert_lineno, docstring)
