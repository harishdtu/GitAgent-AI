"""
GitAgent Code Generation Orchestrator
Multi-agent system for autonomous code generation and GitHub integration
"""

import os
import json
import asyncio
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import subprocess
import tempfile
import shutil

# You'll need these installed: pip install anthropic gitpython requests
from anthropic import Anthropic
from git import Repo
import requests


@dataclass
class CodeGenerationTask:
    """Represents a code generation task"""
    project_name: str
    description: str
    tech_stack: str  # "python", "typescript", "fastapi", "nextjs"
    features: list[str]
    github_url: Optional[str] = None
    task_id: Optional[str] = None


@dataclass
class AgentResult:
    """Result from an agent"""
    agent_name: str
    status: str
    output: str
    timestamp: str


class CodeGenAgent:
    """Individual agent responsible for code generation"""
    
    def __init__(self, name: str, role: str, client: Anthropic):
        self.name = name
        self.role = role
        self.client = client
        self.conversation_history = []
    
    def analyze_requirements(self, task: CodeGenerationTask) -> str:
        """Agent analyzes requirements and creates plan"""
        prompt = f"""You are a Code Architecture Agent. Analyze this request and create a detailed plan.

Project: {task.project_name}
Description: {task.description}
Tech Stack: {task.tech_stack}
Features Needed: {', '.join(task.features)}

Provide:
1. Project structure/architecture
2. Key modules needed
3. Dependencies
4. Implementation order
5. Potential challenges

Be concise and actionable."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=1500,
            system=f"You are {self.role}. Provide clear, actionable technical guidance.",
            messages=self.conversation_history
        )
        
        result = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })
        
        return result
    
    def generate_code(self, task: CodeGenerationTask, architecture_plan: str) -> str:
        """Agent generates actual code"""
        prompt = f"""Based on this architecture plan, generate production-ready code.

Architecture:
{architecture_plan}

Project Details:
- Name: {task.project_name}
- Stack: {task.tech_stack}
- Features: {', '.join(task.features)}

Generate:
1. Core module implementation
2. API/entry point
3. Configuration
4. Basic tests

Use best practices. Make it production-ready."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=3000,
            system=f"You are {self.role}. Generate complete, working code.",
            messages=self.conversation_history
        )
        
        result = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })
        
        return result
    
    def review_code(self, code: str, task: CodeGenerationTask) -> str:
        """Agent reviews generated code for quality"""
        prompt = f"""Review this generated code for:
1. Security issues
2. Performance problems
3. Code quality
4. Missing error handling
5. Test coverage

Code:
{code[:2000]}...

Provide specific improvement suggestions."""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=1500,
            system=f"You are {self.role}. Provide critical but constructive code review.",
            messages=self.conversation_history
        )
        
        result = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })
        
        return result


class GitAgentOrchestrator:
    """Orchestrates multiple agents for complete code generation workflow"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.client = Anthropic()
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.agents = {
            "architect": CodeGenAgent(
                "ArchitectAgent",
                "Software architect expert at designing scalable systems",
                self.client
            ),
            "developer": CodeGenAgent(
                "DeveloperAgent",
                "Expert software developer who writes production code",
                self.client
            ),
            "reviewer": CodeGenAgent(
                "ReviewerAgent",
                "Code quality reviewer with security expertise",
                self.client
            )
        }
        self.results = []
    
    async def process_task(self, task: CodeGenerationTask) -> dict:
        """Main orchestration logic"""
        print(f"\n🚀 Starting code generation for: {task.project_name}")
        print("=" * 60)
        
        # Step 1: Architect analyzes requirements
        print("\n📋 [Architect] Analyzing requirements...")
        architecture = self.agents["architect"].analyze_requirements(task)
        self.results.append(AgentResult(
            agent_name="Architect",
            status="completed",
            output=architecture,
            timestamp=datetime.now().isoformat()
        ))
        print("✅ Architecture plan created")
        
        # Step 2: Developer generates code
        print("\n💻 [Developer] Generating code...")
        code = self.agents["developer"].generate_code(task, architecture)
        self.results.append(AgentResult(
            agent_name="Developer",
            status="completed",
            output=code,
            timestamp=datetime.now().isoformat()
        ))
        print("✅ Code generated")
        
        # Step 3: Reviewer reviews code
        print("\n🔍 [Reviewer] Reviewing code quality...")
        review = self.agents["reviewer"].review_code(code, task)
        self.results.append(AgentResult(
            agent_name="Reviewer",
            status="completed",
            output=review,
            timestamp=datetime.now().isoformat()
        ))
        print("✅ Code reviewed")
        
        # Step 4: Prepare for GitHub
        print("\n📦 Preparing artifacts...")
        
        return {
            "task": task.__dict__,
            "architecture": architecture,
            "generated_code": code,
            "code_review": review,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
    
    async def push_to_github(self, result: dict, repo_name: str) -> str:
        """Push generated code to GitHub"""
        if not self.github_token:
            print("⚠️  GitHub token not set. Skipping repository creation.")
            return "skipped"
        
        try:
            # Create temp directory
            temp_dir = tempfile.mkdtemp()
            
            # Initialize git repo
            repo = Repo.init(temp_dir)
            
            # Create project structure and files
            project_structure = {
                "README.md": self._generate_readme(result),
                "main.py": result.get("generated_code", "# Generated code"),
                "ARCHITECTURE.md": result.get("architecture", "# Architecture"),
                ".gitignore": "*.pyc\n__pycache__/\n.env\n.venv/"
            }
            
            for filename, content in project_structure.items():
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, "w") as f:
                    f.write(content)
            
            # Commit
            repo.index.add(["README.md", "main.py", "ARCHITECTURE.md", ".gitignore"])
            repo.index.commit("Initial commit: Auto-generated by GitAgent")
            
            print(f"✅ Local repository prepared at: {temp_dir}")
            return temp_dir
            
        except Exception as e:
            print(f"❌ GitHub integration error: {e}")
            return f"error: {str(e)}"
    
    def _generate_readme(self, result: dict) -> str:
        """Generate README for the project"""
        task = result["task"]
        return f"""# {task['project_name']}

{task['description']}

## Tech Stack
- {task['tech_stack']}

## Features
{chr(10).join(f"- {f}" for f in task['features'])}

## Architecture
See ARCHITECTURE.md for detailed design.

## Getting Started
1. Install dependencies
2. Configure environment
3. Run the application

## Generated By
GitAgent - Multi-agent code generation system

Generated at: {result['timestamp']}
"""
    
    def get_summary(self) -> dict:
        """Get summary of all agent work"""
        return {
            "total_agents": len(self.agents),
            "results": [
                {
                    "agent": r.agent_name,
                    "status": r.status,
                    "timestamp": r.timestamp,
                    "output_length": len(r.output)
                }
                for r in self.results
            ]
        }


async def main():
    """Demo: Generate a FastAPI microservice"""
    
    task = CodeGenerationTask(
        project_name="smart-api-builder",
        description="FastAPI microservice with intelligent endpoint generation",
        tech_stack="fastapi",
        features=[
            "Auto-generated REST endpoints",
            "Built-in validation",
            "OpenAPI documentation",
            "Error handling",
            "Rate limiting"
        ]
    )
    
    orchestrator = GitAgentOrchestrator()
    result = await orchestrator.process_task(task)
    
    # Push to GitHub
    print("\n📤 Pushing to GitHub...")
    repo_path = await orchestrator.push_to_github(result, "smart-api-builder")
    
    # Print summary
    print("\n" + "=" * 60)
    print("✨ GENERATION COMPLETE")
    print("=" * 60)
    summary = orchestrator.get_summary()
    print(f"Agents deployed: {summary['total_agents']}")
    for r in summary['results']:
        print(f"  • {r['agent']}: {r['status']} ({r['output_length']} chars)")
    
    # Save results
    output_file = "/mnt/user-data/outputs/generation_result.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n📄 Full results saved to: {output_file}")
    
    return result


if __name__ == "__main__":
    asyncio.run(main())
