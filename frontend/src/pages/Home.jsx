import { Lightbulb } from "lucide-react";

export default function Home({ onNewChat }) {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="text-center max-w-md px-4">
        <div className="w-16 h-16 bg-[#f4f4f5] rounded-2xl flex items-center justify-center mx-auto mb-6">
          <Lightbulb size={32} className="text-[var(--color-accent)]" />
        </div>
        <h2 className="text-2xl font-bold text-[var(--color-foreground)] mb-2">
          Startup CTO Agent
        </h2>
        <p className="text-[var(--color-muted)] mb-6 leading-relaxed">
          Describe your startup idea and get a comprehensive analysis including
          market research, technical architecture, and feasibility assessment.
        </p>
        <button
          onClick={onNewChat}
          className="px-6 py-2.5 bg-[var(--color-accent)] text-white rounded-lg font-medium hover:bg-[#3f3f46] transition-colors"
        >
          Get Started
        </button>
      </div>
    </div>
  );
}
