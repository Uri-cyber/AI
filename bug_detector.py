"""
Bug Detection and Code Analysis Module
Analyzes code to find bugs, issues, and potential problems
"""

import re
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BugReport:
    """Bug report data structure"""
    severity: str  # critical, high, medium, low
    bug_type: str
    description: str
    location: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    suggested_fix: Optional[str] = None


class BugDetector:
    """Detects bugs and issues in code"""

    def __init__(self):
        """Initialize bug detector"""
        self.bugs_found: List[BugReport] = []

    def analyze_file(self, file_path: str) -> List[BugReport]:
        """
        Analyze a file for bugs

        Args:
            file_path: Path to file to analyze

        Returns:
            List of bug reports
        """
        self.bugs_found = []

        if not os.path.exists(file_path):
            return self.bugs_found

        # Get file extension
        ext = Path(file_path).suffix.lower()

        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return self.bugs_found

        # Run analysis based on file type
        if ext in ['.py']:
            self._analyze_python(lines, file_path)
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            self._analyze_javascript(lines, file_path)
        elif ext in ['.java']:
            self._analyze_java(lines, file_path)
        elif ext in ['.c', '.cpp', '.cc', '.h', '.hpp']:
            self._analyze_c_cpp(lines, file_path)
        else:
            self._analyze_generic(lines, file_path)

        return self.bugs_found

    def analyze_code_snippet(self, code: str, language: str = "python") -> List[BugReport]:
        """
        Analyze a code snippet for bugs

        Args:
            code: Code snippet to analyze
            language: Programming language

        Returns:
            List of bug reports
        """
        self.bugs_found = []
        lines = code.split('\n')

        if language.lower() in ['python', 'py']:
            self._analyze_python(lines, "snippet")
        elif language.lower() in ['javascript', 'js', 'typescript', 'ts']:
            self._analyze_javascript(lines, "snippet")
        elif language.lower() == 'java':
            self._analyze_java(lines, "snippet")
        elif language.lower() in ['c', 'cpp', 'c++']:
            self._analyze_c_cpp(lines, "snippet")
        else:
            self._analyze_generic(lines, "snippet")

        return self.bugs_found

    def _analyze_python(self, lines: List[str], file_path: str):
        """Analyze Python code for bugs"""

        for i, line in enumerate(lines, 1):
            # Bare except clause
            if re.search(r'except\s*:', line):
                self.bugs_found.append(BugReport(
                    severity="medium",
                    bug_type="exception_handling",
                    description="Bare except clause catches all exceptions, including system exits",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use specific exception types: except Exception: or except SpecificError:"
                ))

            # SQL injection risk
            if re.search(r'execute\s*\([^)]*%|execute\s*\([^)]*\+|execute\s*\([^)]*f["\']', line):
                self.bugs_found.append(BugReport(
                    severity="critical",
                    bug_type="security",
                    description="Potential SQL injection vulnerability",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use parameterized queries with placeholders"
                ))

            # eval() usage
            if re.search(r'\beval\s*\(', line):
                self.bugs_found.append(BugReport(
                    severity="high",
                    bug_type="security",
                    description="eval() can execute arbitrary code, security risk",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use ast.literal_eval() for safe evaluation or find alternative approach"
                ))

            # Hardcoded credentials
            if re.search(r'(password|passwd|pwd|secret|token|api_key)\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                self.bugs_found.append(BugReport(
                    severity="critical",
                    bug_type="security",
                    description="Hardcoded credentials detected",
                    location=file_path,
                    line_number=i,
                    code_snippet="[REDACTED]",
                    suggested_fix="Use environment variables or secure credential storage"
                ))

            # Unused variable (simple check)
            if re.search(r'^\s*\w+\s*=\s*.+$', line) and not re.search(r'self\.|global |return ', line):
                var_name = re.match(r'^\s*(\w+)\s*=', line)
                if var_name:
                    # This is a simplified check; a real analyzer would track usage
                    pass  # Would need more context to determine if truly unused

    def _analyze_javascript(self, lines: List[str], file_path: str):
        """Analyze JavaScript/TypeScript code for bugs"""

        for i, line in enumerate(lines, 1):
            # == instead of ===
            if re.search(r'==(?!=)', line) and not re.search(r'===', line):
                self.bugs_found.append(BugReport(
                    severity="low",
                    bug_type="type_safety",
                    description="Using == instead of === can lead to type coercion bugs",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use === for strict equality comparison"
                ))

            # eval() usage
            if re.search(r'\beval\s*\(', line):
                self.bugs_found.append(BugReport(
                    severity="high",
                    bug_type="security",
                    description="eval() can execute arbitrary code, security risk",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use JSON.parse() or find alternative approach"
                ))

            # innerHTML with variable (XSS risk)
            if re.search(r'innerHTML\s*=\s*[^"\']*(?:\$\{|`)', line):
                self.bugs_found.append(BugReport(
                    severity="critical",
                    bug_type="security",
                    description="Potential XSS vulnerability using innerHTML with variables",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use textContent or sanitize input with DOMPurify"
                ))

            # console.log in production
            if re.search(r'console\.(log|debug|info|warn|error)', line):
                self.bugs_found.append(BugReport(
                    severity="low",
                    bug_type="code_quality",
                    description="console.log statement (may leak sensitive info in production)",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Remove console.log or use a proper logging library"
                ))

    def _analyze_java(self, lines: List[str], file_path: str):
        """Analyze Java code for bugs"""

        for i, line in enumerate(lines, 1):
            # Empty catch block
            if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', line):
                self.bugs_found.append(BugReport(
                    severity="medium",
                    bug_type="exception_handling",
                    description="Empty catch block swallows exceptions",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Add proper error handling or logging"
                ))

            # == for string comparison
            if re.search(r'String\s+\w+.*==', line):
                self.bugs_found.append(BugReport(
                    severity="high",
                    bug_type="logic_error",
                    description="Using == to compare strings (compares references, not values)",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use .equals() method for string comparison"
                ))

    def _analyze_c_cpp(self, lines: List[str], file_path: str):
        """Analyze C/C++ code for bugs"""

        for i, line in enumerate(lines, 1):
            # Buffer overflow risk
            if re.search(r'\b(gets|strcpy|strcat|sprintf)\s*\(', line):
                self.bugs_found.append(BugReport(
                    severity="critical",
                    bug_type="security",
                    description="Unsafe function that can cause buffer overflow",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Use safe alternatives: fgets, strncpy, strncat, snprintf"
                ))

            # Memory leak potential
            if re.search(r'\bmalloc\s*\(', line) or re.search(r'\bnew\s+', line):
                # Would need flow analysis to check for corresponding free/delete
                pass

    def _analyze_generic(self, lines: List[str], file_path: str):
        """Generic analysis for any file type"""

        for i, line in enumerate(lines, 1):
            # TODO/FIXME comments
            if re.search(r'(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE):
                self.bugs_found.append(BugReport(
                    severity="low",
                    bug_type="code_quality",
                    description="Code contains TODO/FIXME marker",
                    location=file_path,
                    line_number=i,
                    code_snippet=line.strip(),
                    suggested_fix="Address the TODO item"
                ))

            # Hardcoded IP addresses
            if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line):
                if not re.search(r'(127\.0\.0\.1|0\.0\.0\.0|localhost)', line):
                    self.bugs_found.append(BugReport(
                        severity="medium",
                        bug_type="configuration",
                        description="Hardcoded IP address",
                        location=file_path,
                        line_number=i,
                        code_snippet=line.strip(),
                        suggested_fix="Use configuration files or environment variables"
                    ))

    def get_summary(self) -> Dict[str, int]:
        """
        Get summary of bugs found

        Returns:
            Dictionary with bug counts by severity
        """
        summary = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "total": len(self.bugs_found)
        }

        for bug in self.bugs_found:
            summary[bug.severity] += 1

        return summary

    def format_report(self) -> str:
        """
        Format bug report as string

        Returns:
            Formatted bug report
        """
        if not self.bugs_found:
            return "No bugs detected!"

        report = []
        report.append("=" * 80)
        report.append("BUG DETECTION REPORT")
        report.append("=" * 80)

        summary = self.get_summary()
        report.append(f"Total Issues: {summary['total']}")
        report.append(f"  Critical: {summary['critical']}")
        report.append(f"  High:     {summary['high']}")
        report.append(f"  Medium:   {summary['medium']}")
        report.append(f"  Low:      {summary['low']}")
        report.append("")

        # Group by severity
        for severity in ['critical', 'high', 'medium', 'low']:
            bugs = [b for b in self.bugs_found if b.severity == severity]
            if bugs:
                report.append(f"\n{'='*80}")
                report.append(f"{severity.upper()} SEVERITY ISSUES ({len(bugs)})")
                report.append(f"{'='*80}")

                for i, bug in enumerate(bugs, 1):
                    report.append(f"\n{i}. [{bug.bug_type.upper()}] {bug.description}")
                    report.append(f"   Location: {bug.location}")
                    if bug.line_number:
                        report.append(f"   Line: {bug.line_number}")
                    if bug.code_snippet:
                        report.append(f"   Code: {bug.code_snippet}")
                    if bug.suggested_fix:
                        report.append(f"   Fix: {bug.suggested_fix}")

        report.append("\n" + "=" * 80)

        return "\n".join(report)
