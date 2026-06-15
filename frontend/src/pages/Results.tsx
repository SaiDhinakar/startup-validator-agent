import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  Server,
  Database,
  Code2,
  DollarSign,
  CalendarRange,
  Users,
} from "lucide-react";
import { mockOutput } from "../data/dummy";

const tabs = [
  { id: "architecture", label: "Architecture", icon: Server },
  { id: "database", label: "Database", icon: Database },
  { id: "api", label: "API Specs", icon: Code2 },
  { id: "infrastructure", label: "Infrastructure", icon: DollarSign },
  { id: "sprints", label: "Sprint Plans", icon: CalendarRange },
  { id: "hiring", label: "Hiring", icon: Users },
];

type TabId = (typeof tabs)[number]["id"];

const typeColors: Record<string, string> = {
  frontend: "bg-blue-50 text-blue-700 border-blue-200",
  backend: "bg-emerald-50 text-emerald-700 border-emerald-200",
  database: "bg-amber-50 text-amber-700 border-amber-200",
  service: "bg-violet-50 text-violet-700 border-violet-200",
  external: "bg-gray-50 text-gray-600 border-gray-200",
};

const methodColors: Record<string, string> = {
  GET: "bg-emerald-50 text-emerald-700",
  POST: "bg-blue-50 text-blue-700",
  PATCH: "bg-amber-50 text-amber-700",
  PUT: "bg-orange-50 text-orange-700",
  DELETE: "bg-red-50 text-red-700",
};

const priorityColors: Record<string, string> = {
  critical: "bg-red-50 text-red-700",
  high: "bg-amber-50 text-amber-700",
  medium: "bg-gray-100 text-gray-600",
};

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = (location.state as { idea?: string; budget?: string; teamSize?: string }) || {};
  const [activeTab, setActiveTab] = useState<TabId>("architecture");

  const output = {
    ...mockOutput,
    idea: formData.idea || mockOutput.idea,
    budget: formData.budget || mockOutput.budget,
    teamSize: formData.teamSize || mockOutput.teamSize,
  };

  const totalInfraCost = output.infrastructure.items.reduce((sum, i) => sum + i.cost, 0);

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      {/* Header */}
      <div className="border-b border-gray-100 bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>
          <div className="text-center">
            <h1 className="text-sm font-semibold text-gray-900 truncate max-w-md">
              {output.idea}
            </h1>
            <p className="text-xs text-gray-400">
              {output.budget} · {output.teamSize} team members
            </p>
          </div>
          <div className="w-16" />
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Tab Bar */}
        <div className="flex gap-1 mb-8 overflow-x-auto pb-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all duration-200 ${
                activeTab === tab.id
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-200"
                  : "bg-white text-gray-500 hover:text-gray-700 hover:bg-gray-50 border border-gray-100"
              }`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.25 }}
          >
            {activeTab === "architecture" && <ArchitectureTab output={output} />}
            {activeTab === "database" && <DatabaseTab output={output} />}
            {activeTab === "api" && <ApiTab output={output} />}
            {activeTab === "infrastructure" && <InfrastructureTab output={output} totalCost={totalInfraCost} />}
            {activeTab === "sprints" && <SprintsTab output={output} />}
            {activeTab === "hiring" && <HiringTab output={output} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

function ArchitectureTab({ output }: { output: typeof mockOutput }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Architecture Diagram</h2>
        <p className="text-gray-500 mt-1">System components and data flow</p>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 p-8 shadow-sm">
        {/* Visual diagram */}
        <div className="flex flex-col items-center gap-4">
          {/* Frontend row */}
          <div className="flex gap-4 justify-center">
            {output.architecture.components
              .filter((c) => c.type === "frontend")
              .map((c) => (
                <motion.div
                  key={c.name}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.1 }}
                  className={`px-5 py-3 rounded-xl border text-sm font-medium ${typeColors[c.type]}`}
                >
                  {c.name}
                </motion.div>
              ))}
          </div>

          {/* Arrow */}
          <div className="text-gray-300 text-2xl">↓</div>

          {/* Services row */}
          <div className="flex gap-3 justify-center flex-wrap">
            {output.architecture.components
              .filter((c) => c.type === "service")
              .map((c, i) => (
                <motion.div
                  key={c.name}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 + i * 0.05 }}
                  className={`px-5 py-3 rounded-xl border text-sm font-medium ${typeColors[c.type]}`}
                >
                  {c.name}
                </motion.div>
              ))}
          </div>

          {/* Arrow */}
          <div className="text-gray-300 text-2xl">↓</div>

          {/* Data row */}
          <div className="flex gap-3 justify-center">
            {output.architecture.components
              .filter((c) => c.type === "database")
              .map((c) => (
                <motion.div
                  key={c.name}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4 }}
                  className={`px-5 py-3 rounded-xl border text-sm font-medium ${typeColors[c.type]}`}
                >
                  {c.name}
                </motion.div>
              ))}
            {output.architecture.components
              .filter((c) => c.type === "external")
              .map((c) => (
                <motion.div
                  key={c.name}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.45 }}
                  className={`px-5 py-3 rounded-xl border text-sm font-medium ${typeColors[c.type]}`}
                >
                  {c.name}
                </motion.div>
              ))}
          </div>
        </div>

        {/* Legend */}
        <div className="flex gap-4 mt-8 pt-6 border-t border-gray-100 justify-center flex-wrap">
          {Object.entries(typeColors).map(([type, cls]) => (
            <div key={type} className="flex items-center gap-2 text-xs text-gray-500">
              <span className={`w-3 h-3 rounded border ${cls}`} />
              {type}
            </div>
          ))}
        </div>
      </div>

      {/* Connections */}
      <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4">Data Flow</h3>
        <div className="space-y-2">
          {output.architecture.connections.map((c, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + i * 0.03 }}
              className="flex items-center gap-3 text-sm"
            >
              <span className="font-medium text-gray-700">{c.from}</span>
              <span className="text-gray-300">→</span>
              <span className="font-medium text-gray-700">{c.to}</span>
              <span className="text-xs text-gray-400 bg-gray-50 px-2 py-0.5 rounded">{c.label}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

function DatabaseTab({ output }: { output: typeof mockOutput }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Database Design</h2>
        <p className="text-gray-500 mt-1">PostgreSQL schema with {output.database.tables.length} tables</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {output.database.tables.map((table, i) => (
          <motion.div
            key={table.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden"
          >
            <div className="px-5 py-3 bg-gray-50 border-b border-gray-100">
              <span className="font-bold text-gray-900 font-mono">{table.name}</span>
            </div>
            <div className="p-4">
              {table.columns.map((col) => (
                <div
                  key={col}
                  className="py-1.5 text-sm text-gray-600 font-mono border-b border-gray-50 last:border-0"
                >
                  {col}
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function ApiTab({ output }: { output: typeof mockOutput }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">API Specifications</h2>
        <p className="text-gray-500 mt-1">{output.api.endpoints.length} RESTful endpoints</p>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        {output.api.endpoints.map((ep, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.04 }}
            className="flex items-center gap-4 px-5 py-3.5 border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors"
          >
            <span
              className={`text-xs font-bold px-2.5 py-1 rounded-lg min-w-[52px] text-center ${methodColors[ep.method] || "bg-gray-100 text-gray-600"}`}
            >
              {ep.method}
            </span>
            <code className="text-sm font-mono text-gray-800 flex-1">{ep.path}</code>
            <span className="text-sm text-gray-400 hidden sm:block">{ep.description}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function InfrastructureTab({ output, totalCost }: { output: typeof mockOutput; totalCost: number }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Infrastructure Estimates</h2>
        <p className="text-gray-500 mt-1">
          Monthly cost: <span className="font-semibold text-gray-700">₹{totalCost.toLocaleString("en-IN")}</span> · Annual:{" "}
          <span className="font-semibold text-gray-700">₹{(totalCost * 12).toLocaleString("en-IN")}</span>
        </p>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm space-y-4">
        {output.infrastructure.items.map((item, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-gray-700">{item.name}</span>
                <span className="text-xs text-gray-400">{item.provider}</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">₹{item.cost.toLocaleString("en-IN")}/mo</span>
            </div>
            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(item.cost / Math.max(...output.infrastructure.items.map((x) => x.cost))) * 100}%` }}
                transition={{ duration: 0.6, delay: 0.2 + i * 0.05 }}
                className="h-full bg-indigo-500 rounded-full"
              />
            </div>
          </motion.div>
        ))}
      </div>

      <div className="bg-indigo-50 rounded-2xl p-6 border border-indigo-100">
        <h3 className="font-semibold text-indigo-900 mb-2">Budget Utilization</h3>
        <p className="text-sm text-indigo-700">
          Infrastructure uses ~{Math.round((totalCost * 12) / 100000 * 10)}% of your annual budget. Consider reserved instances
          for 30-40% savings on AWS services.
        </p>
      </div>
    </div>
  );
}

function SprintsTab({ output }: { output: typeof mockOutput }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Sprint Plans</h2>
        <p className="text-gray-500 mt-1">
          {output.sprints.length} sprints · {output.sprints.length * 2} weeks total
        </p>
      </div>

      <div className="relative">
        {/* Timeline line */}
        <div className="absolute left-6 top-0 bottom-0 w-px bg-indigo-200" />

        <div className="space-y-6">
          {output.sprints.map((sprint, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="relative pl-16"
            >
              {/* Timeline dot */}
              <div className="absolute left-4 top-6 w-5 h-5 bg-indigo-600 rounded-full border-4 border-[#FAFAF9]" />

              <div className="bg-white rounded-2xl border border-gray-100 p-6 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-gray-900">{sprint.name}</h3>
                  <span className="text-xs text-gray-400 bg-gray-50 px-2.5 py-1 rounded-lg">{sprint.duration}</span>
                </div>
                <ul className="space-y-2">
                  {sprint.tasks.map((task, j) => (
                    <motion.li
                      key={j}
                      initial={{ opacity: 0, x: -5 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 + j * 0.03 }}
                      className="flex items-start gap-2 text-sm text-gray-600"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-indigo-300 mt-1.5 shrink-0" />
                      {task}
                    </motion.li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

function HiringTab({ output }: { output: typeof mockOutput }) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Hiring Plan</h2>
        <p className="text-gray-500 mt-1">
          {output.hiring.length} roles recommended for {output.teamSize}-person team
        </p>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        {output.hiring.map((role, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-gray-900">{role.role}</h3>
              <span
                className={`text-xs font-medium px-2.5 py-1 rounded-lg ${priorityColors[role.priority]}`}
              >
                {role.priority}
              </span>
            </div>
            <p className="text-sm text-gray-500 mb-3">{role.reason}</p>
            <div className="text-sm font-semibold text-gray-700">{role.cost}</div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
