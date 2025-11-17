"""
AI Troubleshooting Engine
Handles AI interactions and troubleshooting logic
"""

import os
import re
from typing import List, Dict, Optional
from logger import TroubleshootingLogger
from bug_detector import BugDetector, BugReport

# Optional cloud providers
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Local AI provider
try:
    from local_ai import get_local_ai, OllamaProvider, RuleBasedAI
except ImportError:
    get_local_ai = None


class TroubleshootingEngine:
    """Core engine for AI-powered troubleshooting"""

    def __init__(self, provider: str = "local", enable_logging: bool = True, **kwargs):
        """
        Initialize the troubleshooting engine

        Args:
            provider: AI provider to use ('local', 'ollama', 'rule-based', 'anthropic', or 'openai')
            enable_logging: Whether to enable logging
            **kwargs: Additional arguments for local providers (model, host, etc.)
        """
        self.provider = provider.lower()
        self.conversation_history: List[Dict[str, str]] = []
        self.bug_detector = BugDetector()
        self.client = None
        self.model = "unknown"

        # Initialize logger
        self.logger = TroubleshootingLogger() if enable_logging else None

        # Initialize AI provider
        if self.provider in ["local", "ollama", "rule-based"]:
            # Local AI - no tokens required!
            if get_local_ai is None:
                raise ImportError("local_ai module not found")

            self.client = get_local_ai(
                provider_type=self.provider,
                model=kwargs.get("model", "llama2"),
                host=kwargs.get("host", "http://localhost:11434")
            )

            if isinstance(self.client, OllamaProvider):
                self.model = self.client.model
                self.provider = "ollama"
            else:
                self.model = "rule-based-expert-system"
                self.provider = "rule-based"

        elif self.provider == "anthropic":
            if Anthropic is None:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

        elif self.provider == "openai":
            if OpenAI is None:
                raise ImportError("openai package not installed. Run: pip install openai")
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use: local, ollama, rule-based, anthropic, or openai")

        # Log session start
        if self.logger:
            self.logger.log_session_start(self.provider, self.model)

    def get_system_prompt(self) -> str:
        """Get the system prompt for the troubleshooting AI"""
        return """You are an expert AI troubleshooting assistant with advanced bug detection capabilities. Your role is to help users diagnose and solve technical problems across various domains including:

- Software and code issues (bugs, errors, performance)
- System administration (Linux, Windows, macOS)
- Network problems (connectivity, configuration)
- Hardware issues
- Application troubleshooting
- Database problems
- Cloud services and DevOps
- Security vulnerabilities and malfunction detection

When helping users:
1. Ask clarifying questions to understand the problem fully
2. Analyze code snippets for bugs, security issues, and potential malfunctions
3. Identify the severity of issues (critical, high, medium, low)
4. Provide step-by-step troubleshooting steps
5. Explain technical concepts clearly
6. Suggest multiple solutions when applicable
7. Help identify root causes, not just symptoms
8. Provide preventive measures for the future
9. Document all findings including issues, bugs, and diagnostics

When analyzing code or logs:
- Identify security vulnerabilities (SQL injection, XSS, hardcoded credentials, etc.)
- Detect common bugs and anti-patterns
- Flag performance issues and inefficiencies
- Note configuration problems
- Highlight malfunctions and error conditions

Be concise, practical, and actionable. Focus on solving the problem efficiently while ensuring comprehensive issue detection."""

    def troubleshoot(self, problem: str, context: Optional[str] = None,
                    code_file: Optional[str] = None) -> str:
        """
        Analyze a problem and provide troubleshooting guidance

        Args:
            problem: Description of the problem
            context: Additional context (error messages, logs, etc.)
            code_file: Optional code file to analyze for bugs

        Returns:
            AI response with troubleshooting steps
        """
        # Log the problem
        if self.logger:
            self.logger.log_problem(problem, context)

        # Analyze code file if provided
        bug_analysis = ""
        if code_file and os.path.exists(code_file):
            bugs = self.bug_detector.analyze_file(code_file)
            if bugs:
                bug_analysis = "\n\nAutomated Bug Analysis:\n" + self.bug_detector.format_report()

                # Log bugs found
                if self.logger:
                    for bug in bugs:
                        self.logger.log_bug_detected(
                            bug.description,
                            f"{bug.location}:{bug.line_number}",
                            bug.suggested_fix
                        )

        # Build the user message
        user_message = f"Problem: {problem}"
        if context:
            user_message += f"\n\nAdditional Context:\n{context}"
        if bug_analysis:
            user_message += bug_analysis

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get AI response
        response = self._get_ai_response()

        # Log AI interaction
        if self.logger:
            self.logger.log_ai_interaction(problem, response)
            self._extract_and_log_findings(response)

        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def continue_conversation(self, message: str) -> str:
        """
        Continue an ongoing troubleshooting conversation

        Args:
            message: User's follow-up message

        Returns:
            AI response
        """
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        response = self._get_ai_response()

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def _get_ai_response(self) -> str:
        """Get response from the AI provider"""
        if self.provider == "anthropic":
            return self._get_anthropic_response()
        elif self.provider == "openai":
            return self._get_openai_response()
        elif self.provider == "ollama":
            return self._get_ollama_response()
        elif self.provider == "rule-based":
            return self._get_rule_based_response()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _get_anthropic_response(self) -> str:
        """Get response from Anthropic Claude"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.get_system_prompt(),
            messages=self.conversation_history
        )
        return response.content[0].text

    def _get_openai_response(self) -> str:
        """Get response from OpenAI GPT"""
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ] + self.conversation_history

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2048
        )
        return response.choices[0].message.content

    def _get_ollama_response(self) -> str:
        """Get response from local Ollama"""
        # Format messages for Ollama
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ] + self.conversation_history

        return self.client.chat(messages)

    def _get_rule_based_response(self) -> str:
        """Get response from rule-based expert system"""
        # Extract the problem from conversation history
        if self.conversation_history:
            last_message = self.conversation_history[-1]
            problem = last_message.get("content", "")

            # Extract context if available
            context = None
            if len(self.conversation_history) > 1:
                context_parts = []
                for msg in self.conversation_history[:-1]:
                    if msg.get("role") == "user":
                        context_parts.append(msg.get("content", ""))
                context = "\n".join(context_parts) if context_parts else None

            return self.client.analyze(problem, context)
        else:
            return "Please describe the problem you're experiencing."

    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history"

        summary = "Conversation Summary:\n" + "="*50 + "\n\n"
        for i, msg in enumerate(self.conversation_history):
            role = msg["role"].upper()
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary += f"{i+1}. {role}: {content}\n\n"

        return summary

    def analyze_code(self, code: str, language: str = "python") -> str:
        """
        Analyze code snippet for bugs

        Args:
            code: Code to analyze
            language: Programming language

        Returns:
            Bug analysis report
        """
        bugs = self.bug_detector.analyze_code_snippet(code, language)

        if self.logger and bugs:
            for bug in bugs:
                self.logger.log_bug_detected(
                    bug.description,
                    bug.location,
                    bug.suggested_fix
                )

        return self.bug_detector.format_report()

    def _extract_and_log_findings(self, response: str):
        """
        Extract and log issues, bugs, and solutions from AI response

        Args:
            response: AI response to analyze
        """
        if not self.logger:
            return

        # Extract issues (simple heuristic-based)
        response_lower = response.lower()

        # Look for security issues
        if any(word in response_lower for word in ['security', 'vulnerability', 'exploit', 'injection']):
            self.logger.log_issue_found(
                "security",
                "Potential security issue identified in analysis",
                "high"
            )

        # Look for performance issues
        if any(word in response_lower for word in ['slow', 'performance', 'latency', 'timeout']):
            self.logger.log_issue_found(
                "performance",
                "Performance issue identified",
                "medium"
            )

        # Look for error mentions
        if any(word in response_lower for word in ['error', 'exception', 'crash', 'failure']):
            self.logger.log_issue_found(
                "error",
                "Error condition identified",
                "medium"
            )

        # Look for solutions (lines starting with numbers or bullet points)
        solution_patterns = [
            r'^\d+\.',  # Numbered lists
            r'^[-*]',    # Bullet points
            r'Step \d+', # Step mentions
        ]

        lines = response.split('\n')
        solution_steps = []

        for line in lines:
            line = line.strip()
            if any(re.match(pattern, line) for pattern in solution_patterns):
                solution_steps.append(line)

        if solution_steps:
            self.logger.log_solution(
                "Troubleshooting steps provided",
                solution_steps[:10]  # Limit to first 10 steps
            )

    def get_logs_summary(self) -> Optional[str]:
        """Get summary of logged data"""
        if not self.logger:
            return None
        return self.logger.generate_summary_report()

    def save_session(self):
        """Save the current session logs"""
        if self.logger:
            self.logger.log_session_end()

    def __del__(self):
        """Cleanup on deletion"""
        if hasattr(self, 'logger') and self.logger:
            try:
                self.logger.save_session_data()
            except:
                pass  # Ignore errors during cleanup
