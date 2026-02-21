import argparse
import sys
from aethercode.core.agent import Agent

def main():
    parser = argparse.ArgumentParser(description="AetherCode - Autonomous Agentic Engineering Platform")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a file for issues")
    scan_parser.add_argument("file", help="The file to scan")

    # fix command
    fix_parser = subparsers.add_parser("fix", help="Fix issues in a file")
    fix_parser.add_argument("file", help="The file to fix")

    args = parser.parse_args()

    if args.command == "scan":
        agent = Agent(args.file)
        try:
            issues = agent.analyze()
            print(f"Scanning {args.file}...\n")

            ast_issues = issues.get("ast_issues", [])
            pii_issues = issues.get("pii_issues", [])

            if not ast_issues and not pii_issues:
                print("No issues found.")
            else:
                if ast_issues:
                    print("--- Code Quality Issues (Heuristic Layer) ---")
                    for issue in ast_issues:
                        print(f"[Line {issue.get('line', '?')}] {issue['message']}")
                    print()

                if pii_issues:
                    print("--- Security & Compliance Issues (DPDPA Shield) ---")
                    for issue in pii_issues:
                        print(f"[Line {issue.get('line', '?')}] {issue['message']}")
                        print(f"  Match: {issue.get('match', '')}")
                    print()

        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error during scan: {e}")
            sys.exit(1)

    elif args.command == "fix":
        agent = Agent(args.file)
        try:
            print(f"Attempting to fix {args.file}...\n")
            result = agent.fix()
            print(result)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error during fix: {e}")
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
