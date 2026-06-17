import { useState } from "react";
import { Send, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "../lib/utils";

export default function InputArea({ onSubmit, disabled }) {
  const [idea, setIdea] = useState("");
  const [showOptional, setShowOptional] = useState(false);
  const [budget, setBudget] = useState("$100K - $250K");
  const [teamSize, setTeamSize] = useState("4-6");
  const [timeline, setTimeline] = useState("3-4 months");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!idea.trim() || disabled) return;
    onSubmit({ idea: idea.trim(), budget, teamSize, timeline });
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit}>
        <div className="relative">
          <textarea
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder="Describe your startup idea..."
            disabled={disabled}
            rows={3}
            className={cn(
              "w-full px-4 py-3 pr-12 rounded-xl border border-[var(--color-border)]",
              "bg-white text-[var(--color-foreground)] placeholder:text-[var(--color-muted)]",
              "focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)] focus:ring-offset-1",
              "resize-none text-sm leading-relaxed",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
          />
          <button
            type="submit"
            disabled={!idea.trim() || disabled}
            className={cn(
              "absolute right-3 bottom-3 p-2 rounded-lg transition-colors",
              idea.trim() && !disabled
                ? "bg-[var(--color-accent)] text-white hover:bg-[#3f3f46]"
                : "bg-[#f4f4f5] text-[var(--color-muted)] cursor-not-allowed"
            )}
          >
            <Send size={16} />
          </button>
        </div>

        <button
          type="button"
          onClick={() => setShowOptional(!showOptional)}
          className="flex items-center gap-1 text-xs text-[var(--color-muted)] mt-2 hover:text-[var(--color-foreground)] transition-colors"
        >
          {showOptional ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          Optional details
        </button>

        {showOptional && (
          <div className="grid grid-cols-3 gap-3 mt-3">
            <div>
              <label className="block text-xs font-medium text-[var(--color-muted)] mb-1">
                Budget
              </label>
              <input
                type="text"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg border border-[var(--color-border)] text-sm bg-white focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-[var(--color-muted)] mb-1">
                Team Size
              </label>
              <input
                type="text"
                value={teamSize}
                onChange={(e) => setTeamSize(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg border border-[var(--color-border)] text-sm bg-white focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-[var(--color-muted)] mb-1">
                Timeline
              </label>
              <input
                type="text"
                value={timeline}
                onChange={(e) => setTimeline(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg border border-[var(--color-border)] text-sm bg-white focus:outline-none focus:ring-1 focus:ring-[var(--color-accent)]"
              />
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
