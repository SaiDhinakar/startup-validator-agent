import { useState, useCallback, useRef, useEffect } from "react";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Chat from "./pages/Chat";
import { createStrategy, generateCTOStream, listStrategies, deleteStrategy } from "./lib/api";

const TOOL_LABELS = {
  search_web: "searching web",
  search_reddit: "searching Reddit",
  search_trends: "checking trends",
};

function App() {
  const [history, setHistory] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [showChat, setShowChat] = useState(false);
  const [agentStatus, setAgentStatus] = useState(null);
  const [selectedAgents, setSelectedAgents] = useState(null);
  const abortRef = useRef(null);

  useEffect(() => {
    listStrategies(50).then((res) => {
      setHistory((res.strategies || []).map((s) => ({
        ...s,
        agents: {
          planner: s.planner?.plan || "",
          feasibility: s.feasibility_report?.report || "",
          market: s.market_analysis?.analysis || "",
          growth: s.growth_strategy?.strategy || "",
          hiring: s.hiring_plan?.plan || "",
        },
      })));
    }).catch(() => { /* ignore */ });
  }, []);

  const activeStrategy = activeId
    ? history.find((s) => s.id === activeId) || null
    : null;

  const refreshHistory = useCallback(async () => {
    try {
      const res = await listStrategies(50);
      const strategies = (res.strategies || []).map((s) => ({
        ...s,
        agents: {
          planner: s.planner?.plan || "",
          feasibility: s.feasibility_report?.report || "",
          market: s.market_analysis?.analysis || "",
          growth: s.growth_strategy?.strategy || "",
          hiring: s.hiring_plan?.plan || "",
        },
      }));
      setHistory(strategies);
    } catch { /* ignore */ }
  }, []);

  const handleNewChat = useCallback(() => {
    setActiveId(null);
    setShowChat(true);
    setAgentStatus(null);
    setSelectedAgents(null);
  }, []);

  const handleSelect = useCallback((id) => {
    setActiveId(id);
    setShowChat(true);
    setAgentStatus(null);
    setSelectedAgents(null);
  }, []);

  const handleClear = useCallback(async () => {
    try {
      const res = await listStrategies(100);
      for (const s of res.strategies || []) {
        await deleteStrategy(s.id).catch(() => {});
      }
    } catch { /* ignore */ }
    setHistory([]);
    setActiveId(null);
    setShowChat(false);
    setAgentStatus(null);
    setSelectedAgents(null);
  }, []);

  const handleDelete = useCallback(async (id) => {
    await deleteStrategy(id).catch(() => {});
    setHistory((prev) => prev.filter((s) => s.id !== id));
    if (activeId === id) {
      setActiveId(null);
      setShowChat(false);
    }
  }, [activeId]);

  const handleSubmit = useCallback(
    async (data) => {
      setAgentStatus({});
      setSelectedAgents(null);

      try {
        const strategy = await createStrategy(data);
        setActiveId(strategy.id);
        await refreshHistory();

        abortRef.current = generateCTOStream(strategy.id, {
          onAgentsSelected: (agents) => {
            setSelectedAgents(agents);
          },
          onAgentStart: (agent) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "running", detail: "thinking..." },
            }));
          },
          onToolStart: (agent, tool) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "running", detail: TOOL_LABELS[tool] || `using ${tool}...` },
            }));
          },
          onToolDone: (agent) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "running", detail: "processing results..." },
            }));
          },
          onReviewStart: (agent) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "reviewing", detail: "validating output..." },
            }));
          },
          onReviewDone: (agent, valid) => {
            if (!valid) {
              setAgentStatus((prev) => ({
                ...prev,
                [agent]: { state: "running", detail: "retrying..." },
              }));
            }
          },
          onAgentRetry: (agent, attempt) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "retrying", detail: `attempt ${attempt}...` },
            }));
          },
          onAgentSkipped: (agent, reason) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "skipped", detail: reason },
            }));
          },
          onAgentDone: (agent) => {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: { state: "done", detail: "completed" },
            }));
          },
          onDone: async (data) => {
            const updated = {
              ...data,
              agents: {
                planner: data.planner?.plan || "",
                feasibility: data.feasibility_report?.report || "",
                market: data.market_analysis?.analysis || "",
                growth: data.growth_strategy?.strategy || "",
                hiring: data.hiring_plan?.plan || "",
              },
            };
            setHistory((prev) => prev.map((s) => (s.id === data.id ? { ...s, ...updated } : s)));
            setActiveId(data.id);
          },
          onError: (err) => {
            console.error("SSE error:", err);
            setAgentStatus(null);
          },
        });
      } catch (err) {
        console.error("API error:", err);
        setAgentStatus(null);
      }
    },
    [refreshHistory]
  );

  return (
    <Layout
      history={history}
      activeId={activeId}
      onSelect={handleSelect}
      onNewChat={handleNewChat}
      onClear={handleClear}
      onDelete={handleDelete}
    >
      {showChat ? (
        <Chat
          strategy={activeStrategy}
          agentStatus={agentStatus}
          selectedAgents={selectedAgents}
          onSubmit={handleSubmit}
        />
      ) : (
        <Home onNewChat={handleNewChat} />
      )}
    </Layout>
  );
}

export default App;
