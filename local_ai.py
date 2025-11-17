"""
Local AI Provider - No API tokens required!
Supports Ollama and rule-based expert system
"""

import json
import re
import requests
from typing import Optional, Dict, List


class OllamaProvider:
    """Local LLM using Ollama"""

    def __init__(self, model: str = "llama2", host: str = "http://localhost:11434"):
        """
        Initialize Ollama provider

        Args:
            model: Ollama model name (llama2, mistral, codellama, etc.)
            host: Ollama API host
        """
        self.model = model
        self.host = host
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def generate(self, prompt: str, system: str = "") -> str:
        """
        Generate response using Ollama

        Args:
            prompt: User prompt
            system: System prompt

        Returns:
            Generated response
        """
        if not self.available:
            raise RuntimeError("Ollama is not running. Start it with: ollama serve")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }

        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.Timeout:
            raise RuntimeError("Ollama request timed out. Try a smaller model or increase timeout.")
        except Exception as e:
            raise RuntimeError(f"Ollama error: {str(e)}")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Chat completion using Ollama

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            AI response
        """
        if not self.available:
            raise RuntimeError("Ollama is not running. Start it with: ollama serve")

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
        except Exception as e:
            raise RuntimeError(f"Ollama chat error: {str(e)}")


class RuleBasedAI:
    """Rule-based expert system - works offline, no dependencies"""

    def __init__(self):
        """Initialize rule-based AI"""
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> List[Dict]:
        """Load troubleshooting patterns"""
        return [
            # Python errors
            {
                "patterns": [r"ModuleNotFoundError", r"No module named", r"import.*error"],
                "category": "import_error",
                "response": """**Import/Module Error Detected**

Common causes:
1. Package not installed
2. Wrong virtual environment
3. Typo in module name
4. Package not in PYTHONPATH

Solutions:
1. Install the package: `pip install <package-name>`
2. Check you're in correct virtual environment: `which python`
3. Verify package name spelling
4. Check if package exists: `pip list | grep <package>`
5. Update pip: `pip install --upgrade pip`
6. For local modules, check PYTHONPATH: `echo $PYTHONPATH`

Debugging steps:
- Run: `python -m pip list` to see installed packages
- Check Python version compatibility
- Try creating fresh virtual environment"""
            },
            # Database errors
            {
                "patterns": [r"connection.*refused", r"could not connect", r"database.*error"],
                "category": "database_error",
                "response": """**Database Connection Error**

Common causes:
1. Database server not running
2. Wrong connection credentials
3. Firewall blocking connection
4. Wrong host/port
5. Database not initialized

Solutions:
1. Check if database is running:
   - PostgreSQL: `sudo systemctl status postgresql`
   - MySQL: `sudo systemctl status mysql`
   - MongoDB: `sudo systemctl status mongod`

2. Verify connection parameters:
   - Host (localhost vs 127.0.0.1)
   - Port (PostgreSQL: 5432, MySQL: 3306, MongoDB: 27017)
   - Username and password
   - Database name

3. Test connection:
   - PostgreSQL: `psql -h localhost -U username -d database`
   - MySQL: `mysql -h localhost -u username -p`

4. Check firewall:
   - `sudo ufw status`
   - Allow port if needed: `sudo ufw allow 5432/tcp`

5. Check logs for detailed errors"""
            },
            # Performance issues
            {
                "patterns": [r"slow", r"performance", r"taking.*long", r"timeout", r"latency"],
                "category": "performance",
                "response": """**Performance Issue Detected**

Investigation steps:
1. Identify bottleneck:
   - CPU: `top` or `htop`
   - Memory: `free -h`
   - Disk I/O: `iostat`
   - Network: `iftop` or `nethogs`

2. Application profiling:
   - Python: Use `cProfile` or `line_profiler`
   - Node.js: Use `clinic` or `0x`
   - General: `strace` for system calls

3. Common causes:
   - Database queries (N+1 problem)
   - No caching
   - Large file operations
   - Memory leaks
   - Network latency
   - Blocking operations

4. Quick fixes:
   - Add database indexes
   - Implement caching (Redis, Memcached)
   - Use connection pooling
   - Optimize queries (EXPLAIN)
   - Use async/await for I/O
   - Add pagination
   - Compress responses (gzip)
   - Use CDN for static files

5. Monitoring:
   - Set up APM (New Relic, DataDog)
   - Monitor logs for slow queries
   - Track response times"""
            },
            # Docker issues
            {
                "patterns": [r"docker.*exit.*137", r"container.*killed", r"oom"],
                "category": "docker_oom",
                "response": """**Docker Container Out of Memory (Exit 137)**

Exit code 137 = 128 + 9 (SIGKILL) - Container killed due to OOM

Solutions:
1. Increase memory limit:
   ```bash
   docker run -m 512m --memory-swap 1g your-image
   # or in docker-compose.yml:
   mem_limit: 512m
   memswap_limit: 1g
   ```

2. Check memory usage:
   ```bash
   docker stats
   docker inspect <container> | grep Memory
   ```

3. Optimize application:
   - Fix memory leaks
   - Reduce worker processes
   - Add pagination
   - Clear caches periodically
   - Use streaming for large data

4. Investigate:
   ```bash
   docker logs <container>
   dmesg | grep -i oom
   ```

5. Set memory reservation:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
       reservations:
         memory: 256M
   ```"""
            },
            # File permissions
            {
                "patterns": [r"permission denied", r"access denied", r"forbidden"],
                "category": "permission_error",
                "response": """**Permission Denied Error**

Common causes:
1. Insufficient file permissions
2. Wrong file ownership
3. SELinux/AppArmor restrictions
4. Running without sudo when required

Solutions:
1. Check permissions:
   ```bash
   ls -la <file>
   ```

2. Fix ownership:
   ```bash
   sudo chown user:group <file>
   sudo chown -R user:group <directory>
   ```

3. Fix permissions:
   ```bash
   chmod 644 <file>      # Read/write for owner, read for others
   chmod 755 <directory> # Full for owner, read/execute for others
   chmod +x <script>     # Make executable
   ```

4. Check if sudo needed:
   ```bash
   sudo <command>
   ```

5. For Docker:
   - Run with user: `docker run --user $(id -u):$(id -g)`
   - Or fix permissions in container

6. Check SELinux:
   ```bash
   getenforce
   sudo setenforce 0  # Temporarily disable to test
   ```"""
            },
            # Network issues
            {
                "patterns": [r"connection timeout", r"network.*unreachable", r"dns.*fail"],
                "category": "network_error",
                "response": """**Network Connection Error**

Diagnostic steps:
1. Test connectivity:
   ```bash
   ping google.com
   ping 8.8.8.8  # Test without DNS
   curl -I https://example.com
   ```

2. Check DNS:
   ```bash
   nslookup example.com
   dig example.com
   # Test different DNS: dig @8.8.8.8 example.com
   ```

3. Check firewall:
   ```bash
   sudo iptables -L
   sudo ufw status
   ```

4. Check routing:
   ```bash
   traceroute example.com
   ip route show
   ```

5. Check if port is open:
   ```bash
   telnet example.com 80
   nc -zv example.com 80
   ```

6. Check proxy settings:
   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```

Common fixes:
- Restart network: `sudo systemctl restart NetworkManager`
- Flush DNS: `sudo systemd-resolve --flush-caches`
- Check /etc/hosts for conflicts
- Disable VPN temporarily
- Check if behind corporate firewall"""
            },
            # Memory errors
            {
                "patterns": [r"out of memory", r"memory.*error", r"malloc.*fail"],
                "category": "memory_error",
                "response": """**Out of Memory Error**

Investigation:
1. Check memory usage:
   ```bash
   free -h
   top -o %MEM
   ps aux --sort=-%mem | head
   ```

2. Check for memory leaks:
   - Python: Use `tracemalloc` or `memory_profiler`
   - Node.js: Use `--inspect` and Chrome DevTools
   - C/C++: Use `valgrind`

3. Solutions:
   - Increase system RAM
   - Add swap space
   - Optimize code to use less memory
   - Process data in chunks/streams
   - Clear caches periodically
   - Fix memory leaks
   - Reduce concurrency

4. Add swap (temporary):
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

5. Monitor memory:
   ```bash
   watch -n 1 free -h
   vmstat 1
   ```"""
            },
            # Generic errors
            {
                "patterns": [r"error", r"exception", r"fail", r"crash"],
                "category": "generic_error",
                "response": """**Error Troubleshooting Guide**

General debugging approach:
1. Read the full error message carefully
2. Note the exact error type and location
3. Check recent changes (code, config, dependencies)
4. Search for the exact error message online
5. Check logs for additional context

Common debugging techniques:
1. Add logging/print statements
2. Use debugger (pdb for Python, gdb for C/C++)
3. Isolate the problem (minimal reproduction)
4. Check environment variables
5. Verify all dependencies are installed
6. Test with different inputs
7. Review documentation
8. Check version compatibility

Error investigation checklist:
☐ Read complete error message and stack trace
☐ Identify which line/file causes error
☐ Check if it's reproducible
☐ Review recent changes
☐ Check logs
☐ Verify configuration
☐ Test with minimal example
☐ Check dependencies and versions
☐ Search error online
☐ Ask for help with full context"""
            }
        ]

    def analyze(self, problem: str, context: Optional[str] = None) -> str:
        """
        Analyze problem using rule-based system

        Args:
            problem: Problem description
            context: Additional context

        Returns:
            Troubleshooting advice
        """
        combined = f"{problem} {context or ''}".lower()

        # Find matching patterns
        matches = []
        for pattern_group in self.patterns:
            for pattern in pattern_group["patterns"]:
                if re.search(pattern, combined, re.IGNORECASE):
                    matches.append(pattern_group)
                    break

        if matches:
            # Return the best match
            response = matches[0]["response"]

            # Add additional matches if relevant
            if len(matches) > 1:
                response += "\n\n**Also see:**\n"
                for match in matches[1:3]:  # Up to 2 additional
                    response += f"- {match['category'].replace('_', ' ').title()}\n"

            return response
        else:
            # Generic troubleshooting advice
            return self._generic_advice(problem)

    def _generic_advice(self, problem: str) -> str:
        """Provide generic troubleshooting advice"""
        return f"""**Troubleshooting: {problem[:50]}...**

Since I couldn't identify a specific pattern, here's a general debugging approach:

**1. Gather Information:**
- What exactly is the error message?
- When does it occur?
- What changed recently?
- Can you reproduce it?

**2. Debugging Steps:**
1. Check logs for detailed error messages
2. Verify configuration files
3. Test with minimal example
4. Check environment variables
5. Verify all dependencies are installed
6. Look for recent changes (code, config, packages)

**3. Common Issues:**
- Missing dependencies: Run package manager (pip, npm, etc.)
- Permission issues: Check file/folder permissions
- Configuration errors: Verify config files
- Version conflicts: Check compatibility
- Resource limits: Check memory, disk space, CPU

**4. Get More Help:**
- Search exact error message online
- Check official documentation
- Look for similar issues on Stack Overflow
- Check project's GitHub issues
- Provide full error stack trace when asking for help

**5. Prevention:**
- Use version control (git)
- Keep dependencies updated
- Write tests
- Monitor logs
- Document configuration
- Use linting and type checking

Would you like to provide more details about the error?"""


def get_local_ai(provider_type: str = "auto", **kwargs):
    """
    Get local AI provider

    Args:
        provider_type: 'ollama', 'rule-based', or 'auto'
        **kwargs: Additional arguments for provider

    Returns:
        AI provider instance
    """
    if provider_type == "auto":
        # Try Ollama first
        ollama = OllamaProvider(**kwargs)
        if ollama.available:
            return ollama
        # Fallback to rule-based
        return RuleBasedAI()

    elif provider_type == "ollama":
        return OllamaProvider(**kwargs)

    elif provider_type == "rule-based":
        return RuleBasedAI()

    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
