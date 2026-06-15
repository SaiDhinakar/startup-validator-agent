"""Mock LLM responses for each agent — structured JSON payloads."""

PLANNER_RESPONSE = """
{
  "domains": [
    {"name": "Product & UX", "priority": "high", "agents": ["product"]},
    {"name": "System Design", "priority": "high", "agents": ["architecture"]},
    {"name": "Backend Engineering", "priority": "high", "agents": ["engineering"]},
    {"name": "Quality Review", "priority": "medium", "agents": ["reviewer"]}
  ],
  "execution_order": ["product", "architecture", "engineering", "reviewer"],
  "estimated_total_weeks": 12,
  "key_risks": ["budget tight for full team", "3-month timeline aggressive"]
}
"""

PRODUCT_RESPONSE = """
{
  "target_users": [
    {"persona": "Urban shopper", "need": "Quick grocery delivery within 30 mins"},
    {"persona": "Local store owner", "need": "Reach more customers digitally"}
  ],
  "core_features": [
    {"name": "User registration", "priority": "must", "effort": "2 days"},
    {"name": "Store browsing", "priority": "must", "effort": "3 days"},
    {"name": "Cart & checkout", "priority": "must", "effort": "5 days"},
    {"name": "Order tracking", "priority": "must", "effort": "4 days"},
    {"name": "Payment integration", "priority": "must", "effort": "3 days"},
    {"name": "Ratings & reviews", "priority": "should", "effort": "2 days"},
    {"name": "Push notifications", "priority": "should", "effort": "2 days"},
    {"name": "Admin dashboard", "priority": "could", "effort": "5 days"}
  ],
  "user_flows": [
    {"name": "Place order", "steps": ["Browse stores", "Add to cart", "Checkout", "Track delivery"]},
    {"name": "Store onboarding", "steps": ["Register store", "Add products", "Set delivery zone"]}
  ],
  "business_rules": [
    "Delivery radius max 10km",
    "Minimum order ₹200",
    "Commission 15% per order"
  ],
  "mvp_scope": {
    "in": ["User auth", "Store listing", "Cart", "Orders", "Payments", "Basic tracking"],
    "out": ["Loyalty program", "Multi-language", "AI recommendations"],
    "estimated_effort_weeks": 10
  }
}
"""

ARCHITECTURE_RESPONSE = """
{
  "components": [
    {"name": "React Native App", "type": "frontend", "tech": "React Native + TypeScript"},
    {"name": "Admin Dashboard", "type": "frontend", "tech": "React + Vite"},
    {"name": "API Gateway", "type": "service", "tech": "FastAPI"},
    {"name": "Auth Service", "type": "service", "tech": "FastAPI + JWT"},
    {"name": "Order Service", "type": "service", "tech": "FastAPI"},
    {"name": "Payment Service", "type": "service", "tech": "FastAPI + Stripe"},
    {"name": "PostgreSQL", "type": "database", "tech": "PostgreSQL 16"},
    {"name": "Redis", "type": "cache", "tech": "Redis 7"},
    {"name": "Stripe API", "type": "external", "tech": "REST"},
    {"name": "Firebase FCM", "type": "external", "tech": "REST"}
  ],
  "connections": [
    {"from": "React Native App", "to": "API Gateway", "protocol": "HTTPS"},
    {"from": "API Gateway", "to": "Auth Service", "protocol": "gRPC"},
    {"from": "API Gateway", "to": "Order Service", "protocol": "gRPC"},
    {"from": "Order Service", "to": "PostgreSQL", "protocol": "SQL"},
    {"from": "Order Service", "to": "Redis", "protocol": "TCP"}
  ],
  "tech_stack": [
    {"layer": "Mobile", "choice": "React Native", "reason": "Cross-platform, team knows React"},
    {"layer": "Backend", "choice": "FastAPI", "reason": "Async, auto-docs, Python ecosystem"},
    {"layer": "Database", "choice": "PostgreSQL", "reason": "ACID, JSONB for flexibility"},
    {"layer": "Cache", "choice": "Redis", "reason": "Session store, rate limiting"},
    {"layer": "Infra", "choice": "AWS ECS", "reason": "Cost-effective for 5-person team"}
  ],
  "infrastructure": {
    "compute": {"service": "AWS ECS Fargate", "monthly_cost": 8000},
    "database": {"service": "AWS RDS PostgreSQL", "monthly_cost": 4000},
    "cache": {"service": "AWS ElastiCache Redis", "monthly_cost": 2000},
    "storage": {"service": "AWS S3 + CloudFront", "monthly_cost": 1500},
    "monitoring": {"service": "Datadog", "monthly_cost": 3000},
    "total_monthly": 18500,
    "annual_estimate": 222000
  }
}
"""

ENGINEERING_RESPONSE = """
{
  "database": {
    "tables": [
      {"name": "users", "columns": ["id UUID PK", "name VARCHAR", "email VARCHAR UNIQUE", "phone VARCHAR", "role ENUM", "created_at TIMESTAMP"]},
      {"name": "stores", "columns": ["id UUID PK", "owner_id UUID FK", "name VARCHAR", "address TEXT", "is_active BOOLEAN"]},
      {"name": "products", "columns": ["id UUID PK", "store_id UUID FK", "name VARCHAR", "price DECIMAL", "stock INT"]},
      {"name": "orders", "columns": ["id UUID PK", "user_id UUID FK", "store_id UUID FK", "status ENUM", "total DECIMAL", "created_at TIMESTAMP"]},
      {"name": "order_items", "columns": ["id UUID PK", "order_id UUID FK", "product_id UUID FK", "quantity INT", "price DECIMAL"]}
    ],
    "indexes": ["users(email)", "orders(user_id, created_at)", "products(store_id)"]
  },
  "api": {
    "endpoints": [
      {"method": "POST", "path": "/auth/register", "description": "Register user"},
      {"method": "POST", "path": "/auth/login", "description": "Login, get JWT"},
      {"method": "GET", "path": "/stores", "description": "List nearby stores"},
      {"method": "GET", "path": "/stores/:id/products", "description": "Store products"},
      {"method": "POST", "path": "/orders", "description": "Create order"},
      {"method": "PATCH", "path": "/orders/:id/status", "description": "Update order status"},
      {"method": "POST", "path": "/payments/charge", "description": "Process payment"},
      {"method": "GET", "path": "/users/:id/orders", "description": "Order history"}
    ]
  },
  "sprints": [
    {
      "name": "Sprint 1 — Foundation",
      "duration": "2 weeks",
      "tasks": ["Monorepo setup", "CI/CD pipeline", "DB schema", "Auth service", "Basic mobile nav"]
    },
    {
      "name": "Sprint 2 — Core Flow",
      "duration": "2 weeks",
      "tasks": ["Store listing API", "Product catalog", "Cart system", "Order creation", "Push notifications"]
    },
    {
      "name": "Sprint 3 — Payments",
      "duration": "2 weeks",
      "tasks": ["Stripe integration", "Payment flow", "Order tracking", "Ratings", "Order history"]
    },
    {
      "name": "Sprint 4 — Polish",
      "duration": "2 weeks",
      "tasks": ["Admin dashboard", "Performance tuning", "Security audit", "App store submission"]
    }
  ],
  "hiring": [
    {"role": "Full-Stack Developer", "priority": "critical", "cost": "₹8-12 LPA", "timing": "Week 1"},
    {"role": "React Native Dev", "priority": "critical", "cost": "₹6-10 LPA", "timing": "Week 1"},
    {"role": "DevOps Engineer", "priority": "high", "cost": "₹8-12 LPA", "timing": "Week 3"}
  ]
}
"""

REVIEWER_RESPONSE = """
{
  "feasibility_score": 7,
  "feasibility_justification": "Viable with tight timeline. Core features achievable in 8 weeks. Risk in hiring speed.",
  "risks": [
    {"severity": "high", "description": "3-month timeline with 5-person team is aggressive", "mitigation": "Cut admin dashboard to post-MVP"},
    {"severity": "medium", "description": "Payment integration may have compliance delays", "mitigation": "Start Stripe onboarding in week 1"},
    {"severity": "low", "description": "React Native learning curve for team", "mitigation": "Pair programming, shared component library"}
  ],
  "recommendations": [
    "Prioritize mobile app over admin dashboard",
    "Use managed services (RDS, ECS) to reduce ops overhead",
    "Implement feature flags for incremental rollout",
    "Set up monitoring from day 1"
  ],
  "verdict": "go-with-changes",
  "verdict_explanation": "Project is feasible. Cut scope on admin dashboard, start payment onboarding early. Budget is tight but manageable with managed services."
}
"""

MOCK_RESPONSES = {
    "planner": PLANNER_RESPONSE,
    "product": PRODUCT_RESPONSE,
    "architecture": ARCHITECTURE_RESPONSE,
    "engineering": ENGINEERING_RESPONSE,
    "reviewer": REVIEWER_RESPONSE,
}
