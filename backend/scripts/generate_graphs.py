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


def print_mermaid():
    for name, builder in AGENTS.items():
        print(f"## {name} Agent")
        print(f"<!-- {DESCRIPTIONS[name]} -->")
        print(get_mermaid(builder, name))
        print()


def generate_html():
    diagrams = {}
    for name, builder in AGENTS.items():
        diagrams[name] = {
            "mermaid": get_mermaid(builder, name),
            "description": DESCRIPTIONS[name],
        }

    cards = ""
    for name, data in diagrams.items():
        cards += f"""
        <div class="card">
            <h2>{name} Agent</h2>
            <p class="desc">{data["description"]}</p>
            <pre class="mermaid">{data["mermaid"]}</pre>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTO Agent — Workflow Graphs</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Inter, system-ui, sans-serif; background: #f8fafc; color: #1e293b; padding: 2rem; }}
        h1 {{ text-align: center; margin-bottom: 0.5rem; font-size: 2rem; }}
        .subtitle {{ text-align: center; color: #64748b; margin-bottom: 2rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 1.5rem; max-width: 1400px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .card h2 {{ font-size: 1.25rem; margin-bottom: 0.25rem; }}
        .desc {{ color: #64748b; font-size: 0.875rem; margin-bottom: 1rem; }}
        .mermaid {{ display: flex; justify-content: center; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>AI Startup CTO Agent</h1>
    <p class="subtitle">Agent Workflow Graphs</p>
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
