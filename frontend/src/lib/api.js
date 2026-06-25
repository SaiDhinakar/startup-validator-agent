const API_BASE = "/api/v1";
const SSE_BASE = "http://localhost:8000/api/v1";

export async function createStrategy({ idea, budget, teamSize, timeline }) {
  const res = await fetch(`${API_BASE}/strategies`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      idea,
      budget,
      team_size: teamSize,
      timeline,
      product_name: idea,
      product_type: "Startup",
      timeline_months: parseInt(timeline) || 3,
      target_users: "General users",
    }),
  });
  if (!res.ok) throw new Error(`Create failed: ${res.status}`);
  return res.json();
}

export function generateCTOStream(strategyId, callbacks) {
  const {
    onAgentStart,
    onAgentDone,
    onAgentResult,
    onToolStart,
    onToolDone,
    onReviewStart,
    onReviewDone,
    onAgentRetry,
    onAgentSkipped,
    onAgentsSelected,
    onDone,
    onError,
  } = callbacks;

  const ctrl = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${SSE_BASE}/strategies/${strategyId}/generate-cto`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
        signal: ctrl.signal,
      });

      if (!res.ok) throw new Error(`Generate failed: ${res.status}`);

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop();

        let eventType = "";
        for (const line of lines) {
          if (line.startsWith("event: ")) {
            eventType = line.slice(7).trim();
          } else if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(6));
            dispatchEvent(eventType, data);
            eventType = "";
          }
        }
      }

      if (buffer.trim()) {
        let eventType = "";
        for (const line of buffer.split("\n")) {
          if (line.startsWith("event: ")) eventType = line.slice(7).trim();
          else if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(6));
            dispatchEvent(eventType, data);
          }
        }
      }
    } catch (err) {
      if (err.name !== "AbortError") onError?.(err);
    }
  })();

  function dispatchEvent(type, data) {
    switch (type) {
      case "agent_start": onAgentStart?.(data.agent); break;
      case "agent_done": onAgentDone?.(data.agent); break;
      case "agent_result": onAgentResult?.(data.agent, data.output); break;
      case "tool_start": onToolStart?.(data.agent, data.tool, data.query); break;
      case "tool_done": onToolDone?.(data.agent, data.tool); break;
      case "review_start": onReviewStart?.(data.agent); break;
      case "review_done": onReviewDone?.(data.agent, data.valid, data.reason); break;
      case "agent_retry": onAgentRetry?.(data.agent, data.attempt, data.reason); break;
      case "agent_skipped": onAgentSkipped?.(data.agent, data.reason); break;
      case "agents_selected": onAgentsSelected?.(data.agents); break;
      case "done": onDone?.(data); break;
    }
  }

  return () => ctrl.abort();
}

export async function getStrategy(strategyId) {
  const res = await fetch(`${API_BASE}/strategies/${strategyId}`);
  if (!res.ok) throw new Error(`Get failed: ${res.status}`);
  return res.json();
}

export async function listStrategies(limit = 50) {
  const res = await fetch(`${API_BASE}/strategies?limit=${limit}`);
  if (!res.ok) throw new Error(`List failed: ${res.status}`);
  return res.json();
}

export async function deleteStrategy(strategyId) {
  const res = await fetch(`${API_BASE}/strategies/${strategyId}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
}
