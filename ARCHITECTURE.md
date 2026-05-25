# Architecture & Design Document

## System Overview

GitAgent Code Generation is a **multi-agent autonomous system** that generates production-ready code through orchestrated agent collaboration.

## Design Decisions

### 1. Why Multi-Agent?

**Problem**: Single LLM prompts are prone to:
- Scope creep (trying to do everything at once)
- Quality inconsistency (architecture + code + review in one pass)
- Hard to iterate/improve (monolithic prompt)

**Solution**: Decompose into specialized agents:
- Each agent has ONE responsibility
- Each agent can be tested independently
- Results are composable and verifiable
- Easy to add new agent types

### 2. Sequential vs Parallel Execution

**Current**: Sequential (Architect → Developer → Reviewer)

**Why Sequential?**
- Developer needs Architect's output
- Reviewer needs Developer's output
- Dependencies are explicit and clear

**Future Optimization**: 
- Architect and Infrastructure agents can run parallel
- Multiple Developers can iterate on same architecture
- Test agent runs alongside Review agent

### 3. Agent Design Pattern

Each agent follows this pattern:

```python
class Agent:
    - __init__: Initialize with role and context
    - conversation_history: Maintain state across calls
    - method_1: Specific task (analyze, generate, review)
    - Results: String output (compatible with next agent)
```

**Why this pattern?**
- Stateful conversation allows agents to reason about changes
- History enables agents to reference previous decisions
- String output is universal (easy to pass between agents)
- Extensible (easy to add new methods)

### 4. Agent Roles & Responsibilities

#### Architect Agent
**Role**: System Design & Planning  
**Input**: Requirements, tech stack, features  
**Output**: Architecture specification  
**Key Decisions**:
- Project structure
- Module organization
- Technology choices
- Dependency plan

**System Prompt**: "You are a software architect expert at designing scalable systems"

#### Developer Agent
**Role**: Code Implementation  
**Input**: Architecture from Architect  
**Output**: Production code  
**Key Decisions**:
- Actual implementation
- Design patterns
- Error handling
- Performance optimization

**System Prompt**: "You are an expert software developer who writes production code"

#### Reviewer Agent
**Role**: Quality Assurance  
**Input**: Code from Developer  
**Output**: Review feedback  
**Key Decisions**:
- Security issues
- Performance problems
- Code quality
- Missing features

**System Prompt**: "You are a code quality reviewer with security expertise"

## Data Structures

### CodeGenerationTask
```python
@dataclass
class CodeGenerationTask:
    project_name: str          # "smart-api-builder"
    description: str           # What does it do?
    tech_stack: str           # "fastapi", "nextjs", "python"
    features: list[str]       # Specific requirements
    github_url: Optional[str] # Where to push
    task_id: Optional[str]    # Unique identifier
```

### AgentResult
```python
@dataclass
class AgentResult:
    agent_name: str   # "Architect", "Developer", "Reviewer"
    status: str       # "completed", "failed", "in-progress"
    output: str       # The actual result
    timestamp: str    # ISO format timestamp
```

### Orchestrator Result
```python
{
    "task": CodeGenerationTask.__dict__,
    "architecture": str,           # From Architect
    "generated_code": str,         # From Developer
    "code_review": str,            # From Reviewer
    "timestamp": str,              # Completion time
    "status": "completed"
}
```

## Execution Flow

### Phase 1: Analysis
```
Orchestrator
  ↓
Architect Agent
  ├─ Input: Task definition
  ├─ Process: Analyze requirements
  ├─ Decision: Project structure
  └─ Output: Architecture plan
    ↓
  Store in: results[0]
```

**Claude API Call**:
- Model: claude-opus-4-20250514
- Max tokens: 1500
- System: Architecture role definition
- Messages: Complete conversation history

### Phase 2: Implementation
```
Architect Output
  ↓
Developer Agent
  ├─ Input: Architecture plan
  ├─ Process: Generate code
  ├─ Decision: Implementation details
  └─ Output: Working code
    ↓
  Store in: results[1]
```

**Claude API Call**:
- Model: claude-opus-4-20250514
- Max tokens: 3000 (longer output)
- System: Developer role definition
- Messages: Conversation history + architecture

### Phase 3: Review
```
Developer Output
  ↓
Reviewer Agent
  ├─ Input: Generated code
  ├─ Process: Quality review
  ├─ Decision: Improvement suggestions
  └─ Output: Review feedback
    ↓
  Store in: results[2]
```

**Claude API Call**:
- Model: claude-opus-4-20250514
- Max tokens: 1500
- System: Reviewer role definition
- Messages: Conversation history + code excerpt

### Phase 4: GitHub Integration
```
All Results
  ↓
GitHub Orchestrator
  ├─ Create directory structure
  ├─ Write files:
  │   ├─ Generated code
  │   ├─ Architecture docs
  │   ├─ README
  │   └─ .gitignore
  ├─ Initialize Git
  ├─ Commit changes
  └─ Push (optional, requires token)
```

## Conversation Management

Each agent maintains conversation history:

```python
agent.conversation_history = [
    {
        "role": "user",
        "content": "Analyze these requirements..."
    },
    {
        "role": "assistant",
        "content": "Architecture plan: ..."
    },
    {
        "role": "user",
        "content": "Now generate code based on..."
    },
    {
        "role": "assistant",
        "content": "def main(): ..."
    }
]
```

**Benefits**:
- Agents have context for follow-up questions
- System can ask for refinements
- History enables debugging
- Conversation state is transparent

## Error Handling

### At Agent Level
```python
try:
    response = client.messages.create(...)
    result = response.content[0].text
except Exception as e:
    agent_result = AgentResult(
        agent_name=agent.name,
        status="failed",
        output=f"Error: {str(e)}",
        timestamp=datetime.now().isoformat()
    )
```

### At Orchestrator Level
```python
async def process_task(task):
    for agent_name, agent in self.agents.items():
        try:
            result = agent.method(task)
            self.results.append(result)
        except Exception as e:
            # Log and stop on first failure
            # Or: skip and continue (resilience)
```

## Performance Characteristics

### Token Usage
- Architect: ~200-400 tokens in, ~500-1000 out = 700-1400 total
- Developer: ~300-600 tokens in, ~1500-2500 out = 1800-3100 total
- Reviewer: ~400-800 tokens in, ~500-1000 out = 900-1800 total
- **Total**: ~3400-6300 tokens per task

### Execution Time
- API latency: ~2-3 seconds per call
- Processing: ~0.5 seconds
- Network: ~0.5 seconds
- **Total**: ~4-6 seconds for complete generation

### Cost (at Claude pricing)
- Opus 4: $15/1M input, $75/1M output tokens
- Per task: ~$0.05-0.10 per generation

## Scalability Considerations

### Horizontal Scaling
```python
# Run multiple orchestrators in parallel
async def scale_generations(tasks: list[Task]):
    orchestrators = [GitAgentOrchestrator() for _ in range(4)]
    results = await asyncio.gather(
        *[orch.process_task(task) for orch, task in zip(orchestrators, tasks)]
    )
```

### Vertical Scaling
- Increase max_tokens for more detailed output
- Add more agent types (Test, DevOps, Docs agents)
- Implement agent feedback loops

### Storage & Caching
```python
# Cache architecture plans for similar tasks
cache = {
    "fastapi-microservice": cached_architecture,
    "nextjs-dashboard": cached_architecture,
}

# Reuse when task hash matches
if task.hash in cache:
    architecture = cache[task.hash]
else:
    architecture = architect.analyze(task)
    cache[task.hash] = architecture
```

## Testing Strategy

### Unit Tests
```python
def test_architect_agent():
    task = create_test_task()
    result = agent.analyze_requirements(task)
    assert "architecture" in result.lower()
    assert len(result) > 100
```

### Integration Tests
```python
async def test_full_pipeline():
    task = create_test_task()
    orchestrator = GitAgentOrchestrator()
    result = await orchestrator.process_task(task)
    
    assert result["status"] == "completed"
    assert len(result["generated_code"]) > 200
    assert len(result["code_review"]) > 100
```

### E2E Tests
```python
async def test_github_integration():
    result = await orchestrator.process_task(task)
    repo_path = await orchestrator.push_to_github(result, "test-repo")
    
    # Verify Git commits
    assert len(Repo(repo_path).commits()) == 1
```

## Future Enhancements

### Immediate (Next iteration)
1. **Feedback Loop** - Let reviewer feedback be sent to developer for refinement
2. **Parallel Agents** - Run independent agents concurrently
3. **Agent Memory** - Persist successful patterns across generations
4. **Metrics** - Track quality, speed, cost per generation

### Medium-term
1. **More Agents**:
   - Test Agent (generates test suites)
   - DevOps Agent (Docker, CI/CD configs)
   - Documentation Agent (auto-generates docs)
   - Database Agent (schema + migrations)

2. **Smart Routing** - Route tasks to most appropriate agents
3. **Learning** - Update agent prompts based on outcomes
4. **Human Loop** - Review + approve before GitHub push

### Long-term
1. **Multi-Repository Orchestration** - Coordinate across multiple repos
2. **Version Control** - Track architectural changes over time
3. **A/B Testing** - Compare different agent strategies
4. **Fine-tuned Models** - Custom models for specific domains

## Why This Design Wins

✅ **Separation of Concerns** - Each agent has one job  
✅ **Composable** - Results feed naturally into next stage  
✅ **Testable** - Each agent can be tested independently  
✅ **Scalable** - Easy to add agents, parallelize, optimize  
✅ **Transparent** - Full conversation history for debugging  
✅ **Fast** - Complete pipeline in 4-6 seconds  
✅ **Real Output** - Produces actual code, not just plans  

## Comparison: Other Approaches

### Monolithic Prompt
```
❌ Hard to debug
❌ Quality inconsistent  
❌ Can't reuse parts
❌ Scope creep
```

### Sequential Single Prompts
```
✓ Simple
✓ Works for basic tasks
❌ Can't reference previous output
❌ No state between calls
```

### Our Multi-Agent Approach
```
✓ Clear responsibilities
✓ Reusable components
✓ Stateful conversations
✓ Composable results
✓ Easy to extend
✓ Production-ready output
```

---

**TL;DR**: Each agent specializes in one task, maintains conversation history, and produces composable output. Simple, effective, and ships real code.
