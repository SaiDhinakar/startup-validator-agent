import { useState, useRef, useEffect } from "react";
import InputArea from "../components/InputArea";
import AgentProgress from "../components/AgentProgress";
import ReportView from "../components/ReportView";

export default function Chat({ strategy, onSubmit }) {
  const [isRunning, setIsRunning] = useState(false);
  const [showReport, setShowReport] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (strategy) {
      setShowReport(true);
      setIsRunning(false);
    }
  }, [strategy]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [showReport, isRunning]);

  const handleSubmit = (data) => {
    setIsRunning(true);
    setShowReport(false);
    onSubmit(data);
  };

  const handleAgentComplete = () => {
    setIsRunning(false);
    setShowReport(true);
  };

  return (
    <div className="flex h-full">
      {/* Left: Chat area */}
      <div className="flex-1 flex flex-col h-full overflow-y-auto">
        <div className="flex-1 p-6 md:p-8">
          {showReport && strategy ? (
            <ReportView report={strategy.report} idea={strategy.idea} />
          ) : isRunning ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="w-12 h-12 bg-[#f4f4f5] rounded-xl flex items-center justify-center mx-auto mb-4">
                  <div className="w-3 h-3 bg-[var(--color-accent)] rounded-full agent-pulse" />
                </div>
                <p className="text-sm text-[var(--color-muted)]">
                  Analyzing your idea...
                </p>
              </div>
            </div>
          ) : (
            <div className="flex items-end justify-center h-full pb-8">
              <InputArea onSubmit={handleSubmit} disabled={isRunning} />
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      </div>

      {/* Right: Agent progress */}
      <div className="w-80 border-l border-[var(--color-border)] bg-[var(--color-background)] p-4 overflow-y-auto flex-shrink-0">
        <AgentProgress isRunning={isRunning} onComplete={handleAgentComplete} />

        {!isRunning && !showReport && (
          <div className="mt-4 p-4 bg-white border border-[var(--color-border)] rounded-xl">
            <h3 className="text-sm font-semibold text-[var(--color-foreground)] mb-2">
              Agent Pipeline
            </h3>
            <p className="text-xs text-[var(--color-muted)] leading-relaxed">
              Your idea will be analyzed by 5 specialized agents:
            </p>
            <ul className="mt-2 space-y-1">
              {["Planner", "Feasibility", "Market", "Growth", "Hiring"].map(
                (name) => (
                  <li
                    key={name}
                    className="text-xs text-[var(--color-muted)] flex items-center gap-1.5"
                  >
                    <span className="w-1.5 h-1.5 bg-[#d4d4d8] rounded-full" />
                    {name}
                  </li>
                )
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
