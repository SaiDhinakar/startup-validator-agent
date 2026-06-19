"""Mock LLM responses for each agent."""

PLANNER_RESPONSE = """<h1>Execution Plan</h1>
<h2>Strategic Overview</h2>
<p>Based on the idea: <strong>"Build an Uber clone for grocery delivery"</strong></p>
<h2>Domain Breakdown</h2>
<table><thead><tr><th>Domain</th><th>Priority</th><th>Estimated Weeks</th></tr></thead>
<tbody><tr><td>Product & UX</td><td>High</td><td>4</td></tr>
<tr><td>Technical Architecture</td><td>High</td><td>5</td></tr>
<tr><td>Go-to-Market</td><td>Medium</td><td>3</td></tr></tbody></table>"""

FEASIBILITY_RESPONSE = """<h1>Feasibility Review</h1>
<table><thead><tr><th>Dimension</th><th>Assessment</th></tr></thead>
<tbody><tr><td>Budget Feasibility</td><td>Moderate</td></tr>
<tr><td>Timeline Feasibility</td><td>High Risk</td></tr>
<tr><td>Team Feasibility</td><td>Low to Medium</td></tr></tbody></table>"""

MARKET_RESPONSE = """<h1>Market Analysis</h1>
<h2>Market Opportunity</h2>
<table><thead><tr><th>Metric</th><th>Value</th></tr></thead>
<tbody><tr><td>Urban population</td><td>~5M commuters</td></tr>
<tr><td>Ride-hail share</td><td>60% of passenger km</td></tr></tbody></table>"""

GROWTH_RESPONSE = """<h1>Growth Strategy</h1>
<h2>First 100 Users Strategy</h2>
<ul><li>Target early adopters</li><li>QR-cash onboarding</li></ul>
<h2>Acquisition Channels</h2>
<ul><li>Campus Ambassadors</li><li>Corporate Outreach</li></ul>"""

HIRING_RESPONSE = """<h1>Hiring Plan</h1>
<h2>Team Structure</h2>
<table><thead><tr><th>Role</th><th>Priority</th><th>Cost</th></tr></thead>
<tbody><tr><td>Full-Stack Developer</td><td>Critical</td><td>$8-12K/mo</td></tr>
<tr><td>React Native Dev</td><td>Critical</td><td>$6-10K/mo</td></tr></tbody></table>"""

REVIEWER_VALID = """VALID
REASON: Output is specific to the idea and contains plausible claims."""

REVIEWER_INVALID = """INVALID
REASON: Output contains fabricated statistics and generic advice not specific to this idea."""

MOCK_RESPONSES = {
    "planner": PLANNER_RESPONSE,
    "feasibility": FEASIBILITY_RESPONSE,
    "market": MARKET_RESPONSE,
    "growth": GROWTH_RESPONSE,
    "hiring": HIRING_RESPONSE,
    "reviewer_valid": REVIEWER_VALID,
    "reviewer_invalid": REVIEWER_INVALID,
}
