# 🤖 AI Troubleshooting Assistant

An intelligent AI-powered debugging and troubleshooting tool that helps developers find bugs, diagnose issues, and solve technical problems. Built with advanced code analysis, comprehensive logging, and conversational AI.

## 🆓 **NEW: 100% FREE LOCAL MODE - No API Tokens Required!**

**Run your own AI completely FREE with zero API costs!**

```bash
pip install colorama prompt-toolkit requests
python main.py  # Works instantly - no tokens needed!
```

✅ **Works out of the box** - No configuration required
✅ **No API costs** - Everything runs locally
✅ **No internet needed** - Fully offline capable
✅ **100% Private** - Your code never leaves your machine

**👉 [See LOCAL_MODE.md for complete guide](LOCAL_MODE.md)**

Choose your mode:
- **Rule-Based (Default)** - Instant, works anywhere, no setup
- **Ollama** - Smarter local AI, free, requires Ollama installation
- **Cloud AI** - Best quality, requires API tokens (Claude/GPT)

---

## ✨ Features

### 🔍 Automated Bug Detection
- **Static Code Analysis**: Automatically scans code for common bugs and vulnerabilities
- **Multi-Language Support**: Python, JavaScript/TypeScript, Java, C/C++
- **Security Vulnerability Detection**: Identifies SQL injection, XSS, hardcoded credentials, and more
- **Code Quality Checks**: Finds anti-patterns, performance issues, and code smells

### 🤖 AI-Powered Troubleshooting
- **Conversational Interface**: Natural language interaction for problem-solving
- **Context-Aware Analysis**: Understands your codebase and environment
- **Step-by-Step Solutions**: Provides actionable troubleshooting steps
- **Root Cause Analysis**: Identifies underlying issues, not just symptoms

### 📊 Comprehensive Logging
- **Session Tracking**: Records all troubleshooting sessions
- **Issue Cataloging**: Logs bugs, errors, and malfunctions
- **Diagnostic Reports**: Generates detailed analysis reports
- **JSON Export**: Export session data for further analysis

### 💬 Multiple Interaction Modes
- **Interactive CLI**: Full-featured command-line interface
- **Quick Debug**: One-command debugging for fast troubleshooting
- **File Analysis**: Batch analyze files for bugs
- **Code Snippet Analysis**: Analyze code snippets on the fly

## 🚀 Quick Start

### Option 1: Local Mode (Recommended - FREE!)

```bash
# 1. Install minimal dependencies
pip install colorama prompt-toolkit requests

# 2. Run immediately - no configuration needed!
python main.py
```

**That's it!** Works instantly with rule-based AI. No tokens, no setup, no cost.

**Want smarter AI?** Install [Ollama](https://ollama.ai) (free, local):
```bash
ollama pull llama2
ollama serve
python main.py  # Auto-detects and uses Ollama!
```

### Option 2: Cloud AI (Requires API Tokens)

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY

# 3. Set provider
echo "AI_PROVIDER=anthropic" >> .env  # or "openai"

# 4. Run
python main.py
```

## 📖 Usage

### Interactive Mode

Start the full interactive CLI:

```bash
python main.py
```

Features in interactive mode:
- Natural conversation with AI assistant
- `/help` - Show available commands
- `/reset` - Start new troubleshooting session
- `/summary` - View conversation history
- `/quit` - Exit the application

### Analyze Files for Bugs

Scan a file for potential bugs and security issues:

```bash
# Analyze a Python file
python main.py analyze-file app.py

# Save report to file
python main.py analyze-file app.py -o report.txt
```

### Quick Debug

Get instant AI help for a specific problem:

```bash
# Simple debugging
python main.py debug --problem "My application crashes on startup"

# With error message
python main.py debug --problem "Database connection fails" --error "ConnectionRefusedError: [Errno 111]"

# With code file
python main.py debug --problem "Function returns wrong value" --file mycode.py

# Save troubleshooting logs
python main.py debug --problem "Memory leak" --save-logs
```

### Analyze Code Snippets

Analyze code without saving to a file:

```bash
# From command line
python main.py analyze-code --code "password = 'admin123'" --language python

# From file
python main.py analyze-code --file snippet.py --language python

# From stdin
echo "eval(user_input)" | python main.py analyze-code
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# AI Provider (anthropic or openai)
AI_PROVIDER=anthropic

# Anthropic API Key (for Claude)
ANTHROPIC_API_KEY=your_key_here

# OpenAI API Key (for GPT)
OPENAI_API_KEY=your_key_here

# Model Selection
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
OPENAI_MODEL=gpt-4-turbo-preview
```

### Choosing an AI Provider

#### Anthropic Claude (Recommended)
- Superior code understanding and debugging
- Better at complex technical analysis
- More thorough security vulnerability detection

#### OpenAI GPT
- Fast response times
- Good general troubleshooting
- Wide knowledge base

## 📝 Bug Detection Capabilities

### Security Issues (Critical/High)
- SQL Injection vulnerabilities
- Cross-Site Scripting (XSS)
- Hardcoded credentials
- `eval()` usage
- Buffer overflow risks (C/C++)
- Unsafe string functions

### Logic Errors (High/Medium)
- String comparison with `==` in Java
- Type coercion issues in JavaScript
- Bare except clauses in Python
- Empty catch blocks

### Code Quality (Low/Medium)
- TODO/FIXME markers
- Hardcoded IP addresses
- Console.log statements
- Code smells and anti-patterns

## 📊 Logging and Reports

All troubleshooting sessions are automatically logged to the `logs/` directory:

### Log Files Generated

- `session_YYYYMMDD_HHMMSS.log` - Detailed session log
- `issues_YYYYMMDD_HHMMSS.log` - Issues and warnings only
- `session_YYYYMMDD_HHMMSS.json` - Structured session data
- `summary_YYYYMMDD_HHMMSS.txt` - Human-readable summary

### Log Contents

- Problems analyzed
- Bugs and issues found
- Diagnostic information
- Solutions provided
- AI interactions
- Timestamps and severity levels

## 🎯 Use Cases

### For Developers
- Debug runtime errors and exceptions
- Find security vulnerabilities before deployment
- Get help with unfamiliar error messages
- Learn best practices and fixes

### For Code Reviewers
- Automated code quality checks
- Security vulnerability scanning
- Identify potential bugs early
- Generate bug reports

### For DevOps/SRE
- Troubleshoot system issues
- Diagnose performance problems
- Analyze logs and error messages
- Network connectivity debugging

### For Students
- Learn debugging techniques
- Understand error messages
- Get explanations for code issues
- Improve code quality

## 🛠️ Advanced Features

### Programmatic Usage

Use the AI engine in your own Python scripts:

```python
from ai_engine import TroubleshootingEngine

# Initialize
engine = TroubleshootingEngine(provider="anthropic")

# Troubleshoot a problem
response = engine.troubleshoot(
    problem="Application crashes on startup",
    context="Error: NameError: name 'config' is not defined"
)

print(response)

# Analyze code
from bug_detector import BugDetector

detector = BugDetector()
bugs = detector.analyze_file("myapp.py")

for bug in bugs:
    print(f"{bug.severity}: {bug.description}")

# Save session
engine.save_session()
```

### Custom Logging

```python
from logger import TroubleshootingLogger

logger = TroubleshootingLogger(log_dir="custom_logs")
logger.log_session_start("anthropic", "claude-sonnet-4")
logger.log_bug_detected("SQL injection", "app.py:42", "Use parameterized queries")
logger.log_session_end()
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for educational and professional use.

## 🙏 Acknowledgments

- Built with Anthropic Claude and OpenAI GPT
- Uses colorama for terminal colors
- Uses prompt-toolkit for enhanced CLI

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the logs for detailed error information
- Use the `/help` command in interactive mode

---

**Happy Debugging! 🐛🔨**
