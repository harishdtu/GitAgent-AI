"""
GitAgent Code Generation Orchestrator
Multi-agent system for autonomous code generation and GitHub integration
Using Google Gemini AI
"""

import os
import json
import asyncio
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import tempfile

# Install:
# pip install google-genai gitpython requests
from google import genai
from git import Repo
import requests
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def extract_text(response):
    try:
        if hasattr(response, "text") and response.text:
            return response.text

        if hasattr(response, "candidates"):
            text_parts = []

            for part in response.candidates[0].content.parts:
                if hasattr(part, "text"):
                    text_parts.append(part.text)

            return "\n".join(text_parts)

        return str(response)

    except Exception as e:
        print(f"Extraction error: {e}")
        return str(response)


@dataclass
class CodeGenerationTask:
    """Represents a code generation task"""

    project_name: str
    description: str
    tech_stack: str
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

    def __init__(self, name: str, role: str, client):
        self.name = name
        self.role = role
        self.client = client
        self.conversation_history = []

    def analyze_requirements(self, task: CodeGenerationTask) -> str:
        """Agent analyzes requirements and creates plan"""

        prompt = f"""
You are a Code Architecture Agent.

Analyze this request and create a detailed plan.

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

Be concise and actionable.
"""

        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are {self.role}

{prompt}
"""
        )

        result = extract_text(response)

        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })

        return result

    def generate_code(
        self,
        task: CodeGenerationTask,
        architecture_plan: str
    ) -> str:
        """Agent generates actual code"""

        prompt = f"""
Based on this architecture plan, generate production-ready code.

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

Use best practices. Make it production-ready.
"""

        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are {self.role}

{prompt}
"""
        )

        result = extract_text(response)

        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })

        return result

    def review_code(
        self,
        code: str,
        task: CodeGenerationTask
    ) -> str:
        """Agent reviews generated code for quality"""

        prompt = f"""
Review this generated code for:
1. Security issues
2. Performance problems
3. Code quality
4. Missing error handling
5. Test coverage

Code:
{code[:2000]}...

Provide specific improvement suggestions.
"""

        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are {self.role}

{prompt}
""",
            config={
                "max_output_tokens": 4096,
                "temperature": 0.4
            }
        )

        result = extract_text(response)

        self.conversation_history.append({
            "role": "assistant",
            "content": result
        })

        return result


class GitAgentOrchestrator:
    """Orchestrates multiple agents for complete code generation workflow"""

    def __init__(self, github_token: Optional[str] = None):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set"
            )

        self.client = genai.Client(api_key=api_key)

        self.github_token = (
            github_token or os.getenv("GITHUB_TOKEN")
        )

        # Create agents
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

    async def process_task(
        self,
        task: CodeGenerationTask
    ) -> dict:
        """Main orchestration logic"""

        print(f"\n🚀 Starting code generation for: {task.project_name}")
        print("=" * 60)

        try:
            # Step 1: Architect
            print("\n📋 [Architect] Analyzing requirements...")

            architecture = self.agents[
                "architect"
            ].analyze_requirements(task)

            self.results.append(
                AgentResult(
                    agent_name="Architect",
                    status="completed",
                    output=architecture,
                    timestamp=datetime.now().isoformat()
                )
            )

            print("✅ Architecture plan created")
            print(
                f"   └─ Generated "
                f"{len(architecture)} characters"
            )

            # Step 2: Developer
            print("\n💻 [Developer] Generating code...")

            code = self.agents[
                "developer"
            ].generate_code(task, architecture)

            self.results.append(
                AgentResult(
                    agent_name="Developer",
                    status="completed",
                    output=code,
                    timestamp=datetime.now().isoformat()
                )
            )

            print("✅ Code generated")
            print(
                f"   └─ Generated "
                f"{len(code)} characters"
            )

            # Step 3: Reviewer
            print("\n🔍 [Reviewer] Reviewing code quality...")

            review = self.agents[
                "reviewer"
            ].review_code(code, task)

            self.results.append(
                AgentResult(
                    agent_name="Reviewer",
                    status="completed",
                    output=review,
                    timestamp=datetime.now().isoformat()
                )
            )

            print("✅ Code reviewed")
            print(
                f"   └─ Generated "
                f"{len(review)} characters"
            )

            # Final result
            return {
                "task": task.__dict__,
                "architecture": architecture,
                "generated_code": code,
                "review_report": review,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "model_used": "Gemini 2.5 Flash",

                "stats": {
                    "architecture_chars": len(architecture),
                    "code_chars": len(code),
                    "review_chars": len(review),
                    "total_chars": (
                        len(architecture)
                        + len(code)
                        + len(review)
                    )
                },

                "agents": {
                    "architect": {
                        "status": "completed",
                        "output_chars": len(architecture)
                    },
                    "developer": {
                        "status": "completed",
                        "output_chars": len(code)
                    },
                    "reviewer": {
                        "status": "completed",
                        "output_chars": len(review)
                    }
                }
            }

        except Exception as e:
            print(f"\n❌ Error during processing: {e}")

            import traceback
            traceback.print_exc()

            return {
                "task": task.__dict__,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "model_used": "Gemini 2.5 Flash"
            }

    async def push_to_github(
        self,
        result: dict,
        repo_name: str
    ) -> str:
        """Push generated code to GitHub"""

        if not self.github_token:
            print(
                "⚠️ GitHub token not set. "
                "Skipping repository creation."
            )
            return "skipped"

        try:
            temp_dir = tempfile.mkdtemp()

            # Initialize git repo
            repo = Repo.init(temp_dir)

            # Project files
            project_structure = {
                "README.md": self._generate_readme(result),
                "main.py": result.get(
                    "generated_code",
                    "# Generated code"
                ),
                "ARCHITECTURE.md": result.get(
                    "architecture",
                    "# Architecture"
                ),
                ".gitignore": (
                    "*.pyc\n"
                    "__pycache__/\n"
                    ".env\n"
                    ".venv/"
                )
            }

            for filename, content in project_structure.items():
                file_path = os.path.join(
                    temp_dir,
                    filename
                )

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

            # Git commit
            repo.index.add(list(project_structure.keys()))

            repo.index.commit(
                "Initial commit: "
                "Auto-generated by GitAgent using Gemini AI"
            )

            print(f"✅ Local repository prepared at: {temp_dir}")

            return temp_dir

        except Exception as e:
            print(f"❌ GitHub integration error: {e}")

            return f"error: {str(e)}"

    def _generate_readme(self, result: dict) -> str:
        """Generate README"""

        if "error" in result:
            return (
                "# Error in Generation\n\n"
                "Failed to generate code."
            )

        task = result["task"]

        features = "\n".join(
            [f"- {feature}" for feature in task["features"]]
        )

        return f"""# {task['project_name']}

{task['description']}

## Tech Stack
- {task['tech_stack']}

## Features
{features}

## Architecture
See ARCHITECTURE.md for detailed design.

## Getting Started

1. Install dependencies
2. Configure environment
3. Run the application

## Generated By
GitAgent - Multi-agent code generation system

Model: {result.get('model_used', 'Gemini AI')}

Generated at:
{result['timestamp']}
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
        description=(
            "FastAPI microservice with "
            "intelligent endpoint generation"
        ),
        tech_stack="fastapi",
        features=[
            "Auto-generated REST endpoints",
            "Built-in validation",
            "OpenAPI documentation",
            "Error handling",
            "Rate limiting"
        ]
    )

    try:
        orchestrator = GitAgentOrchestrator()

        result = await orchestrator.process_task(task)

        # Push to GitHub
        print("\n📤 Pushing to GitHub...")

        repo_path = await orchestrator.push_to_github(
            result,
            "smart-api-builder"
        )

        # Print summary
        print("\n" + "=" * 60)
        print("✨ GENERATION COMPLETE")
        print("=" * 60)

        summary = orchestrator.get_summary()

        print(f"Agents deployed: {summary['total_agents']}")

        for r in summary["results"]:
            print(
                f"  • {r['agent']}: "
                f"{r['status']} "
                f"({r['output_length']} chars)"
            )

        if "stats" in result:
            print("\n📊 Generation Stats:")

            print(
                f"  • Architecture: "
                f"{result['stats']['architecture_chars']} chars"
            )

            print(
                f"  • Generated Code: "
                f"{result['stats']['code_chars']} chars"
            )

            print(
                f"  • Code Review: "
                f"{result['stats']['review_chars']} chars"
            )

            print(
                f"  • Total Output: "
                f"{result['stats']['total_chars']} chars"
            )

        # Create output folder
        os.makedirs("public", exist_ok=True)

        # Save results
        output_file = "public/generation_result.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"\n📄 Full results saved to: {output_file}")

        print(f"\n📁 Repository Path: {repo_path}")

        return result

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")

        print("\nPlease set your API key:")

        print(
            "$env:GEMINI_API_KEY='your-api-key-here'"
        )

        print("\nGet your API key at:")
        print("https://ai.google.dev/")

        return None


if __name__ == "__main__":
    asyncio.run(main())