"""
CLI Interface for AI Troubleshooting Assistant
Provides interactive command-line interface
"""

import sys
from typing import Optional
from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from ai_engine import TroubleshootingEngine

# Initialize colorama
init(autoreset=True)


class TroubleshootingCLI:
    """Command-line interface for troubleshooting assistant"""

    def __init__(self, provider: str = "local", **kwargs):
        """Initialize the CLI"""
        self.engine = TroubleshootingEngine(provider, **kwargs)
        self.history = InMemoryHistory()
        self.running = True
        self.provider = provider

    def print_banner(self):
        """Print welcome banner"""
        # Determine AI mode
        ai_mode = self.engine.provider.upper()
        if ai_mode == "RULE-BASED":
            mode_desc = f"{Fore.GREEN}🟢 LOCAL MODE - Rule-Based Expert System{Style.RESET_ALL}"
            mode_info = f"{Fore.YELLOW}💡 Tip: For smarter AI, install Ollama: https://ollama.ai{Style.RESET_ALL}"
        elif ai_mode == "OLLAMA":
            mode_desc = f"{Fore.GREEN}🟢 LOCAL MODE - Ollama ({self.engine.model}){Style.RESET_ALL}"
            mode_info = f"{Fore.GREEN}✓ Running locally - No API costs!{Style.RESET_ALL}"
        elif ai_mode in ["ANTHROPIC", "OPENAI"]:
            mode_desc = f"{Fore.CYAN}☁️  CLOUD MODE - {ai_mode.title()}{Style.RESET_ALL}"
            mode_info = f"{Fore.YELLOW}⚠️  Using cloud AI - API costs apply{Style.RESET_ALL}"
        else:
            mode_desc = f"{Fore.CYAN}AI Mode: {ai_mode}{Style.RESET_ALL}"
            mode_info = ""

        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗
║                                                            ║
║           🤖 AI TROUBLESHOOTING ASSISTANT 🤖              ║
║                                                            ║
║          Your intelligent problem-solving companion        ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{mode_desc}
{mode_info}

{Fore.YELLOW}Available Commands:{Style.RESET_ALL}
  • Type your problem description to start troubleshooting
  • {Fore.GREEN}/help{Style.RESET_ALL}     - Show help and commands
  • {Fore.GREEN}/reset{Style.RESET_ALL}    - Start a new troubleshooting session
  • {Fore.GREEN}/summary{Style.RESET_ALL}  - Show conversation summary
  • {Fore.GREEN}/quit{Style.RESET_ALL}     - Exit the application

{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
"""
        print(banner)

    def print_help(self):
        """Print help message"""
        help_text = f"""
{Fore.CYAN}═══ HELP ═══{Style.RESET_ALL}

{Fore.YELLOW}How to use:{Style.RESET_ALL}
1. Describe your problem in detail
2. The AI will ask clarifying questions if needed
3. Follow the troubleshooting steps provided
4. Continue the conversation with follow-up questions

{Fore.YELLOW}Tips for better results:{Style.RESET_ALL}
• Include error messages or logs
• Describe what you've already tried
• Mention your environment (OS, software versions, etc.)
• Be specific about when the problem occurs

{Fore.YELLOW}Example problems:{Style.RESET_ALL}
• "My Python script throws a 'ModuleNotFoundError' when I run it"
• "Website is loading slowly, took 30 seconds to load homepage"
• "Cannot connect to PostgreSQL database, getting connection refused"
• "Docker container keeps restarting with exit code 137"

{Fore.YELLOW}Commands:{Style.RESET_ALL}
• {Fore.GREEN}/help{Style.RESET_ALL}     - Show this help message
• {Fore.GREEN}/reset{Style.RESET_ALL}    - Clear conversation and start fresh
• {Fore.GREEN}/summary{Style.RESET_ALL}  - Show conversation history
• {Fore.GREEN}/quit{Style.RESET_ALL}     - Exit the application
"""
        print(help_text)

    def print_error(self, message: str):
        """Print error message"""
        print(f"\n{Fore.RED}❌ Error: {message}{Style.RESET_ALL}\n")

    def print_success(self, message: str):
        """Print success message"""
        print(f"\n{Fore.GREEN}✓ {message}{Style.RESET_ALL}\n")

    def print_ai_response(self, response: str):
        """Print AI response with formatting"""
        print(f"\n{Fore.CYAN}🤖 AI Assistant:{Style.RESET_ALL}\n")
        print(f"{response}\n")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")

    def handle_command(self, command: str) -> bool:
        """
        Handle special commands

        Args:
            command: Command to handle

        Returns:
            True if command was handled, False otherwise
        """
        command = command.lower().strip()

        if command == "/help":
            self.print_help()
            return True

        elif command == "/reset":
            self.engine.reset_conversation()
            self.print_success("Conversation reset. Ready for a new troubleshooting session!")
            return True

        elif command == "/summary":
            summary = self.engine.get_conversation_summary()
            print(f"\n{Fore.YELLOW}{summary}{Style.RESET_ALL}")
            return True

        elif command in ["/quit", "/exit", "/q"]:
            self.running = False
            print(f"\n{Fore.CYAN}Thanks for using AI Troubleshooting Assistant! Goodbye! 👋{Style.RESET_ALL}\n")
            return True

        return False

    def get_multiline_input(self, initial_line: str) -> str:
        """
        Get multiline input from user

        Args:
            initial_line: First line of input

        Returns:
            Complete multiline input
        """
        lines = [initial_line]

        print(f"{Fore.YELLOW}(Press Enter twice to submit, or type text and press Enter to continue){Style.RESET_ALL}")

        while True:
            try:
                line = prompt("... ", history=self.history)
                if line.strip() == "":
                    break
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break

        return "\n".join(lines)

    def start_troubleshooting(self, problem: str) -> Optional[str]:
        """
        Start a new troubleshooting session

        Args:
            problem: Problem description

        Returns:
            AI response or None if error
        """
        try:
            print(f"\n{Fore.YELLOW}🔍 Analyzing your problem...{Style.RESET_ALL}\n")
            response = self.engine.troubleshoot(problem)
            return response
        except Exception as e:
            self.print_error(f"Failed to get AI response: {str(e)}")
            return None

    def continue_conversation(self, message: str) -> Optional[str]:
        """
        Continue the conversation

        Args:
            message: User message

        Returns:
            AI response or None if error
        """
        try:
            response = self.engine.continue_conversation(message)
            return response
        except Exception as e:
            self.print_error(f"Failed to get AI response: {str(e)}")
            return None

    def run(self):
        """Run the CLI application"""
        self.print_banner()

        conversation_started = False

        while self.running:
            try:
                # Get user input
                user_input = prompt(
                    f"{Fore.GREEN}You: {Style.RESET_ALL}",
                    history=self.history
                ).strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    self.handle_command(user_input)
                    continue

                # Check if multiline input is needed
                if user_input.endswith("\\"):
                    user_input = self.get_multiline_input(user_input[:-1])

                # Process troubleshooting request
                if not conversation_started:
                    response = self.start_troubleshooting(user_input)
                    if response:
                        conversation_started = True
                        self.print_ai_response(response)
                else:
                    response = self.continue_conversation(user_input)
                    if response:
                        self.print_ai_response(response)

            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Use /quit to exit{Style.RESET_ALL}\n")
                continue

            except EOFError:
                self.running = False
                print(f"\n{Fore.CYAN}Goodbye! 👋{Style.RESET_ALL}\n")
                break

            except Exception as e:
                self.print_error(f"Unexpected error: {str(e)}")
                continue


def main():
    """Main entry point"""
    import os
    try:
        from dotenv import load_dotenv
        load_dotenv()  # Optional - only if dotenv installed
    except ImportError:
        pass  # dotenv not required for local mode

    # Get provider from environment or use local by default
    provider = os.getenv("AI_PROVIDER", "local")

    # Validate API key only for cloud providers
    if provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            print(f"{Fore.RED}Error: ANTHROPIC_API_KEY not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Create .env with your API key or use local mode{Style.RESET_ALL}")
            sys.exit(1)
    elif provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            print(f"{Fore.RED}Error: OPENAI_API_KEY not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Create .env with your API key or use local mode{Style.RESET_ALL}")
            sys.exit(1)

    # Start CLI with local mode support
    try:
        cli = TroubleshootingCLI(
            provider,
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )
        cli.run()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Falling back to rule-based mode...{Style.RESET_ALL}")
        cli = TroubleshootingCLI("rule-based")
        cli.run()


if __name__ == "__main__":
    main()
