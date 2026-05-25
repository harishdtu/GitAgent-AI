# GitAgent with Google Gemini AI - Setup Guide

## Quick Start with Gemini AI

### 1. Get Your Gemini API Key

Go to: https://ai.google.dev/

- Click "Get API Key"
- Create a new API key in Google Cloud Console
- Copy your API key

### 2. Set Environment Variable

```bash
# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

### 3. Install Dependencies

```bash
pip install -r requirements_gemini.txt
```

Or install manually:
```bash
pip install google-generativeai gitpython requests
```

### 4. Run the System

```bash
python agent_orchestrator_gemini.py
```

### Expected Output

```
🚀 Starting code generation for: smart-api-builder
============================================================

📋 [Architect] Analyzing requirements...
✅ Architecture plan created

💻 [Developer] Generating code...
✅ Code generated

🔍 [Reviewer] Reviewing code quality...
✅ Code reviewed

📦 Preparing artifacts...

============================================================
✨ GENERATION COMPLETE
============================================================
Agents deployed: 3
  • Architect: completed (2847 chars)
  • Developer: completed (3521 chars)
  • Reviewer: completed (1892 chars)

📄 Full results saved to: generation_result.json
```

## Key Differences from Anthropic Version

### Gemini Advantages
✅ **Free Tier** - 60 requests/min free (vs Anthropic's paid)
✅ **No Credit Card** - Can use with just Google account
✅ **Fast** - Gemini 2.0 Flash is very quick
✅ **Good Quality** - Produces excellent code

### Setup Differences

| Feature | Anthropic | Gemini |
|---------|-----------|--------|
| API Key | sk-ant-... | From Google AI Console |
| Library | anthropic | google-generativeai |
| Model | claude-opus-4 | gemini-2.0-flash |
| Free Tier | No | Yes (60 req/min) |
| Setup Time | 2 min | 5 min |

## Troubleshooting

### Error: "GEMINI_API_KEY environment variable not set"

**Solution:**
```bash
# Check if key is set
echo $GEMINI_API_KEY

# If empty, set it again
export GEMINI_API_KEY="your-key"

# Verify
python -c "import os; print('API Key set:', len(os.getenv('GEMINI_API_KEY', '')) > 0)"
```

### Error: "API key invalid"

**Solution:**
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create NEW key (don't reuse old ones)
4. Copy the FULL key
5. Set environment variable again

### Error: "Rate limit exceeded"

**Solution:**
- Free tier: 60 requests/minute
- Wait a minute or upgrade to paid
- Use smaller tasks to stay under limit

### Error: "Model not found"

**Solution:**
Available models in Gemini:
- `gemini-2.0-flash` (recommended, fastest)
- `gemini-1.5-pro` (more capable, slower)
- `gemini-1.5-flash` (balanced)

Update in code if needed:
```python
self.model = genai.GenerativeModel('gemini-2.0-flash')
```

## Code Generation Details

### What Gets Generated

Running `python agent_orchestrator_gemini.py` produces:

```json
{
  "task": {
    "project_name": "smart-api-builder",
    "description": "...",
    "tech_stack": "fastapi",
    "features": [...]
  },
  "architecture": "Detailed architecture plan...",
  "generated_code": "Production Python code...",
  "code_review": "Quality review...",
  "timestamp": "2024-01-20T10:30:45",
  "status": "completed",
  "model_used": "Gemini 2.0 Flash"
}
```

### Customizing Tasks

Edit the `main()` function:

```python
task = CodeGenerationTask(
    project_name="your-project",
    description="What does it do?",
    tech_stack="fastapi",  # or "nextjs", "python"
    features=[
        "Feature 1",
        "Feature 2",
        "Feature 3",
    ]
)
```

## Performance Metrics

### Speed (Gemini 2.0 Flash)
- Architect Agent: 1.5-2.5 seconds
- Developer Agent: 2.5-3.5 seconds
- Reviewer Agent: 1.0-2.0 seconds
- **Total: 5-8 seconds**

### Tokens Used
- Input: ~1,200-1,600 tokens
- Output: ~2,000-3,500 tokens
- Total: ~3,200-5,100 tokens per task

### Cost
- **Free Tier**: $0.00 (up to 60 requests/min)
- **Paid**: ~$0.05-0.08 per generation

## Switching Between Models

To use different Gemini models:

```python
# In __init__ method:
self.model = genai.GenerativeModel('gemini-1.5-pro')  # More capable
self.model = genai.GenerativeModel('gemini-1.5-flash')  # Balanced
self.model = genai.GenerativeModel('gemini-2.0-flash')  # Fastest (default)
```

## Multiple Agents in Parallel

To run multiple generation tasks in parallel:

```python
import asyncio

async def run_multiple():
    tasks = [
        CodeGenerationTask(
            project_name=f"project-{i}",
            description="...",
            tech_stack="fastapi",
            features=[...]
        )
        for i in range(3)
    ]
    
    orchestrator = GitAgentOrchestrator()
    results = await asyncio.gather(
        *[orchestrator.process_task(task) for task in tasks]
    )
    
    return results

# Run
results = asyncio.run(run_multiple())
```

## Next Steps

1. ✅ Set GEMINI_API_KEY
2. ✅ Install requirements: `pip install -r requirements_gemini.txt`
3. ✅ Run: `python agent_orchestrator_gemini.py`
4. ✅ Check: `cat generation_result.json`
5. ✅ Customize the task for your needs
6. ✅ Integrate into your workflow

## Support & Resources

- **Get API Key**: https://ai.google.dev/
- **Gemini Documentation**: https://ai.google.dev/docs
- **Code Examples**: https://github.com/google-gemini/gemini-api-samples

---

That's it! You now have a production-ready multi-agent code generation system powered by Google Gemini AI! 🚀
