"""
Logging System for AI Troubleshooting Assistant
Tracks issues, bugs, diagnostics, and AI interactions
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import json


class TroubleshootingLogger:
    """Comprehensive logging system for troubleshooting sessions"""

    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the logging system

        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # Set up logging
        self._setup_logging()

        # Session data
        self.session_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "issues_found": [],
            "bugs_detected": [],
            "diagnostics": [],
            "solutions_provided": [],
            "conversations": []
        }

    def _setup_logging(self):
        """Set up Python logging"""
        # Main log file
        main_log = os.path.join(self.log_dir, f"session_{self.session_id}.log")

        # Issues log file
        issues_log = os.path.join(self.log_dir, f"issues_{self.session_id}.log")

        # Configure main logger
        self.logger = logging.getLogger("TroubleshootingAI")
        self.logger.setLevel(logging.DEBUG)

        # Main log handler
        main_handler = logging.FileHandler(main_log)
        main_handler.setLevel(logging.DEBUG)
        main_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        main_handler.setFormatter(main_formatter)

        # Issues log handler
        self.issues_handler = logging.FileHandler(issues_log)
        self.issues_handler.setLevel(logging.WARNING)
        issues_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(message)s'
        )
        self.issues_handler.setFormatter(issues_formatter)

        # Add handlers
        self.logger.addHandler(main_handler)
        self.logger.addHandler(self.issues_handler)

        # Console handler for critical issues
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(main_formatter)
        self.logger.addHandler(console_handler)

    def log_session_start(self, provider: str, model: str):
        """Log session start"""
        self.logger.info(f"=== Troubleshooting Session Started ===")
        self.logger.info(f"Session ID: {self.session_id}")
        self.logger.info(f"AI Provider: {provider}")
        self.logger.info(f"Model: {model}")
        self.session_data["provider"] = provider
        self.session_data["model"] = model

    def log_problem(self, problem: str, context: Optional[str] = None):
        """
        Log a problem being analyzed

        Args:
            problem: Problem description
            context: Additional context
        """
        self.logger.info(f"New Problem: {problem}")
        if context:
            self.logger.info(f"Context: {context}")

        self.session_data["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "problem",
            "content": problem,
            "context": context
        })

    def log_issue_found(self, issue_type: str, description: str, severity: str = "medium"):
        """
        Log an issue that was found

        Args:
            issue_type: Type of issue (bug, error, performance, security, etc.)
            description: Issue description
            severity: Severity level (low, medium, high, critical)
        """
        issue_data = {
            "timestamp": datetime.now().isoformat(),
            "type": issue_type,
            "description": description,
            "severity": severity
        }

        self.session_data["issues_found"].append(issue_data)

        # Log based on severity
        log_msg = f"[{issue_type.upper()}] {description} (Severity: {severity})"

        if severity == "critical":
            self.logger.critical(log_msg)
        elif severity == "high":
            self.logger.error(log_msg)
        elif severity == "medium":
            self.logger.warning(log_msg)
        else:
            self.logger.info(log_msg)

    def log_bug_detected(self, bug_description: str, location: Optional[str] = None,
                         suggested_fix: Optional[str] = None):
        """
        Log a bug that was detected

        Args:
            bug_description: Description of the bug
            location: Where the bug was found (file, line, etc.)
            suggested_fix: Suggested fix for the bug
        """
        bug_data = {
            "timestamp": datetime.now().isoformat(),
            "description": bug_description,
            "location": location,
            "suggested_fix": suggested_fix
        }

        self.session_data["bugs_detected"].append(bug_data)

        log_msg = f"BUG DETECTED: {bug_description}"
        if location:
            log_msg += f" | Location: {location}"
        if suggested_fix:
            log_msg += f" | Fix: {suggested_fix}"

        self.logger.error(log_msg)

    def log_diagnostic(self, diagnostic_type: str, result: str, details: Optional[Dict[str, Any]] = None):
        """
        Log diagnostic information

        Args:
            diagnostic_type: Type of diagnostic (system, network, code, database, etc.)
            result: Diagnostic result
            details: Additional details
        """
        diagnostic_data = {
            "timestamp": datetime.now().isoformat(),
            "type": diagnostic_type,
            "result": result,
            "details": details or {}
        }

        self.session_data["diagnostics"].append(diagnostic_data)
        self.logger.info(f"DIAGNOSTIC [{diagnostic_type}]: {result}")

        if details:
            self.logger.debug(f"Diagnostic details: {json.dumps(details, indent=2)}")

    def log_solution(self, solution: str, steps: Optional[list] = None):
        """
        Log a solution provided to the user

        Args:
            solution: Solution description
            steps: Step-by-step instructions
        """
        solution_data = {
            "timestamp": datetime.now().isoformat(),
            "solution": solution,
            "steps": steps or []
        }

        self.session_data["solutions_provided"].append(solution_data)
        self.logger.info(f"SOLUTION PROVIDED: {solution}")

        if steps:
            for i, step in enumerate(steps, 1):
                self.logger.info(f"  Step {i}: {step}")

    def log_ai_interaction(self, user_message: str, ai_response: str):
        """
        Log AI interaction

        Args:
            user_message: User's message
            ai_response: AI's response
        """
        self.logger.debug(f"USER: {user_message}")
        self.logger.debug(f"AI: {ai_response[:200]}...")  # Truncate long responses

        self.session_data["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "interaction",
            "user": user_message,
            "ai": ai_response
        })

    def log_malfunction(self, component: str, description: str, error_msg: Optional[str] = None):
        """
        Log a system malfunction

        Args:
            component: Component that malfunctioned
            description: Malfunction description
            error_msg: Error message if available
        """
        malfunction_data = {
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "description": description,
            "error": error_msg
        }

        self.session_data["issues_found"].append(malfunction_data)

        log_msg = f"MALFUNCTION [{component}]: {description}"
        if error_msg:
            log_msg += f" | Error: {error_msg}"

        self.logger.error(log_msg)

    def generate_summary_report(self) -> str:
        """
        Generate a summary report of the session

        Returns:
            Summary report as string
        """
        report = []
        report.append("=" * 80)
        report.append("TROUBLESHOOTING SESSION SUMMARY")
        report.append("=" * 80)
        report.append(f"Session ID: {self.session_id}")
        report.append(f"Start Time: {self.session_data['start_time']}")
        report.append(f"End Time: {datetime.now().isoformat()}")
        report.append("")

        # Issues found
        report.append(f"ISSUES FOUND: {len(self.session_data['issues_found'])}")
        for i, issue in enumerate(self.session_data['issues_found'], 1):
            report.append(f"  {i}. [{issue.get('type', 'unknown')}] {issue.get('description', 'N/A')}")

        report.append("")

        # Bugs detected
        report.append(f"BUGS DETECTED: {len(self.session_data['bugs_detected'])}")
        for i, bug in enumerate(self.session_data['bugs_detected'], 1):
            report.append(f"  {i}. {bug['description']}")
            if bug.get('location'):
                report.append(f"     Location: {bug['location']}")

        report.append("")

        # Diagnostics run
        report.append(f"DIAGNOSTICS RUN: {len(self.session_data['diagnostics'])}")
        for i, diag in enumerate(self.session_data['diagnostics'], 1):
            report.append(f"  {i}. [{diag['type']}] {diag['result']}")

        report.append("")

        # Solutions provided
        report.append(f"SOLUTIONS PROVIDED: {len(self.session_data['solutions_provided'])}")
        for i, sol in enumerate(self.session_data['solutions_provided'], 1):
            report.append(f"  {i}. {sol['solution']}")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)

    def save_session_data(self):
        """Save session data to JSON file"""
        self.session_data["end_time"] = datetime.now().isoformat()

        session_file = os.path.join(self.log_dir, f"session_{self.session_id}.json")

        with open(session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)

        self.logger.info(f"Session data saved to {session_file}")

    def log_session_end(self):
        """Log session end and generate report"""
        summary = self.generate_summary_report()
        self.logger.info(summary)

        # Save session data
        self.save_session_data()

        # Write summary to file
        summary_file = os.path.join(self.log_dir, f"summary_{self.session_id}.txt")
        with open(summary_file, 'w') as f:
            f.write(summary)

        self.logger.info(f"Session ended. Summary saved to {summary_file}")
