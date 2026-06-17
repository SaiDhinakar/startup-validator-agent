import { Plus, MessageSquare, Trash2 } from "lucide-react";
import { cn } from "../lib/utils";

export default function Sidebar({ history, activeId, onSelect, onNewChat, onClear }) {
  return (
    <aside className="w-72 h-screen bg-white border-r border-[var(--color-border)] flex flex-col fixed left-0 top-0 z-20">
      <div className="p-4 border-b border-[var(--color-border)]">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-lg font-semibold text-[var(--color-foreground)]">
            Startup CTO
          </h1>
          {history.length > 0 && (
            <button
              onClick={onClear}
              className="p-1.5 text-[var(--color-muted)] hover:text-[var(--color-destructive)] hover:bg-red-50 rounded-md transition-colors"
              title="Clear history"
            >
              <Trash2 size={16} />
            </button>
          )}
        </div>
        <button
          onClick={onNewChat}
          className={cn(
            "w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
            "bg-[var(--color-accent)] text-[var(--color-accent-foreground)] hover:bg-[#3f3f46]"
          )}
        >
          <Plus size={16} />
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {history.length === 0 ? (
          <div className="text-center text-[var(--color-muted)] text-sm mt-8 px-4">
            <MessageSquare size={32} className="mx-auto mb-2 opacity-40" />
            <p>No conversations yet</p>
            <p className="text-xs mt-1 opacity-60">Describe your startup idea to get started</p>
          </div>
        ) : (
          <div className="space-y-1">
            {history.map((item) => (
              <button
                key={item.id}
                onClick={() => onSelect(item.id)}
                className={cn(
                  "w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors",
                  activeId === item.id
                    ? "bg-[var(--color-accent)] text-[var(--color-accent-foreground)]"
                    : "text-[var(--color-foreground)] hover:bg-[#f4f4f5]"
                )}
              >
                <div className="truncate font-medium">{item.idea}</div>
                <div
                  className={cn(
                    "text-xs mt-0.5",
                    activeId === item.id ? "opacity-70" : "text-[var(--color-muted)]"
                  )}
                >
                  {new Date(item.created_at).toLocaleDateString()}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </aside>
  );
}
