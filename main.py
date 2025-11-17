#!/usr/bin/env python3
"""
AI Troubleshooting Assistant - Main Application
A comprehensive AI-powered debugging and troubleshooting tool
"""

import sys
import os
import argparse
from pathlib import Path
from colorama import Fore, Style, init

# Optional imports
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # dotenv is optional

from ai_engine import TroubleshootingEngine
from bug_detector import BugDetector
from cli import TroubleshootingCLI

# Initialize colorama
init(autoreset=True)


def analyze_file_command(args):
    """Analyze a file for bugs"""
    detector = BugDetector()

    print(f"\n{Fore.CYAN}🔍 Analyzing file: {args.file}{Style.RESET_ALL}\n")

    if not os.path.exists(args.file):
        print(f"{Fore.RED}Error: File '{args.file}' not found{Style.RESET_ALL}")
        return 1

    bugs = detector.analyze_file(args.file)

    if bugs:
        print(detector.format_report())

        if args.output:
            with open(args.output, 'w') as f:
                f.write(detector.format_report())
            print(f"\n{Fore.GREEN}Report saved to: {args.output}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.GREEN}✓ No bugs detected!{Style.RESET_ALL}\n")

    return 0


def analyze_code_command(args):
    """Analyze code snippet for bugs"""
    detector = BugDetector()

    print(f"\n{Fore.CYAN}🔍 Analyzing code snippet...{Style.RESET_ALL}\n")

    # Read code from stdin or file
    if args.code:
        code = args.code
    elif args.file:
        with open(args.file, 'r') as f:
            code = f.read()
    else:
        print(f"{Fore.YELLOW}Enter code (press Ctrl+D when done):{Style.RESET_ALL}\n")
        code = sys.stdin.read()

    language = args.language or "python"
    bugs = detector.analyze_code_snippet(code, language)

    if bugs:
        print(detector.format_report())
    else:
        print(f"{Fore.GREEN}✓ No bugs detected!{Style.RESET_ALL}\n")

    return 0


def debug_command(args):
    """Start debugging session with AI"""
    if load_dotenv:
        load_dotenv()  # Load .env if it exists (optional)

    provider = os.getenv("AI_PROVIDER", "local")  # Default to local mode!

    # Validate API key only for cloud providers
    if provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            print(f"{Fore.RED}Error: ANTHROPIC_API_KEY not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please create a .env file with your API key{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Or use local mode: AI_PROVIDER=local{Style.RESET_ALL}")
            return 1
    elif provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            print(f"{Fore.RED}Error: OPENAI_API_KEY not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please create a .env file with your API key{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Or use local mode: AI_PROVIDER=local{Style.RESET_ALL}")
            return 1

    try:
        engine = TroubleshootingEngine(
            provider,
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )
    except Exception as e:
        print(f"{Fore.RED}Error initializing AI: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Falling back to rule-based mode...{Style.RESET_ALL}")
        engine = TroubleshootingEngine("rule-based")

    print(f"\n{Fore.CYAN}🤖 AI Debugging Assistant Started{Style.RESET_ALL}\n")

    # If problem provided via command line
    if args.problem:
        print(f"{Fore.YELLOW}Problem: {args.problem}{Style.RESET_ALL}\n")

        context = None
        if args.context:
            context = args.context
        elif args.error:
            context = f"Error: {args.error}"
        elif args.file:
            with open(args.file, 'r') as f:
                context = f"Code:\n{f.read()}"

        response = engine.troubleshoot(args.problem, context)
        print(f"{Fore.CYAN}AI Assistant:{Style.RESET_ALL}\n{response}\n")

        # Save logs if requested
        if args.save_logs:
            engine.save_session()
            print(f"{Fore.GREEN}Logs saved to logs/ directory{Style.RESET_ALL}")

        return 0

    # Otherwise start interactive session
    print(f"{Fore.YELLOW}Use Ctrl+C to exit or type 'quit'{Style.RESET_ALL}\n")

    while True:
        try:
            problem = input(f"{Fore.GREEN}Describe the issue: {Style.RESET_ALL}")

            if problem.lower() in ['quit', 'exit', 'q']:
                break

            if not problem.strip():
                continue

            response = engine.troubleshoot(problem)
            print(f"\n{Fore.CYAN}AI Assistant:{Style.RESET_ALL}\n{response}\n")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
            break
        except EOFError:
            break

    return 0


def interactive_command(args):
    """Start interactive CLI"""
    if load_dotenv:
        load_dotenv()  # Load .env if it exists (optional)

    provider = os.getenv("AI_PROVIDER", "local")  # Default to local mode!

    # Validate API key only for cloud providers
    if provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            print(f"{Fore.RED}Error: ANTHROPIC_API_KEY not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please create a .env file with your API key{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Or use local mode: AI_PROVIDER=local{Style.RESET_ALL}")
            return 1
    elif provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            print(f"{Fore.RED}Error: OPENAI_API_KEY not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please create a .env file with your API key{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Or use local mode: AI_PROVIDER=local{Style.RESET_ALL}")
            return 1

    try:
        cli = TroubleshootingCLI(
            provider,
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )
        cli.run()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Trying rule-based mode...{Style.RESET_ALL}")
        cli = TroubleshootingCLI("rule-based")
        cli.run()

    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Troubleshooting and Debugging Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python main.py

  # Analyze a file for bugs
  python main.py analyze-file app.py

  # Quick debugging
  python main.py debug --problem "My app crashes on startup"

  # Debug with error message
  python main.py debug --problem "Connection timeout" --error "TimeoutError: Connection timed out after 30s"

  # Analyze code snippet
  python main.py analyze-code --language python --code "password = 'admin123'"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Interactive mode (default)
    parser_interactive = subparsers.add_parser('interactive', help='Start interactive CLI')

    # Analyze file command
    parser_analyze = subparsers.add_parser('analyze-file', help='Analyze a file for bugs')
    parser_analyze.add_argument('file', help='File to analyze')
    parser_analyze.add_argument('-o', '--output', help='Output report to file')
    parser_analyze.set_defaults(func=analyze_file_command)

    # Analyze code command
    parser_code = subparsers.add_parser('analyze-code', help='Analyze code snippet')
    parser_code.add_argument('-c', '--code', help='Code snippet to analyze')
    parser_code.add_argument('-f', '--file', help='Read code from file')
    parser_code.add_argument('-l', '--language', default='python',
                            help='Programming language (default: python)')
    parser_code.set_defaults(func=analyze_code_command)

    # Debug command
    parser_debug = subparsers.add_parser('debug', help='Start debugging with AI')
    parser_debug.add_argument('-p', '--problem', help='Problem description')
    parser_debug.add_argument('-c', '--context', help='Additional context')
    parser_debug.add_argument('-e', '--error', help='Error message')
    parser_debug.add_argument('-f', '--file', help='Code file related to the issue')
    parser_debug.add_argument('-s', '--save-logs', action='store_true',
                             help='Save troubleshooting logs')
    parser_debug.set_defaults(func=debug_command)

    args = parser.parse_args()

    # Default to interactive mode if no command specified
    if not args.command:
        return interactive_command(args)

    # Execute the appropriate command
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
