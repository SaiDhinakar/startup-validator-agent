import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ClipboardList,
  SearchCheck,
  BarChart3,
  Rocket,
  Users,
  Check,
  Loader2,
} from "lucide-react";
import { AGENT_ORDER, AGENT_DELAYS } from "../lib/dummy";
import { cn } from "../lib/utils";

const ICONS = {
  ClipboardList,
  SearchCheck,
  BarChart3,
  Rocket,
  Users,
};

export default function AgentProgress({ isRunning, onComplete }) {
  const [completed, setCompleted] = useState([]);
  const [current, setCurrent] = useState(-1);

  useEffect(() => {
    if (!isRunning) {
      setCompleted([]);
      setCurrent(-1);
      return;
    }

    setCompleted([]);
    setCurrent(0);

    let timeouts = [];
    let cumulativeDelay = 0;

    AGENT_ORDER.forEach((agent, index) => {
      const startDelay = cumulativeDelay;
      const endDelay = cumulativeDelay + AGENT_DELAYS[index];

      timeouts.push(
        setTimeout(() => {
          setCurrent(index);
        }, startDelay)
      );

      timeouts.push(
        setTimeout(() => {
          setCompleted((prev) => [...prev, index]);
          if (index === AGENT_ORDER.length - 1) {
            setCurrent(-1);
            setTimeout(() => onComplete?.(), 500);
          }
        }, endDelay)
      );

      cumulativeDelay = endDelay;
    });

    return () => timeouts.forEach(clearTimeout);
  }, [isRunning]);

  if (!isRunning && completed.length === 0) return null;

  return (
    <div className="bg-white border border-[var(--color-border)] rounded-xl p-5 shadow-sm">
      <h3 className="text-sm font-semibold text-[var(--color-foreground)] mb-4">
        Agent Pipeline
      </h3>
      <div className="space-y-3">
        <AnimatePresence>
          {AGENT_ORDER.map((agent, index) => {
            const isDone = completed.includes(index);
            const isActive = current === index;
            const isWaiting = !isDone && !isActive;
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
                  isActive && "bg-[#f4f4f5] agent-pulse",
                  isWaiting && "opacity-40"
                )}
              >
                <div
                  className={cn(
                    "w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0",
                    isDone && "bg-green-100 text-green-600",
                    isActive && "bg-[var(--color-accent)] text-white",
                    isWaiting && "bg-[#f4f4f5] text-[var(--color-muted)]"
                  )}
                >
                  {isDone ? (
                    <Check size={16} />
                  ) : isActive ? (
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
                      isActive && "text-[var(--color-foreground)]",
                      isWaiting && "text-[var(--color-muted)]"
                    )}
                  >
                    {agent.label} Agent
                  </div>
                  <div className="text-xs text-[var(--color-muted)]">
                    {isDone
                      ? "Completed"
                      : isActive
                      ? "Working..."
                      : "Waiting"}
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
