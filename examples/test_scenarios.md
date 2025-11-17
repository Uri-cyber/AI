# Test Scenarios for AI Troubleshooting Assistant

## Scenario 1: Runtime Error Debugging

**Problem**: "My Python script crashes with 'KeyError: config'"

**How to test**:
```bash
python main.py debug --problem "Script crashes with KeyError: config"
```

**Expected**: AI should suggest checking dictionary keys, using .get() method, or adding error handling.

---

## Scenario 2: Performance Issue

**Problem**: "My web application is very slow, taking 30 seconds to load"

**How to test**:
```bash
python main.py debug --problem "Web app slow, 30s load time" --context "Django application with 1000+ users"
```

**Expected**: AI should suggest:
- Database query optimization
- Caching strategies
- Profiling tools
- Network diagnostics

---

## Scenario 3: Security Vulnerability Scan

**Problem**: Analyze code for security issues

**How to test**:
```bash
python main.py analyze-file examples/buggy_code.py
```

**Expected**: Should detect:
- Hardcoded credentials (CRITICAL)
- SQL injection vulnerability (CRITICAL)
- eval() usage (HIGH)
- Other security issues

---

## Scenario 4: Database Connection Error

**Problem**: "Cannot connect to PostgreSQL database"

**How to test**:
```bash
python main.py debug --problem "Cannot connect to PostgreSQL" --error "psycopg2.OperationalError: could not connect to server: Connection refused"
```

**Expected**: AI should suggest:
- Check if PostgreSQL is running
- Verify connection parameters
- Check firewall rules
- Validate credentials

---

## Scenario 5: Import Error

**Problem**: "ModuleNotFoundError when running script"

**How to test**:
```bash
python main.py debug --problem "Getting ModuleNotFoundError for requests module"
```

**Expected**: AI should suggest:
- Installing the module with pip
- Checking virtual environment
- Verifying PYTHONPATH
- Checking for typos in import statement

---

## Scenario 6: Memory Leak Investigation

**Problem**: "Application memory usage keeps growing"

**How to test**:
```bash
python main.py debug --problem "Memory leak, RAM usage grows from 100MB to 2GB" --save-logs
```

**Expected**: AI should suggest:
- Using memory profilers
- Checking for circular references
- Looking for unclosed resources
- Analyzing object lifecycle

---

## Scenario 7: API Integration Issue

**Problem**: "REST API returns 401 Unauthorized"

**How to test**:
```bash
python main.py debug --problem "API returns 401 Unauthorized" --context "Using requests library with API key in header"
```

**Expected**: AI should suggest:
- Verify API key is correct
- Check authentication method
- Examine request headers
- Test with curl/Postman
- Check API documentation

---

## Scenario 8: Docker Container Crash

**Problem**: "Docker container keeps restarting"

**How to test**:
```bash
python main.py debug --problem "Docker container keeps restarting with exit code 137"
```

**Expected**: AI should identify:
- Exit code 137 = killed by SIGKILL
- Likely out of memory
- Suggest increasing memory limits
- Check application memory usage

---

## Scenario 9: Code Quality Review

**Problem**: Review code for quality issues

**How to test**:
```bash
python main.py analyze-code --file examples/buggy_code.py --language python
```

**Expected**: Should find:
- TODO/FIXME markers
- Unused variables
- Code smells
- Best practice violations

---

## Scenario 10: JavaScript Bug Detection

**Problem**: Analyze JavaScript code

**How to test**:
```bash
echo "if (user.name == null) { user.innerHTML = username; }" | python main.py analyze-code --language javascript
```

**Expected**: Should detect:
- Using == instead of ===
- Potential XSS vulnerability with innerHTML

---

## Interactive Mode Testing

**Test the full CLI**:
```bash
python main.py
```

**Commands to try**:
1. Type: "My Python script throws a TypeError"
2. Type: "/help" to see commands
3. Type: "/reset" to start new session
4. Type: "/summary" to see history
5. Type: "/quit" to exit

---

## Logging Verification

**Test log generation**:
```bash
python main.py debug --problem "Test logging" --save-logs
ls -la logs/
cat logs/session_*.log
cat logs/summary_*.txt
```

**Expected**: Should create:
- Session log file
- Issues log file
- JSON data file
- Summary report

---

## Batch File Analysis

**Test analyzing multiple files**:
```bash
for file in *.py; do
    echo "Analyzing $file"
    python main.py analyze-file "$file"
done
```

---

## Edge Cases

### Empty Input
```bash
python main.py debug --problem ""
```

### Very Long Error Message
```bash
python main.py debug --problem "Error" --error "$(cat /var/log/syslog)"
```

### Non-existent File
```bash
python main.py analyze-file nonexistent.py
```

### Invalid Language
```bash
python main.py analyze-code --code "test" --language "brainfuck"
```

---

## Success Criteria

✅ AI provides helpful, actionable advice
✅ Bug detection finds security vulnerabilities
✅ Logs are created and contain useful information
✅ CLI is responsive and user-friendly
✅ Error handling works gracefully
✅ Multi-language support works correctly
✅ Session data is saved properly
