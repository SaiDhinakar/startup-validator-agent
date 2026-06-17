import { useState, useCallback } from "react";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Chat from "./pages/Chat";
import {
  generateDummyStrategy,
  loadHistory,
  saveToHistory,
  clearHistory,
  getStrategyById,
} from "./lib/dummy";

function App() {
  const [history, setHistory] = useState(() => loadHistory());
  const [activeId, setActiveId] = useState(null);
  const [showChat, setShowChat] = useState(false);

  const activeStrategy = activeId ? getStrategyById(activeId) : null;

  const handleNewChat = useCallback(() => {
    setActiveId(null);
    setShowChat(true);
  }, []);

  const handleSelect = useCallback((id) => {
    setActiveId(id);
    setShowChat(true);
  }, []);

  const handleClear = useCallback(() => {
    clearHistory();
    setHistory([]);
    setActiveId(null);
    setShowChat(false);
  }, []);

  const handleSubmit = useCallback(
    (data) => {
      const strategy = generateDummyStrategy(data.idea);
      saveToHistory(strategy);
      setHistory(loadHistory());
      setActiveId(strategy.id);
    },
    []
  );

  return (
    <Layout
      history={history}
      activeId={activeId}
      onSelect={handleSelect}
      onNewChat={handleNewChat}
      onClear={handleClear}
    >
      {showChat ? (
        <Chat
          key={activeId || "new"}
          strategy={activeStrategy}
          onSubmit={handleSubmit}
        />
      ) : (
        <Home onNewChat={handleNewChat} />
      )}
    </Layout>
  );
}

export default App;
