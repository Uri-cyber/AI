# 🚀 Quick Start Guide

Get started with the AI Troubleshooting Assistant in 3 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API key from Anthropic (Claude) or OpenAI (GPT)

## Step 1: Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# or
vim .env
```

Add your API key:
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**Get API Keys:**
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/api-keys

## Step 3: Run!

### Interactive Mode (Recommended for First Time)
```bash
python main.py
```

This starts a conversational interface. Try asking:
- "My Python script crashes with a KeyError"
- "How do I debug a memory leak?"
- "Analyze this code: `eval(user_input)`"

### Analyze a File for Bugs
```bash
python main.py analyze-file examples/buggy_code.py
```

This scans the file and reports:
- Security vulnerabilities
- Common bugs
- Code quality issues

### Quick Debug Session
```bash
python main.py debug --problem "My app is slow"
```

Get instant AI help for a specific issue.

## Common Commands

```bash
# Interactive CLI
python main.py

# Analyze file
python main.py analyze-file yourfile.py

# Quick debug
python main.py debug --problem "your issue here"

# Debug with error message
python main.py debug --problem "connection error" --error "ConnectionRefusedError"

# Analyze code snippet
python main.py analyze-code --code "password = 'admin'" --language python

# See all options
python main.py --help
```

## What to Try

### 1. Test Bug Detection
```bash
python main.py analyze-file examples/buggy_code.py
```
Should find 10+ issues including critical security vulnerabilities!

### 2. Interactive Troubleshooting
```bash
python main.py
```
Then type: "My Docker container keeps crashing with exit code 137"

### 3. Get Logs
```bash
python main.py debug --problem "test" --save-logs
ls logs/
```
Check the generated logs!

## Tips

- **Use context**: Provide error messages, logs, or code snippets for better help
- **Be specific**: "Module not found" is better than "error"
- **Save logs**: Use `--save-logs` to keep track of troubleshooting sessions
- **Try examples**: Check `examples/test_scenarios.md` for more ideas

## Troubleshooting the Troubleshooter 😄

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API key not found"
Make sure you:
1. Created `.env` file (copy from `.env.example`)
2. Added your actual API key
3. Set `AI_PROVIDER` correctly

### "Rate limit exceeded"
You've made too many requests. Wait a minute or upgrade your API plan.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try the test scenarios in [examples/test_scenarios.md](examples/test_scenarios.md)
- Integrate into your development workflow
- Use programmatically in your own scripts

## Need Help?

- Use `/help` in interactive mode
- Check the logs in `logs/` directory
- Review [examples/test_scenarios.md](examples/test_scenarios.md)
- Read the full documentation in [README.md](README.md)

---

**Happy Debugging! 🐛🔨**
