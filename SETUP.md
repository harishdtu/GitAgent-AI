# GitAgent Setup Guide

Complete step-by-step guide to get the system running.

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for frontend)
- **npm** or **yarn**
- **Git**
- **Anthropic API Key** (get at https://console.anthropic.com)
- **GitHub Account** (optional, for repository integration)

## Installation

### Step 1: Set Up Environment

```bash
# Clone or navigate to project directory
cd gitagent-project

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."  # Your actual key
# On Windows: set ANTHROPIC_API_KEY=sk-ant-...
```

### Step 2: Install Python Dependencies

```bash
# Install required packages
pip install anthropic gitpython requests

# Verify installation
python -c "import anthropic; print('✓ Anthropic SDK ready')"
python -c "import git; print('✓ GitPython ready')"
```

### Step 3: Set Up Frontend

```bash
# Install Node dependencies
npm install

# Or with yarn
yarn install

# Verify Node setup
npm list next react tailwindcss
```

### Step 4: Verify Setup

```bash
# Check Python setup
python demo.py  # Should print demo info (may need API key to fully run)

# Check frontend setup
npm run build  # Should complete without errors
```

## Running the System

### Option 1: Backend Only (Code Generation)

Perfect for testing the agent system without UI:

```bash
# Run the main orchestrator
python agent_orchestrator.py

# Expected output:
# 🚀 Starting code generation for: smart-api-builder
# ✅ Architecture plan created
# ✅ Code generated
# ✅ Code reviewed
# 📄 Full results saved to: generation_result.json
```

**Output**: `generation_result.json` with complete generation results

### Option 2: Run Demo Script

Educational walkthrough with multiple examples:

```bash
python demo.py

# Shows:
# - Single agent execution
# - Full pipeline
# - Multiple tech stacks
# - Performance metrics
# - Usage patterns
```

### Option 3: Frontend Dashboard

Start the Next.js dashboard:

```bash
# Development mode (hot reload)
npm run dev

# Open browser to http://localhost:3000
# You'll see:
# - Project management interface
# - Agent execution timeline
# - Generation controls
# - Real-time status
```

**First start**: May take 30-60s to compile  
**Subsequent**: Instant hot reload

### Option 4: Full Stack (Recommended)

Run everything together:

```bash
# Terminal 1: Backend service (if needed)
python agent_orchestrator.py

# Terminal 2: Frontend dashboard
npm run dev

# Terminal 3: Monitor logs (optional)
tail -f generation_result.json
```

## Configuration

### API Configuration

Create `.env.local` for frontend:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_PROJECT_NAME=GitAgent
```

Create `.env` for backend:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_... (optional)
PROJECT_ROOT=/path/to/projects
```

### Customizing Tasks

Edit `agent_orchestrator.py` to change the demo task:

```python
task = CodeGenerationTask(
    project_name="your-project-name",
    description="What does this project do?",
    tech_stack="fastapi",  # or "nextjs", "python"
    features=[
        "Feature 1",
        "Feature 2",
        "Feature 3",
    ]
)
```

Supported tech stacks:
- `fastapi` - Python backend
- `nextjs` - Frontend/full-stack
- `python` - CLI tools and utilities

### GitHub Integration

To enable auto-pushing to GitHub:

```bash
# 1. Generate GitHub token
# - Go to https://github.com/settings/tokens
# - Create "Personal access token"
# - Grant: repo, write:packages

# 2. Set environment variable
export GITHUB_TOKEN="ghp_..."

# 3. Update code to use token
orchestrator = GitAgentOrchestrator(github_token=os.getenv("GITHUB_TOKEN"))
```

## Troubleshooting

### Python Issues

**Problem**: `ModuleNotFoundError: No module named 'anthropic'`
```bash
# Solution
pip install anthropic gitpython requests --upgrade
```

**Problem**: `ANTHROPIC_API_KEY not found`
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="sk-..."

# Verify
python -c "import os; print(os.getenv('ANTHROPIC_API_KEY')[:10])"
```

**Problem**: `Async event loop error`
```bash
# Solution: Use Python 3.10+
python --version  # Should be 3.10 or higher
```

### Frontend Issues

**Problem**: `npm: command not found`
```bash
# Install Node.js from https://nodejs.org
node --version  # Should be 18+
npm --version   # Should be 9+
```

**Problem**: `Port 3000 already in use`
```bash
# Use different port
npm run dev -- -p 3001

# Then open http://localhost:3001
```

**Problem**: Build fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API Issues

**Problem**: `401 Unauthorized - Invalid API key`
```bash
# Check key format
echo $ANTHROPIC_API_KEY
# Should start with: sk-ant-

# Get new key from https://console.anthropic.com
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Problem**: `RateLimitError`
```bash
# Add retry logic or wait
# The system includes exponential backoff
# Default: 3 retries with increasing delay
```

**Problem**: `Timeout during generation`
```bash
# Increase timeout
# Default: 60 seconds
# May need longer for complex tasks
```

## Development Workflow

### Making Changes

**Backend Changes**:
```bash
# Edit agent_orchestrator.py
# Test immediately (no server restart needed)
python agent_orchestrator.py
```

**Frontend Changes**:
```bash
# Edit dashboard.tsx or styles
# Auto-reload in browser (if running npm run dev)
# Changes visible in ~1-2 seconds
```

**Testing Changes**:
```bash
# Run full demo
python demo.py

# Run specific test
python -m pytest tests/test_agents.py -v
```

### Debugging

**Enable debug logging**:
```python
# In agent_orchestrator.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Monitor API calls**:
```python
# In agents
print(f"Sending to Claude: {len(prompt)} chars")
print(f"Response: {len(response)} chars")
```

**Check conversation history**:
```python
# Print agent's memory
agent.conversation_history
# Shows all API calls and responses
```

## Deployment

### Local Deployment

1. **Backend**: Keep `agent_orchestrator.py` running in background
2. **Frontend**: Deploy Next.js build:
   ```bash
   npm run build
   npm start
   ```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY agent_orchestrator.py .
CMD ["python", "agent_orchestrator.py"]
```

### Cloud Deployment (Vercel)

For Next.js frontend:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Opens https://your-project.vercel.app
```

## Performance Tuning

### Faster Generation

```python
# Reduce output size
# Architect: max_tokens=1000  (was 1500)
# Developer: max_tokens=2000  (was 3000)
# Reviewer: max_tokens=1000   (was 1500)

# Result: 2-3 seconds faster, slightly less detailed
```

### Lower Cost

```python
# Use faster model
model="claude-haiku-3"  # Cheaper, faster, less capable

# Or batch requests
# Generate multiple tasks in parallel
```

### Better Quality

```python
# Increase thinking time
max_tokens=4000  # More detailed output

# Add more agents
# Test, Documentation, DevOps agents
```

## Monitoring & Metrics

### View Execution Logs

```bash
# Check generation results
cat generation_result.json | python -m json.tool

# Monitor in real-time
tail -f generation_result.json
```

### Track Performance

Add to orchestrator:

```python
import time

start = time.time()
result = await orchestrator.process_task(task)
duration = time.time() - start

print(f"Total time: {duration:.2f}s")
print(f"Cost: ${duration * 0.0001:.4f}")  # Approximate
```

## Next Steps

1. **Explore Code**: Read through `agent_orchestrator.py`
2. **Customize**: Create your own task definitions
3. **Extend**: Add new agent types
4. **Deploy**: Push to GitHub and deploy
5. **Share**: Show it to Lyzr AI team!

## Getting Help

**Stuck?**
1. Check TROUBLESHOOTING section above
2. Review ARCHITECTURE.md for design details
3. Look at demo.py for usage examples
4. Check GitHub repo: https://github.com/open-gitagent/gitagent

**Issues with**:
- **Claude API**: https://support.anthropic.com
- **GitAgent**: https://github.com/open-gitagent/gitagent/issues
- **Next.js**: https://nextjs.org/docs

## Quick Reference

| Task | Command |
|------|---------|
| Run backend | `python agent_orchestrator.py` |
| Run demo | `python demo.py` |
| Start frontend | `npm run dev` |
| Build frontend | `npm run build` |
| Install packages | `pip install -r requirements.txt` |
| Check setup | `python -c "import anthropic; print('✓')"` |
| View logs | `tail -f generation_result.json` |
| Deploy | `npm run build && npm start` |

---

**Ready to ship?** Run `python agent_orchestrator.py` and watch it generate code! 🚀
