"""Generate visual graphs of all agent workflows.

Outputs mermaid diagrams to stdout and optionally writes an HTML viewer.

Usage:
    python scripts/generate_graphs.py              # print mermaid to stdout
    python scripts/generate_graphs.py --html       # write docs/graphs.html
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.planner.graph import build_planner_graph
from app.agents.product.graph import build_product_graph
from app.agents.architecture.graph import build_architecture_graph
from app.agents.engineering.graph import build_engineering_graph
from app.agents.reviewer.graph import build_reviewer_graph


AGENTS = {
    "Planner": build_planner_graph,
    "Product": build_product_graph,
    "Architecture": build_architecture_graph,
    "Engineering": build_engineering_graph,
    "Reviewer": build_reviewer_graph,
}

DESCRIPTIONS = {
    "Planner": "Analyzes requirements and orchestrates the agent workflow",
    "Product": "Extracts business requirements and core features",
    "Architecture": "Designs technical stack and system components",
    "Engineering": "Generates DB schemas, APIs, and sprint roadmaps",
    "Reviewer": "Evaluates feasibility, scalability, and constraints",
}


def get_mermaid(graph_builder, name: str) -> str:
    """Extract mermaid syntax from a compiled LangGraph."""
    compiled = graph_builder()
    try:
        return compiled.get_graph().draw_mermaid()
    except Exception:
        # Fallback: manual mermaid generation
        return _manual_mermaid(graph_builder, name)


def _manual_mermaid(graph_builder, name: str) -> str:
    """Fallback mermaid generation from graph structure."""
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
    """Print mermaid diagrams for all agents."""
    for name, builder in AGENTS.items():
        print(f"## {name} Agent")
        print(f"<!-- {DESCRIPTIONS[name]} -->")
        print(get_mermaid(builder, name))
        print()


def generate_html():
    """Generate an HTML viewer with all agent graphs."""
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
