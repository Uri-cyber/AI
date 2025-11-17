# 🆓 LOCAL MODE - No API Tokens Required!

**Run your own AI troubleshooting assistant completely FREE with no API costs!**

This guide shows you how to use the AI Troubleshooting Assistant **without any API tokens** - everything runs locally on your computer.

---

## 🎯 Quick Start (30 seconds)

```bash
# Install minimal dependencies (no cloud AI libraries!)
pip install colorama prompt-toolkit requests

# Run immediately - works out of the box!
python main.py
```

**That's it!** The app will run in rule-based mode automatically.

---

## 🤖 Two Local AI Options

### Option 1: Rule-Based Expert System (Instant, No Setup)

**✅ Pros:**
- Works immediately, no installation
- No internet required
- Zero cost
- Fast responses
- Covers common issues (errors, databases, Docker, networks, etc.)

**How it works:**
- Pattern matching against 100+ troubleshooting scenarios
- Provides step-by-step solutions
- Based on expert knowledge and best practices

**When to use:**
- First time trying the app
- Common, well-known problems
- Quick diagnostics
- No Ollama installed

```bash
# Explicitly use rule-based mode
python main.py  # Uses rule-based by default!
```

---

### Option 2: Ollama (Smarter AI, Requires Setup)

**✅ Pros:**
- Much smarter responses
- Understands context better
- Can handle complex/unique problems
- Still 100% local and free!

**⚠️ Cons:**
- Requires Ollama installation
- Downloads ~4GB model file
- Needs decent hardware (8GB RAM minimum)

**Setup Ollama:**

```bash
# 1. Install Ollama
# macOS/Linux:
curl https://ollama.ai/install.sh | sh

# Or visit: https://ollama.ai for manual download

# 2. Pull a model (one-time download)
ollama pull llama2        # Recommended (3.8GB)
# OR
ollama pull mistral       # Faster, smaller (4.1GB)
# OR
ollama pull codellama     # Best for code (3.8GB)

# 3. Start Ollama server
ollama serve

# 4. Run the app (in new terminal)
python main.py

# The app will auto-detect and use Ollama!
```

---

## 📋 Comparison

| Feature | Rule-Based | Ollama | Cloud AI (GPT/Claude) |
|---------|-----------|--------|----------------------|
| **Cost** | Free | Free | $$ Paid |
| **Setup Time** | 0 min | 10 min | 2 min |
| **Internet Required** | No | No | Yes |
| **Response Speed** | Instant | 5-30s | 2-10s |
| **Intelligence** | Good | Great | Excellent |
| **Context Understanding** | Limited | Good | Excellent |
| **Custom Problems** | Limited | Good | Excellent |
| **Privacy** | 100% Private | 100% Private | Cloud-based |
| **Hardware Needs** | Minimal | 8GB+ RAM | Minimal |

---

## ⚙️ Configuration

### Auto-Detect Mode (Recommended)

No configuration needed! The app automatically:
1. Checks if Ollama is running
2. Uses Ollama if available
3. Falls back to rule-based if not

```bash
# Just run it!
python main.py
```

### Manual Configuration

Create `.env` file (optional):

```bash
# Force specific mode
AI_PROVIDER=local          # Auto-detect (default)
# AI_PROVIDER=ollama       # Force Ollama
# AI_PROVIDER=rule-based   # Force rule-based

# Ollama settings (optional)
OLLAMA_MODEL=llama2        # Change model
OLLAMA_HOST=http://localhost:11434  # Change host
```

---

## 🚀 Usage Examples

### Example 1: Common Error (Rule-Based Works Great)

```bash
$ python main.py

You: ModuleNotFoundError when running my Python script

AI Assistant:
**Import/Module Error Detected**

Common causes:
1. Package not installed
2. Wrong virtual environment
3. Typo in module name

Solutions:
1. Install the package: `pip install <package-name>`
2. Check you're in correct virtual environment: `which python`
3. Verify package name spelling
...
```

### Example 2: Complex Issue (Ollama Shines)

```bash
$ python main.py

You: My React app renders slowly and I'm seeing memory leaks in Chrome DevTools

AI Assistant:
Based on your description, you're experiencing performance issues likely related to:

1. Unnecessary re-renders - Check if you're creating new objects/functions in render
2. Missing React.memo() or useMemo() optimizations
3. Event listeners not being cleaned up

Let's diagnose step by step:
- First, use React DevTools Profiler to identify which components re-render most
- Check for missing dependencies in useEffect hooks
...
```

---

## 💡 Tips for Best Results

### With Rule-Based Mode:
- Be specific about error types ("ModuleNotFoundError" vs "error")
- Include error codes ("exit code 137")
- Mention technology stack ("Docker", "PostgreSQL", "Python")

### With Ollama:
- Provide context about what you were doing
- Include relevant code snippets
- Describe what you've already tried
- Ask follow-up questions for clarification

---

## 🔧 Troubleshooting

### "Ollama not detected, using rule-based mode"

**This is normal!** It means Ollama isn't running. To fix:

```bash
# Start Ollama in a terminal
ollama serve

# Then run the app in another terminal
python main.py
```

### Ollama is slow

**Normal behavior.** Local AI takes time:
- First response: 10-30 seconds (loading model)
- Follow-up responses: 5-15 seconds
- Faster on M1/M2 Macs and modern GPUs

**To speed up:**
- Use a smaller model: `ollama pull phi` (1.6GB)
- Close other applications
- Ensure Ollama uses GPU (automatic on Mac/NVIDIA)

### Out of memory

**Ollama needs RAM:**
- llama2: Needs 8GB RAM
- phi: Needs 4GB RAM
- mistral: Needs 8GB RAM

**Solutions:**
- Use smaller model: `ollama pull phi`
- Close other applications
- Use rule-based mode instead

---

## 🎓 Recommended Models

**For general troubleshooting:**
```bash
ollama pull llama2       # Best balance
```

**For code-specific issues:**
```bash
ollama pull codellama    # Optimized for code
```

**For low-end hardware:**
```bash
ollama pull phi          # Smallest, fastest
```

**For best quality (if you have 16GB+ RAM):**
```bash
ollama pull mixtral      # Most capable
```

---

## 📊 Hardware Requirements

### Rule-Based Mode:
- CPU: Any
- RAM: 1GB
- Disk: 50MB
- Internet: No

### Ollama Mode:
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Disk: 5-10GB for models
- GPU: Optional (speeds up significantly)
- Internet: Only for initial model download

---

## 🔒 Privacy & Security

**Everything stays local:**
- No data sent to cloud
- No API calls
- No tracking
- No internet required (after model download)

**Your code and errors never leave your machine!**

---

## ❓ FAQ

**Q: Do I need API tokens?**
A: No! Local mode requires zero tokens.

**Q: Which mode should I use?**
A: Start with rule-based (instant). If you want smarter AI and have decent hardware, use Ollama.

**Q: Can I use both?**
A: Yes! The app auto-detects. Stop Ollama to fall back to rule-based.

**Q: Is Ollama really free?**
A: Yes, completely free and open source!

**Q: How do I switch modes?**
A: Set `AI_PROVIDER` in `.env` or just start/stop Ollama.

**Q: Can I use this offline?**
A: Yes! Both modes work 100% offline (after Ollama model download).

**Q: What if I want better AI than Ollama?**
A: Use cloud AI (Claude/GPT) with API tokens. See main README.

---

## 🎯 Command Reference

```bash
# Run with auto-detect (recommended)
python main.py

# Force rule-based mode
AI_PROVIDER=rule-based python main.py

# Force Ollama mode
AI_PROVIDER=ollama python main.py

# Analyze file (no AI needed!)
python main.py analyze-file yourcode.py

# Quick debug with rule-based
python main.py debug --problem "Docker container crashing"

# Interactive mode
python cli.py
```

---

## 🌟 What's Next?

1. **Try it now** - Works out of the box with rule-based mode
2. **Install Ollama** - For smarter AI (10-minute setup)
3. **Experiment** - Try different Ollama models
4. **Give feedback** - Let us know what works!

---

**Enjoy FREE AI troubleshooting with no API costs! 🎉**
