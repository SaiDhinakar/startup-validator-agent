"""Generate visual graphs of agent workflows.

Outputs mermaid diagrams to stdout and optionally writes an HTML viewer.

Usage:
    python scripts/generate_graphs.py              # print mermaid to stdout
    python scripts/generate_graphs.py --html       # write docs/graphs.html
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.planner.graph import build_planner_graph
from app.agents.feasibility.graph import build_feasibility_graph
from app.agents.market.graph import build_market_graph
from app.agents.growth.graph import build_growth_graph
from app.agents.hiring.graph import build_hiring_graph


AGENTS = {
    "Planner": build_planner_graph,
    "Feasibility": build_feasibility_graph,
    "Market": build_market_graph,
    "Growth": build_growth_graph,
    "Hiring": build_hiring_graph,
}

DESCRIPTIONS = {
    "Planner": "Analyzes requirements and orchestrates the agent workflow",
    "Feasibility": "Analyzes budget, timeline, and team feasibility",
    "Market": "Analyzes market opportunity and go-to-market strategy",
    "Growth": "Generates user acquisition and retention strategies",
    "Hiring": "Generates team structure and hiring plans",
    "Reviewer": "Validates agent outputs for ground truth accuracy",
    "Orchestrator": "Routes requests, manages state, coordinates all agents",
    "search_web": "External tool — web search for research",
}


def get_mermaid(graph_builder, name: str) -> str:
    compiled = graph_builder()
    try:
        return compiled.get_graph().draw_mermaid()
    except Exception:
        return _manual_mermaid(graph_builder, name)


def _manual_mermaid(graph_builder, name: str) -> str:
    compiled = graph_builder()
    graph = compiled.get_graph()
    lines = ["graph TD"]
    for node in graph.nodes:
        if node in ("__start__", "__end__"):
            continue
        lines.append(f"    {node}({node})")
    for edge in graph.edges:
        src = edge.source if hasattr(edge, "source") else edge[0]
        tgt = edge.target if hasattr(edge, "target") else edge[1]
        if src == "__start__":
            src = "START"
            lines.append(f"    START((START))")
        if tgt == "__end__":
            tgt = "END"
            lines.append(f"    END((END))")
        lines.append(f"    {src} --> {tgt}")
    return "\n".join(lines)


def build_agent_mapping_mermaid() -> str:
    """Build complete agent-to-agent mapping graph showing the full orchestration."""
    lines = [
        "graph TD",
        "",
        "    %% ── External Inputs ──",
        '    UserRequest[/"User Request<br/>(idea, budget, team, timeline)"/]',
        "",
        "    %% ── Core Components ──",
        '    Orchestrator["Orchestrator<br/>(router.py)"]',
        '    SharedState[["Shared State<br/>idea, budget, plan,<br/>feasibility_report,<br/>market_analysis,<br/>growth_strategy, hiring_plan"]]',
        "",
        "    %% ── Agents ──",
        '    Planner["Planner Agent<br/>(plan_node)"]',
        '    Feasibility["Feasibility Agent<br/>(feasibility_node)"]',
        '    Market["Market Agent<br/>(market_node)"]',
        '    Growth["Growth Agent<br/>(growth_node)"]',
        '    Hiring["Hiring Agent<br/>(hiring_node)"]',
        "",
        "    %% ── Reviewer ──",
        '    Reviewer["Reviewer Agent<br/>(review_agent_output)"]',
        "",
        "    %% ── Tools ──",
        '    SearchWeb{{"search_web<br/>(tool)"}}',
        "",
        "    %% ── Phase 1: Planner ──",
        "    UserRequest --> Orchestrator",
        "    Orchestrator -->|\"Phase 1: run planner\"| Planner",
        "    Planner -->|\"read inputs\"| SharedState",
        "    Planner --> SearchWeb",
        "    Planner -->|\"outputs plan + selected_agents\"| SharedState",
        "",
        "    %% ── Review Planner ──",
        "    Orchestrator -->|\"review output\"| Reviewer",
        "    Planner -.->|\"plan output\"| Reviewer",
        "    Reviewer -->|\"valid/invalid\"| Orchestrator",
        "",
        "    %% ── Retry loop ──",
        '    Reviewer -.->|"invalid → retry"| Planner',
        "",
        "    %% ── Phase 2: Downstream Agents ──",
        "    Orchestrator -->|\"Phase 2: run selected agents\"| Feasibility",
        "    Orchestrator -->|\"Phase 2: run selected agents\"| Market",
        "    Orchestrator -->|\"Phase 2: run selected agents\"| Growth",
        "    Orchestrator -->|\"Phase 2: run selected agents\"| Hiring",
        "",
        "    %% ── State reads ──",
        "    Feasibility -->|\"read idea, budget, team, timeline\"| SharedState",
        "    Market -->|\"read idea, budget, team\"| SharedState",
        "    Growth -->|\"read idea + market_analysis\"| SharedState",
        "    Hiring -->|\"read idea, budget, team\"| SharedState",
        "",
        "    %% ── Tool usage ──",
        "    Feasibility --> SearchWeb",
        "    Market --> SearchWeb",
        "    Growth --> SearchWeb",
        "    Hiring --> SearchWeb",
        "",
        "    %% ── State writes ──",
        "    Feasibility -->|\"write feasibility_report\"| SharedState",
        "    Market -->|\"write market_analysis\"| SharedState",
        "    Growth -->|\"write growth_strategy\"| SharedState",
        "    Hiring -->|\"write hiring_plan\"| SharedState",
        "",
        "    %% ── Review each downstream agent ──",
        "    Orchestrator -->|\"review feasibility\"| Reviewer",
        "    Orchestrator -->|\"review market\"| Reviewer",
        "    Orchestrator -->|\"review growth\"| Reviewer",
        "    Orchestrator -->|\"review hiring\"| Reviewer",
        "",
        "    Feasibility -.->|\"output\"| Reviewer",
        "    Market -.->|\"output\"| Reviewer",
        "    Growth -.->|\"output\"| Reviewer",
        "    Hiring -.->|\"output\"| Reviewer",
        "",
        "    Reviewer -.->|\"invalid → retry\"| Feasibility",
        "    Reviewer -.->|\"invalid → retry\"| Market",
        "    Reviewer -.->|\"invalid → retry\"| Growth",
        "    Reviewer -.->|\"invalid → retry\"| Hiring",
        "",
        "    %% ── Final output ──",
        "    Orchestrator -->|\"save to DB\"| SharedState",
        "    Orchestrator -->|\"stream done\"| UserRequest",
        "",
        "    %% ── Styles ──",
        "    classDef orchestrator fill:#4f46e5,stroke:#3730a3,color:#fff",
        "    classDef agent fill:#0ea5e9,stroke:#0284c7,color:#fff",
        "    classDef reviewer fill:#f59e0b,stroke:#d97706,color:#fff",
        "    classDef state fill:#10b981,stroke:#059669,color:#fff",
        "    classDef tool fill:#8b5cf6,stroke:#7c3aed,color:#fff",
        "    classDef input fill:#ec4899,stroke:#db2777,color:#fff",
        "",
        "    class Orchestrator orchestrator",
        "    class Planner,Feasibility,Market,Growth,Hiring agent",
        "    class Reviewer reviewer",
        "    class SharedState state",
        "    class SearchWeb tool",
        "    class UserRequest input",
    ]
    return "\n".join(lines)


def build_data_flow_mermaid() -> str:
    """Build a data-flow focused graph showing what each agent reads/writes."""
    lines = [
        "graph LR",
        "",
        "    %% ── Input ──",
        '    Input[/"User Input<br/>idea, budget,<br/>team_size, timeline"/]',
        "",
        "    %% ── Agents ──",
        '    P["Planner"]',
        '    F["Feasibility"]',
        '    M["Market"]',
        '    G["Growth"]',
        '    H["Hiring"]',
        '    R["Reviewer"]',
        "",
        "    %% ── State Keys ──",
        '    S_plan[("plan")]',
        '    S_selected[("selected_agents")]',
        '    S_feas[("feasibility_report")]',
        '    S_market[("market_analysis")]',
        '    S_growth[("growth_strategy")]',
        '    S_hire[("hiring_plan")]',
        "",
        "    %% ── Planner ──",
        "    Input --> P",
        "    P -->|writes| S_plan",
        "    P -->|writes| S_selected",
        "    P --> R",
        "",
        "    %% ── Feasibility ──",
        "    Input --> F",
        "    S_plan -.->|reads| F",
        "    F -->|writes| S_feas",
        "    F --> R",
        "",
        "    %% ── Market ──",
        "    Input --> M",
        "    S_plan -.->|reads| M",
        "    M -->|writes| S_market",
        "    M --> R",
        "",
        "    %% ── Growth (depends on Market) ──",
        "    Input --> G",
        "    S_market -.->|reads| G",
        "    S_plan -.->|reads| G",
        "    G -->|writes| S_growth",
        "    G --> R",
        "",
        "    %% ── Hiring ──",
        "    Input --> H",
        "    S_plan -.->|reads| H",
        "    H -->|writes| S_hire",
        "    H --> R",
        "",
        "    %% ── Retry ──",
        '    R -.->|"invalid → retry"| P',
        '    R -.->|"invalid → retry"| F',
        '    R -.->|"invalid → retry"| M',
        '    R -.->|"invalid → retry"| G',
        '    R -.->|"invalid → retry"| H',
        "",
        "    classDef agent fill:#0ea5e9,stroke:#0284c7,color:#fff",
        "    classDef reviewer fill:#f59e0b,stroke:#d97706,color:#fff",
        "    classDef state fill:#10b981,stroke:#059669,color:#fff",
        "    classDef input fill:#ec4899,stroke:#db2777,color:#fff",
        "",
        "    class P,F,M,G,H agent",
        "    class R reviewer",
        "    class S_plan,S_selected,S_feas,S_market,S_growth,S_hire state",
        "    class Input input",
    ]
    return "\n".join(lines)


def build_phase_mermaid() -> str:
    """Build a phase-by-phase execution flow."""
    lines = [
        "graph TD",
        "",
        '    Start(("START"))',
        "",
        "    %% ── Phase 0: Input ──",
        '    ParseInput["Parse user input<br/>(idea, budget, team, timeline)"]',
        "",
        "    %% ── Phase 1: Planning ──",
        '    RunPlanner["Run Planner Agent<br/>search_web → LLM → plan"]',
        '    ExtractSelected["Extract selected_agents<br/>from plan output"]',
        '    ReviewPlanner["Review Planner output<br/>(Reviewer agent)"]',
        '    PlannerValid{{"Planner valid?"}}',
        '    PlannerRetry["Retry Planner<br/>(max 2 attempts)"]',
        '    PlannerSkip["Skip Planner<br/>(use best-effort plan)"]',
        "",
        "    %% ── Phase 2: Parallel Agents ──",
        '    RunFeasibility["Run Feasibility Agent<br/>search_web → LLM → report"]',
        '    RunMarket["Run Market Agent<br/>search_web → LLM → analysis"]',
        '    RunGrowth["Run Growth Agent<br/>search_web → LLM → strategy"]',
        '    RunHiring["Run Hiring Agent<br/>search_web → LLM → plan"]',
        "",
        "    %% ── Phase 2: Review each ──",
        '    ReviewFeas["Review Feasibility"]',
        '    ReviewMkt["Review Market"]',
        '    ReviewGrow["Review Growth"]',
        '    ReviewHire["Review Hiring"]',
        "",
        '    FeasValid{{"valid?"}}',
        '    MktValid{{"valid?"}}',
        '    GrowValid{{"valid?"}}',
        '    HireValid{{"valid?"}}',
        "",
        "    %% ── Phase 3: Save ──",
        '    SaveDB["Save all results to DB"]',
        '    StreamDone["Stream done event"]',
        '    End(("END"))',
        "",
        "    %% ── Flow ──",
        "    Start --> ParseInput",
        "    ParseInput --> RunPlanner",
        "    RunPlanner --> ExtractSelected",
        "    ExtractSelected --> ReviewPlanner",
        "    ReviewPlanner --> PlannerValid",
        '    PlannerValid -->|"yes"| RunFeasibility',
        '    PlannerValid -->|"yes"| RunMarket',
        '    PlannerValid -->|"yes"| RunGrowth',
        '    PlannerValid -->|"yes"| RunHiring',
        '    PlannerValid -->|"no"| PlannerRetry',
        "    PlannerRetry --> ReviewPlanner",
        '    PlannerRetry -->|"max retries"| PlannerSkip',
        "    PlannerSkip --> RunFeasibility",
        "    PlannerSkip --> RunMarket",
        "    PlannerSkip --> RunGrowth",
        "    PlannerSkip --> RunHiring",
        "",
        "    RunFeasibility --> ReviewFeas",
        "    RunMarket --> ReviewMkt",
        "    RunGrowth --> ReviewGrow",
        "    RunHiring --> ReviewHire",
        "",
        "    ReviewFeas --> FeasValid",
        "    ReviewMkt --> MktValid",
        "    ReviewGrow --> GrowValid",
        "    ReviewHire --> HireValid",
        "",
        '    FeasValid -->|"yes"| SaveDB',
        '    MktValid -->|"yes"| SaveDB',
        '    GrowValid -->|"yes"| SaveDB',
        '    HireValid -->|"yes"| SaveDB',
        '    FeasValid -->|"no, retry"| RunFeasibility',
        '    MktValid -->|"no, retry"| RunMarket',
        '    GrowValid -->|"no, retry"| RunGrowth',
        '    HireValid -->|"no, retry"| RunHiring',
        "",
        "    SaveDB --> StreamDone",
        "    StreamDone --> End",
        "",
        "    classDef phase0 fill:#ec4899,stroke:#db2777,color:#fff",
        "    classDef phase1 fill:#4f46e5,stroke:#3730a3,color:#fff",
        "    classDef phase2 fill:#0ea5e9,stroke:#0284c7,color:#fff",
        "    classDef review fill:#f59e0b,stroke:#d97706,color:#fff",
        "    classDef phase3 fill:#10b981,stroke:#059669,color:#fff",
        "    classDef decision fill:#f97316,stroke:#ea580c,color:#fff",
        "",
        "    class ParseInput phase0",
        "    class RunPlanner,ExtractSelected,PlannerRetry,PlannerSkip phase1",
        "    class RunFeasibility,RunMarket,RunGrowth,RunHiring phase2",
        "    class ReviewPlanner,ReviewFeas,ReviewMkt,ReviewGrow,ReviewHire review",
        "    class PlannerValid,FeasValid,MktValid,GrowValid,HireValid decision",
        "    class SaveDB,StreamDone phase3",
    ]
    return "\n".join(lines)


def print_mermaid():
    print("## Agent Mapping — Complete System Overview")
    print("<!-- Shows how all agents connect, share state, and coordinate -->")
    print(build_agent_mapping_mermaid())
    print()

    print("## Data Flow — State Read/Write Map")
    print("<!-- What each agent reads from and writes to shared state -->")
    print(build_data_flow_mermaid())
    print()

    print("## Execution Phases — Step-by-Step Flow")
    print("<!-- The actual execution order with review/retry loops -->")
    print(build_phase_mermaid())
    print()

    for name, builder in AGENTS.items():
        print(f"## {name} Agent — Internal Graph")
        print(f"<!-- {DESCRIPTIONS[name]} -->")
        print(get_mermaid(builder, name))
        print()


def generate_html():
    diagrams = {
        "System Overview": {
            "mermaid": build_agent_mapping_mermaid(),
            "description": "Complete agent-to-agent mapping showing orchestration, state flow, tool usage, and review loops",
        },
        "Data Flow": {
            "mermaid": build_data_flow_mermaid(),
            "description": "What each agent reads from and writes to shared state",
        },
        "Execution Phases": {
            "mermaid": build_phase_mermaid(),
            "description": "Step-by-step execution order with review and retry logic",
        },
    }

    for name, builder in AGENTS.items():
        diagrams[name] = {
            "mermaid": get_mermaid(builder, name),
            "description": DESCRIPTIONS[name],
        }

    cards = ""
    for name, data in diagrams.items():
        cards += f"""
        <div class="card">
            <h2>{name}</h2>
            <p class="desc">{data["description"]}</p>
            <pre class="mermaid">{data["mermaid"]}</pre>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTO Agent — Agent Mapping</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Inter, system-ui, sans-serif; background: #f8fafc; color: #1e293b; padding: 2rem; }}
        h1 {{ text-align: center; margin-bottom: 0.5rem; font-size: 2rem; }}
        .subtitle {{ text-align: center; color: #64748b; margin-bottom: 2rem; }}
        .grid {{ display: grid; grid-template-columns: 1fr; gap: 1.5rem; max-width: 1400px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .card h2 {{ font-size: 1.25rem; margin-bottom: 0.25rem; }}
        .desc {{ color: #64748b; font-size: 0.875rem; margin-bottom: 1rem; }}
        .mermaid {{ display: flex; justify-content: center; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>AI Startup CTO Agent</h1>
    <p class="subtitle">Complete Agent Mapping &amp; Workflow</p>
    <div class="grid">{cards}
    </div>
    <script>mermaid.initialize({{ startOnLoad: true, theme: 'default', securityLevel: 'loose' }});</script>
</body>
</html>"""

    out_dir = Path(__file__).resolve().parent.parent / "docs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "graphs.html"
    out_path.write_text(html)
    print(f"Written to {out_path}")


if __name__ == "__main__":
    if "--html" in sys.argv:
        generate_html()
    else:
        print_mermaid()
