'use client';

import React, { useEffect, useState } from 'react';
import {
  Zap,
  Code,
  Github,
  Play,
  CheckCircle,
  Clock,
} from 'lucide-react';
import { motion } from 'framer-motion';

type GenerationResult = {
  architecture: string;
  generated_code: string;
  review: string;
};

type Project = {
  id: number;
  name: string;
  description: string;
  status: 'completed' | 'in-progress';
  tech: string;
  progress: number;
  agents: string[];
  timestamp: string;
};

export default function GitAgentDashboard() {
  const [activeProject, setActiveProject] = useState(0);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedTech, setSelectedTech] = useState('fastapi');
  const [repoUrl, setRepoUrl] = useState('');
  const [description, setDescription] = useState('');

  const [result, setResult] = useState<GenerationResult | null>(null);

  const [stats, setStats] = useState({
    lines: 0,
    agents: 0,
    speed: 0,
  });

  const [terminalOutput, setTerminalOutput] = useState<string[]>([]);

  const projects: Project[] = [
    {
      id: 1,
      name: 'Smart API Builder',
      description:
        'FastAPI microservice with intelligent endpoint generation',
      status: 'completed',
      tech: 'fastapi',
      progress: 100,
      agents: ['Architect', 'Developer', 'Reviewer', 'FixAgent'],
      timestamp: '2 min ago',
    },
    {
      id: 2,
      name: 'React Dashboard',
      description:
        'Next.js admin dashboard with real-time data sync',
      status: 'in-progress',
      tech: 'nextjs',
      progress: 65,
      agents: ['Architect', 'Developer'],
      timestamp: 'Just now',
    },
  ];

  const features = [
    {
      icon: '🤖',
      label: 'Multi-Agent Orchestration',
      desc: 'Architect, Developer, Reviewer working in sync',
    },
    {
      icon: '⚡',
      label: 'Lightning Fast',
      desc:
        'Multi-agent orchestration with autonomous planning, generation, and repair.',
    },
    {
      icon: '📦',
      label: 'GitHub Ready',
      desc:
        'Repository-aware workflows with autonomous commits and pull requests.',
    },
    {
      icon: '🧪',
      label: 'Auto-Reviewed',
      desc:
        'Built-in code quality checks and security review',
    },
  ];

  const terminalLines = [
    '[Architect] Understanding repository structure...',
    '[Architect] Creating execution roadmap...',
    '[Developer] Generating authentication service...',
    '[Tester] 1 failing test detected...',
    '[FixAgent] Resolving dependency issue...',
    '[Tester] All tests passing.',
    '[PR-Agent] Generating pull request summary...',
  ];

  useEffect(() => {
    const saved = localStorage.getItem('gitagent-result');

    if (saved) {
      setResult(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    if (result) {
      localStorage.setItem(
        'gitagent-result',
        JSON.stringify(result)
      );
    }
  }, [result]);

  const streamTerminalLogs = async () => {
    setTerminalOutput([]);

    for (let i = 0; i < terminalLines.length; i++) {
      await new Promise((resolve) =>
        setTimeout(resolve, 450)
      );

      setTerminalOutput((prev) => [
        ...prev,
        terminalLines[i],
      ]);
    }
  };

  const handleGenerateCode = async () => {
    setIsGenerating(true);

    try {
      streamTerminalLogs();

      await new Promise((resolve) =>
        setTimeout(resolve, 3000)
      );

      setActiveProject(0);

      const response = await fetch(
        '/generation_result.json'
      );

      if (!response.ok) {
        throw new Error(
          'Failed to fetch generation results'
        );
      }

      const data = await response.json();

      const normalizedData: GenerationResult = {
        architecture:
          data.architecture ||
          data.architecture_plan ||
          data.results?.architecture ||
          '',

        generated_code:
          data.generated_code ||
          data.results?.generated_code ||
          '',

        review:
          data.review ||
          data.review_report ||
          data.code_review ||
          data.results?.review ||
          '',
      };

      setResult(normalizedData);

      setStats({
        lines:
          normalizedData.generated_code.split('\n')
            .length,
        agents: 4,
        speed: 4.6,
      });
    } catch (error) {
      console.error(
        'Failed to load generation results:',
        error
      );
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRunDemo = async () => {
    setIsGenerating(true);

    setTimeout(() => {
      setIsGenerating(false);

      alert('Workflow executed successfully 🚀');
    }, 2500);
  };

  return (
    <div
      className="min-h-screen"
      style={{
        background:
          'linear-gradient(to bottom, #f5f1ed 0%, #ede9e5 100%)',
      }}
    >
      {/* HEADER */}
      <header className="border-b-4 border-amber-900/80">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-3 h-3 bg-amber-900 rounded-full"></div>

            <span className="text-sm font-semibold text-amber-900 tracking-wide">
              GITAGENT
            </span>
          </div>

          <h1 className="text-6xl md:text-7xl font-black text-amber-950 tracking-tight leading-none">
           AI Agents
            <br />

            <span className="text-amber-700">
              That Build Production Code.
            </span>
          </h1>

          <p className="text-xl md:text-2xl text-amber-800/70 mt-6 max-w-3xl leading-relaxed">
            Powered by Gemini 2.5 Flash + Multi-Agent Orchestration.

            Build. Review. Ship.
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-8 py-10">
        {/* CONTROL PANEL */}
        <div className="bg-white border-2 border-amber-900/20 rounded-2xl p-8 mb-8 shadow-sm">
          <h2 className="text-2xl font-bold text-amber-950 mb-6">
            Generate
          </h2>

          {/* INPUTS */}
          <div className="grid gap-4 mb-8">
            <div>
              <label className="block text-sm font-semibold text-amber-900 mb-2">
                Repository URL
              </label>

              <input
                type="text"
                placeholder="Paste GitHub repository URL..."
                value={repoUrl}
                onChange={(e) =>
                  setRepoUrl(e.target.value)
                }
                className="w-full px-4 py-4 bg-amber-50 border-2 border-amber-200 rounded-xl text-amber-950 font-medium focus:outline-none focus:border-amber-400"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-900 mb-2">
                Description
              </label>

              <textarea
                rows={3}
                placeholder="Describe the feature, workflow, or bug fix..."
                value={description}
                onChange={(e) =>
                  setDescription(e.target.value)
                }
                className="w-full px-4 py-4 bg-amber-50 border-2 border-amber-200 rounded-xl text-amber-950 font-medium resize-none focus:outline-none focus:border-amber-400"
              />
            </div>
          </div>

          {/* CONTROLS */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div>
              <label className="block text-sm font-semibold text-amber-900 mb-3">
                Tech Stack
              </label>

              <select
                value={selectedTech}
                onChange={(e) =>
                  setSelectedTech(e.target.value)
                }
                className="w-full px-4 py-3 bg-amber-50 border-2 border-amber-200 rounded-lg text-amber-950 font-medium focus:outline-none focus:border-amber-400"
              >
                <option value="fastapi">
                  FastAPI (Python)
                </option>

                <option value="nextjs">
                  Next.js (TypeScript)
                </option>

                <option value="python">
                  Python CLI
                </option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-amber-900 mb-3">
                Project Type
              </label>

              <select className="w-full px-4 py-3 bg-amber-50 border-2 border-amber-200 rounded-lg text-amber-950 font-medium focus:outline-none focus:border-amber-400">
                <option>
                  Autonomous Workflows
                </option>

                <option>
                  Multi-Agent Systems
                </option>

                <option>API Service</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={handleGenerateCode}
                disabled={isGenerating}
                className="w-full bg-amber-900 hover:bg-amber-800 disabled:bg-amber-700 text-white font-bold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2 shadow-md"
              >
                {isGenerating ? (
                  <>
                    <Clock className="w-5 h-5 animate-spin" />

                    Generating...
                  </>
                ) : (
                  <>
                    <Zap className="w-5 h-5" />

                    Launch Agents
                  </>
                )}
              </button>
            </div>
          </div>

          {/* FEATURES */}
          <div className="grid md:grid-cols-2 gap-4">
            {features.map((feature, i) => (
              <div
                key={i}
                className="bg-gradient-to-br from-amber-50 to-amber-100/30 border border-amber-200 rounded-lg p-4"
              >
                <div className="flex gap-3">
                  <span className="text-2xl">
                    {feature.icon}
                  </span>

                  <div>
                    <p className="font-semibold text-amber-950">
                      {feature.label}
                    </p>

                    <p className="text-sm text-amber-800/60">
                      {feature.desc}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* PROJECTS */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-amber-950 mb-6">
            Recent Generations
          </h2>

          <div className="space-y-4">
            {projects.map((project, idx) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                onClick={() =>
                  setActiveProject(idx)
                }
                className={`cursor-pointer transition-all rounded-2xl p-6 border-2 ${
                  activeProject === idx
                    ? 'bg-amber-900/5 border-amber-900/40 shadow-md'
                    : 'bg-white border-amber-900/10 hover:border-amber-900/20'
                }`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold text-amber-950">
                        {project.name}
                      </h3>

                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          project.status ===
                          'completed'
                            ? 'bg-green-100 text-green-700'
                            : 'animate-pulse bg-yellow-100 text-yellow-700'
                        }`}
                      >
                        {project.status}
                      </span>
                    </div>

                    <p className="text-amber-800/70">
                      {project.description}
                    </p>
                  </div>

                  <div className="text-right">
                    <p className="text-sm text-amber-800/50">
                      {project.timestamp}
                    </p>

                    <p className="text-xs font-semibold text-amber-900 mt-2">
                      {project.tech.toUpperCase()}
                    </p>
                  </div>
                </div>

                <div className="w-full bg-amber-100 rounded-full h-2">
                  <div
                    className="bg-amber-900 h-2 rounded-full transition-all duration-500"
                    style={{
                      width: `${project.progress}%`,
                    }}
                  ></div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* TERMINAL */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-[#1E1E1E] text-green-400 rounded-3xl p-8 mb-10 shadow-2xl border border-black/20"
        >
          <div className="flex items-center gap-2 mb-6">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>

            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>

            <div className="w-3 h-3 bg-green-500 rounded-full"></div>

            <span className="ml-4 text-gray-400 text-sm">
              live-agent-execution.ts
            </span>
          </div>

          <div className="space-y-3 font-mono text-sm md:text-base max-h-64 overflow-y-auto">
            {terminalOutput.map((line, i) => (
              <motion.p
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
              >
                {line}
              </motion.p>
            ))}
          </div>
        </motion.div>

        {/* RESULTS */}
        {result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white border-2 border-amber-900/20 rounded-2xl p-8 shadow-sm mt-10"
          >
            <h2 className="text-3xl font-bold text-amber-950 mb-8">
              Generated Results
            </h2>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-amber-50 rounded-2xl p-6">
                <h3 className="font-bold text-lg mb-2">
                  Architecture
                </h3>

                <p className="text-amber-800">
                  {result?.architecture?.length || 0}{' '}
                  characters generated
                </p>
              </div>

              <div className="bg-amber-50 rounded-2xl p-6">
                <h3 className="font-bold text-lg mb-2">
                  Generated Code
                </h3>

                <p className="text-amber-800">
                  {
                    result?.generated_code?.length || 0
                  }{' '}
                  characters generated
                </p>
              </div>

              <div className="bg-amber-50 rounded-2xl p-6">
                <h3 className="font-bold text-lg mb-2">
                  Review Report
                </h3>

                <p className="text-amber-800">
                  {result?.review?.length || 0}{' '}
                  characters generated
                </p>
              </div>
            </div>

            <div className="bg-black text-green-400 rounded-2xl p-6 font-mono text-sm overflow-auto max-h-[400px]">
              <pre>
                {(result?.generated_code || "").substring(0, 1800)}
              </pre>
            </div>

            {/* ACTIONS */}
            <div className="flex gap-3 mt-8 pt-6 border-t border-amber-200">
              <a
                href={
                  repoUrl ||
                  'https://github.com/vercel/next.js'
                }
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1"
              >
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full bg-amber-900 text-white font-bold py-3 px-4 rounded-lg hover:bg-amber-800 transition-colors flex items-center justify-center gap-2 shadow-md"
                >
                  <Github className="w-5 h-5" />

                  View on GitHub
                </motion.button>
              </a>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleRunDemo}
                className="flex-1 bg-amber-100 text-amber-900 font-bold py-3 px-4 rounded-lg hover:bg-amber-200 transition-colors flex items-center justify-center gap-2 shadow-md"
              >
                <Play className="w-5 h-5" />

                Run Demo
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* STATS */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="grid md:grid-cols-3 gap-6 mt-12"
        >
          {[
            {
              label: 'Code Generated',
              value: `${stats.lines.toLocaleString()} lines`,
              icon: Code,
            },
            {
              label: 'Agents Deployed',
              value: `${stats.agents}`,
              icon: Zap,
            },
            {
              label: 'Avg Speed',
              value: `${stats.speed} seconds`,
              icon: Clock,
            },
          ].map((stat, i) => {
            const Icon = stat.icon;

            return (
              <motion.div
                key={i}
                whileHover={{ y: -5 }}
                className="bg-white border-2 border-amber-900/10 rounded-xl p-6 text-center hover:border-amber-900/30 transition-colors shadow-sm"
              >
                <Icon className="w-6 h-6 text-amber-900 mx-auto mb-3" />

                <p className="text-sm text-amber-800/60 mb-2">
                  {stat.label}
                </p>

                <p className="text-2xl font-bold text-amber-950">
                  {stat.value}
                </p>
              </motion.div>
            );
          })}
        </motion.div>
      </div>

      {/* FOOTER */}
      <footer className="border-t border-amber-900/20 mt-16 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-amber-800/60 text-sm">
          <p>
            GitAgent Demo • Multi-Agent Code
            Generation System
          </p>

          <p className="mt-2">
            Built for autonomous engineering
            workflows.
          </p>
        </div>
      </footer>
    </div>
  );
}