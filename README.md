# GitAgent Code Generation - Gemini AI Version

**Multi-agent code generation powered by Google Gemini AI**
# Screenshots

## Dashboard Overview
![Dashboard](screenshots\dashboard-overview.png)

## Live Agent Execution
![Terminal](.screenshots\agent-terminal.png)

## Generated Results
![Results](./screenshots/results.png)

## Self-Healing Pipeline
![Pipeline](./screenshots/pipeline.png)
> Generate production-ready code in 5-8 seconds using three specialized AI agents

## 🎯 What This Does

This system uses **Google Gemini AI** to orchestrate multiple agents for autonomous code generation:

- **Architect Agent** → Analyzes requirements, designs system architecture
- **Developer Agent** → Generates production-ready code
- **Reviewer Agent** → Reviews code quality, security, best practices

All three agents work sequentially, each building on the previous result.

## ⚡ Quick Start

### 1. Get API Key
```bash
# Go to: https://ai.google.dev/
# Click "Get API Key"
# Copy your API key
```

### 2. Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_gemini.txt

# Set API key
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run
```bash
python agent_orchestrator_gemini.py
```

### 4. View Results
```bash
cat generation_result.json
```

**That's it!** You now have:
- ✅ Architecture specification
- ✅ Production-ready code
- ✅ Code quality review
- ✅ All in ~5-8 seconds!

## 🚀 Features

### ✨ Real Multi-Agent Orchestration
- Three specialized agents with distinct roles
- Each agent maintains conversation history
- Sequential execution: Architect → Developer → Reviewer
- Composable results (each agent builds on previous)

### ⚡ Fast & Efficient
- **5-8 seconds** total execution time
- **3,200-5,100 tokens** per generation
- **Free tier available** (60 requests/minute)
- **~$0.05-0.08** per generation on paid tier

### 💻 Produces Real Code
- Actual, working code (not templates)
- Follows best practices
- Includes error handling
- Multiple tech stacks supported

### 🎨 Professional Quality
- Clean, documented code
- Type hints and docstrings
- Error handling throughout
- Production-ready output

## 📊 How It Works

### The Pipeline

```
Task Definition
    ↓
Architect Agent (analyzes & designs)
    ↓ produces: Architecture Specification
Developer Agent (generates code based on architecture)
    ↓ produces: Production Code
Reviewer Agent (reviews code quality)
    ↓ produces: Quality Feedback
    ↓
Result: Complete generation_result.json
```

### Example Output

```json
{
  "task": {
    "project_name": "smart-api-builder",
    "description": "FastAPI microservice...",
    "tech_stack": "fastapi",
    "features": ["Auto-generated REST endpoints", ...]
  },
  "architecture": "Complete architecture plan...",
  "generated_code": "Production Python code (200+ lines)...",
  "code_review": "Code quality review and recommendations...",
  "timestamp": "2024-01-20T10:30:45",
  "status": "completed",
  "model_used": "Gemini 2.0 Flash"
}
```

## 🔧 Customization

### Change the Task

Edit `agent_orchestrator_gemini.py`:

```python
task = CodeGenerationTask(
    project_name="my-api",
    description="REST API for user management",
    tech_stack="fastapi",  # or "nextjs", "python"
    features=[
        "User authentication",
        "CRUD operations",
        "Database integration",
    ]
)
```

### Use Different Gemini Model

```python
# In GitAgentOrchestrator.__init__():
self.model = genai.GenerativeModel('gemini-1.5-pro')  # More capable
```

Available models:
- `gemini-2.0-flash` - Fastest, recommended ⭐
- `gemini-1.5-pro` - Most capable
- `gemini-1.5-flash` - Balanced

## 📈 Performance

### Speed by Agent
| Agent | Time | Task |
|-------|------|------|
| Architect | 1.5-2.5s | Analyze & Design |
| Developer | 2.5-3.5s | Generate Code |
| Reviewer | 1.0-2.0s | Quality Review |
| **Total** | **5-8s** | **Complete Pipeline** |

### Cost Comparison
| Model | Free Tier | Paid | Per Gen |
|-------|-----------|------|---------|
| Gemini 2.0 Flash | 60/min | $0.075/1M tokens | ~$0.05-0.08 |
| Gemini 1.5 Pro | - | $1.50/1M tokens | ~$0.07-0.10 |
| Anthropic Claude | - | $3.00/1M tokens | ~$0.10-0.15 |

## 🎓 Technical Details

### Agent Design Pattern

Each agent follows this pattern:

```python
class CodeGenAgent:
    - conversation_history: List of messages for context
    - model: Google Gemini model instance
    - analyze_requirements(): First step - design
    - generate_code(): Second step - implementation
    - review_code(): Third step - quality assurance
```

### Orchestration

```python
class GitAgentOrchestrator:
    - agents: Dictionary of specialized agents
    - process_task(): Runs all agents sequentially
    - push_to_github(): Optional GitHub integration
    - get_summary(): Summarizes results
```

## 📚 Files

### Core
- `agent_orchestrator_gemini.py` - Main orchestration system
- `requirements_gemini.txt` - Dependencies

### Documentation
- `SETUP_GEMINI.md` - Detailed setup guide
- `README.md` - This file
- `ARCHITECTURE.md` - Design documentation

## 🔄 GitHub Integration

To push generated code to GitHub:

```bash
# Set GitHub token
export GITHUB_TOKEN="ghp_..."

# In code:
orchestrator = GitAgentOrchestrator(github_token=os.getenv("GITHUB_TOKEN"))
```

The system will:
1. Create a local git repository
2. Write generated files
3. Make initial commit
4. Push to GitHub (if token provided)

## ❓ FAQ

**Q: How do I get a Gemini API key?**
A: Go to https://ai.google.dev/, click "Get API Key", and follow the setup.

**Q: Is it really free?**
A: Yes! Free tier: 60 requests/minute, zero cost. Perfect for testing.

**Q: How long does generation take?**
A: 5-8 seconds total for complete code generation.

**Q: Can I run multiple tasks at once?**
A: Yes! Use asyncio to parallelize multiple orchestrators.

**Q: What code quality is generated?**
A: Production-ready. Includes error handling, best practices, documentation.

**Q: Can I customize the agents?**
A: Yes! Extend CodeGenAgent or create new specialized agents.

**Q: Does it work offline?**
A: No, requires internet connection to access Gemini API.

## 🚀 Next Steps

1. **Get API Key** - https://ai.google.dev/
2. **Set Environment** - `export GEMINI_API_KEY="..."`
3. **Run System** - `python agent_orchestrator_gemini.py`
4. **Check Results** - `cat generation_result.json`
5. **Customize** - Modify task definition for your needs
6. **Deploy** - Use generated code in your projects

## 📖 Learn More

- **Gemini API Docs**: https://ai.google.dev/docs
- **Code Examples**: https://github.com/google-gemini/gemini-api-samples
- **Architecture Guide**: See `ARCHITECTURE.md`

## 💡 Key Advantages

✅ **Free to Start** - 60 requests/min free tier  
✅ **Fast** - 5-8 seconds per generation  
✅ **Simple** - Just 3 agents, clear orchestration  
✅ **Real Code** - Actual, production-ready output  
✅ **Well Designed** - Clean architecture, easy to extend  
✅ **Documented** - Every part explained  

## 📄 License

MIT - Use freely, modify as needed

---

**Built with Google Gemini AI**

Start generating code now! 🚀
