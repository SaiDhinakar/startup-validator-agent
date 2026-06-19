import { Plus, MessageSquare, Trash2, X } from "lucide-react";
import { cn } from "../lib/utils";

export default function Sidebar({ history, activeId, onSelect, onNewChat, onClear, onDelete }) {
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
              title="Clear all history"
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
              <div
                key={item.id}
                className={cn(
                  "group flex items-center gap-1 rounded-lg transition-colors",
                  activeId === item.id
                    ? "bg-[var(--color-accent)]"
                    : "hover:bg-[#f4f4f5]"
                )}
              >
                <button
                  onClick={() => onSelect(item.id)}
                  className="flex-1 text-left px-3 py-2.5 text-sm"
                >
                  <div
                    className={cn(
                      "truncate font-medium",
                      activeId === item.id
                        ? "text-[var(--color-accent-foreground)]"
                        : "text-[var(--color-foreground)]"
                    )}
                  >
                    {item.idea}
                  </div>
                  <div
                    className={cn(
                      "text-xs mt-0.5",
                      activeId === item.id ? "opacity-70 text-[var(--color-accent-foreground)]" : "text-[var(--color-muted)]"
                    )}
                  >
                    {new Date(item.created_at).toLocaleDateString()}
                  </div>
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete?.(item.id);
                  }}
                  className={cn(
                    "p-1.5 mr-1 rounded-md transition-colors flex-shrink-0",
                    "opacity-0 group-hover:opacity-100",
                    activeId === item.id
                      ? "text-[var(--color-accent-foreground)] hover:bg-white/20"
                      : "text-[var(--color-muted)] hover:text-[var(--color-destructive)] hover:bg-red-50"
                  )}
                  title="Delete chat"
                >
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </aside>
  );
}
