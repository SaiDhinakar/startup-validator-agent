import { motion, AnimatePresence } from "framer-motion";
import {
  ClipboardList,
  SearchCheck,
  BarChart3,
  Rocket,
  Users,
  Check,
  Loader2,
  AlertTriangle,
  XCircle,
  Search,
} from "lucide-react";
import { AGENT_ORDER } from "../lib/dummy";
import { cn } from "../lib/utils";

const ICONS = {
  ClipboardList,
  SearchCheck,
  BarChart3,
  Rocket,
  Users,
};

function getStatusInfo(status) {
  if (!status) return { label: "Waiting", color: "text-[var(--color-muted)]", icon: null };

  const s = typeof status === "string" ? status : status.state;
  const detail = typeof status === "object" ? status.detail : null;

  switch (s) {
    case "running":
      return { label: detail || "Working...", color: "text-[var(--color-foreground)]", icon: "spinner" };
    case "reviewing":
      return { label: detail || "Reviewing...", color: "text-amber-600", icon: "search" };
    case "retrying":
      return { label: detail || "Retrying...", color: "text-orange-500", icon: "retry" };
    case "skipped":
      return { label: detail || "Skipped", color: "text-red-500", icon: "skip" };
    case "done":
      return { label: "Completed", color: "text-green-700", icon: "check" };
    default:
      return { label: "Waiting", color: "text-[var(--color-muted)]", icon: null };
  }
}

export default function AgentProgress({ agentStatus, selectedAgents }) {
  if (!agentStatus || Object.keys(agentStatus).length === 0) return null;

  const visibleAgents = selectedAgents
    ? AGENT_ORDER.filter((a) => a.key === "planner" || selectedAgents.includes(a.key))
    : AGENT_ORDER;

  return (
    <div className="bg-white border border-[var(--color-border)] rounded-xl p-5 shadow-sm">
      <h3 className="text-sm font-semibold text-[var(--color-foreground)] mb-4">
        Agent Pipeline
      </h3>
      <div className="space-y-3">
        <AnimatePresence>
          {visibleAgents.map((agent, index) => {
            const status = agentStatus[agent.key];
            const statusInfo = getStatusInfo(status);
            const isDone = typeof status === "object" ? status?.state === "done" : status === "done";
            const isRunning = typeof status === "object"
              ? ["running", "reviewing", "retrying"].includes(status?.state)
              : status === "running";
            const isSkipped = typeof status === "object" ? status?.state === "skipped" : false;
            const isWaiting = !status;
            const Icon = ICONS[agent.icon];

            return (
              <motion.div
                key={agent.key}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-300",
                  isDone && "bg-green-50",
                  isRunning && "bg-[#f4f4f5] agent-pulse",
                  isSkipped && "bg-red-50",
                  isWaiting && "opacity-40"
                )}
              >
                <div
                  className={cn(
                    "w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0",
                    isDone && "bg-green-100 text-green-600",
                    isRunning && "bg-[var(--color-accent)] text-white",
                    isSkipped && "bg-red-100 text-red-500",
                    isWaiting && "bg-[#f4f4f5] text-[var(--color-muted)]"
                  )}
                >
                  {isDone ? (
                    <Check size={16} />
                  ) : isSkipped ? (
                    <XCircle size={16} />
                  ) : isRunning ? (
                    <Loader2 size={16} className="spinner" />
                  ) : (
                    <Icon size={16} />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div
                    className={cn(
                      "text-sm font-medium",
                      isDone && "text-green-700",
                      isRunning && "text-[var(--color-foreground)]",
                      isSkipped && "text-red-600",
                      isWaiting && "text-[var(--color-muted)]"
                    )}
                  >
                    {agent.label} Agent
                  </div>
                  <div className={cn("text-xs flex items-center gap-1", statusInfo.color)}>
                    {statusInfo.icon === "spinner" && <Loader2 size={10} className="spinner" />}
                    {statusInfo.icon === "search" && <Search size={10} />}
                    {statusInfo.icon === "skip" && <AlertTriangle size={10} />}
                    {statusInfo.label}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
}
