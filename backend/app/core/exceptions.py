"""Custom exception hierarchy for agent failures."""


class AgentError(Exception):
    """Base exception for agent failures."""

    def __init__(self, message: str, agent: str = "unknown"):
        self.agent = agent
        super().__init__(f"[{agent}] {message}")


class LLMError(AgentError):
    """LLM call failed or returned invalid output."""


class ValidationError(AgentError):
    """Agent output failed schema validation."""
