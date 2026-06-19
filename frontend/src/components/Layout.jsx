import Sidebar from "./Sidebar";

export default function Layout({
  children,
  history,
  activeId,
  onSelect,
  onNewChat,
  onClear,
  onDelete,
}) {
  return (
    <div className="flex h-screen overflow-hidden bg-[var(--color-background)]">
      <Sidebar
        history={history}
        activeId={activeId}
        onSelect={onSelect}
        onNewChat={onNewChat}
        onClear={onClear}
        onDelete={onDelete}
      />
      <main className="flex-1 ml-72 overflow-y-auto">{children}</main>
    </div>
  );
}
