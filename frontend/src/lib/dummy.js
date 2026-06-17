const AGENT_RESPONSES = {
  planner: (idea) => `# Execution Plan

## Strategic Overview

Based on the idea: **"${idea}"**

### Domain Breakdown

| Domain | Priority | Estimated Weeks | Key Agents |
|--------|----------|-----------------|------------|
| Product & UX | High | 4 | Market Agent, Growth Agent |
| Technical Architecture | High | 5 | Growth Agent, Hiring Agent |
| Go-to-Market | Medium | 3 | Market Agent |
| Team Building | Medium | 2 | Hiring Agent |
| Review & Optimization | Medium | 1 | Feasibility Agent |

### Execution Order
1. Market Analysis & Validation
2. Architecture Design
3. MVP Development
4. Growth Strategy
5. Feasibility Review

### Timeline
- **Total Estimated Duration:** 15 weeks
- **Critical Path:** Product → Architecture → MVP → Review
- **Parallel Work:** Market research can run alongside architecture

### Key Risks
- Market timing — need to validate demand before full build
- Technical complexity may exceed initial estimates
- Team scaling could delay Phase 2

### Recommendations
- Start with a 2-week discovery sprint
- Build a landing page to gauge interest before development
- Hire a senior architect early to avoid costly pivots`,

  feasibility: (idea) => `# Feasibility Assessment

## Score: 7.5 / 10

### Executive Summary

The idea **"${idea}"** shows strong market potential with manageable technical risks. The concept addresses a real pain point and has a clear path to monetization.

### Market Feasibility
- **Market Size:** TAM estimated at $2.4B with 12% YoY growth
- **Target Audience:** Well-defined and accessible
- **Competitive Landscape:** Moderate — several incumbents but room for disruption
- **Timing:** Favorable — market shifting toward this solution

### Technical Feasibility
- **Complexity:** Medium — standard web/mobile stack required
- **Existing Solutions:** Can leverage proven technologies
- **Integration Needs:** APIs available for most required services
- **Scalability:** Cloud-native approach handles growth well

### Financial Feasibility
- **Initial Investment:** $150K-$250K for MVP
- **Runway Needed:** 8-12 months to reach break-even
- **Revenue Model:** SaaS with transaction fees — proven model
- **Unit Economics:** Favorable LTV/CAC ratio expected

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| User acquisition cost | High | Focus on organic/referral growth first |
| Technical debt | Medium | Enforce code review and testing standards |
| Regulatory changes | Low | Monitor compliance landscape |
| Team retention | Medium | Competitive equity packages |

### Recommendations
1. **Go** — Proceed with MVP development
2. Validate with 100 beta users before full launch
3. Keep burn rate low in first 6 months
4. Focus on one core feature, nail it before expanding

### Verdict: GO WITH CONDITIONS
Proceed with the following conditions:
- Complete market validation (2 weeks)
- Secure seed funding of at least $200K
- Hire a CTO/technical co-founder`,

  market: (idea) => `# Market Analysis

## Target Market: "${idea}"

### Market Overview
The market for this solution is experiencing significant growth, driven by increasing demand and technological advancement.

### Target Users

| Persona | Age | Need | Willingness to Pay |
|---------|-----|------|-------------------|
| Tech-savvy early adopters | 25-35 | Efficiency gains | High |
| Small business owners | 30-50 | Cost reduction | Medium |
| Enterprise teams | 28-45 | Scalability | Very High |
| Freelancers | 22-40 | Time savings | Medium |

### Core Features (MoSCoW)

**Must Have:**
- User authentication and profiles
- Core marketplace/transaction engine
- Real-time notifications
- Basic analytics dashboard

**Should Have:**
- Mobile app (React Native)
- Payment integration (Stripe)
- Automated matching algorithm
- Email marketing integration

**Could Have:**
- AI-powered recommendations
- Advanced reporting
- API for third-party integrations
- Multi-language support

**Won't Have (v1):**
- White-label solution
- Enterprise SSO
- Custom SLA agreements

### User Flows

1. **Onboarding Flow:** Sign up → Profile setup → Tutorial → First action
2. **Core Transaction Flow:** Browse → Select → Confirm → Pay → Complete
3. **Discovery Flow:** Search → Filter → View details → Compare → Choose

### Business Rules
- Users must verify email before transactions
- Minimum rating of 3.0 to remain active
- 14-day refund window for digital products
- Platform fee: 5% per transaction

### MVP Scope
- **In:** Core marketplace, payments, basic profiles, notifications
- **Out:** Mobile app, advanced analytics, API access
- **Estimated Effort:** 10 weeks with a team of 4`,

  growth: (idea) => `# Technical Architecture

## System Design for "${idea}"

### Architecture Overview

采用 Microservices architecture with event-driven communication between services.

### Core Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Next.js 14 + TypeScript | Web application |
| API Gateway | Kong / AWS API Gateway | Request routing, rate limiting |
| Auth Service | Node.js + JWT | Authentication & authorization |
| Core Service | Python FastAPI | Business logic |
| Payment Service | Node.js + Stripe SDK | Payment processing |
| Notification Service | Node.js + WebSocket | Real-time updates |
| Database | PostgreSQL | Primary data store |
| Cache | Redis | Session & query caching |
| Search | Elasticsearch | Full-text search |
| File Storage | AWS S3 | Media & document storage |
| Message Queue | RabbitMQ | Event-driven communication |

### Data Flow

\`\`\`
User Request → API Gateway → Auth Service → Core Service → Database
                                           ↓
                                    Message Queue → Notification Service
                                           ↓
                                    Payment Service → Stripe
\`\`\`

### Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Frontend | Next.js 14 | SSR, SEO, great DX |
| Backend | FastAPI | Async, type-safe, fast |
| Database | PostgreSQL | ACID, JSON support |
| Cache | Redis | Performance, pub/sub |
| Search | Elasticsearch | Full-text capabilities |
| Infrastructure | AWS ECS + RDS | Managed, scalable |
| CI/CD | GitHub Actions | Free for open source |
| Monitoring | Datadog | Comprehensive observability |

### Infrastructure Costs (Monthly)

- **Compute (ECS):** $800
- **Database (RDS):** $500
- **Cache (Elasticache):** $200
- **Search (OpenSearch):** $400
- **Storage (S3):** $50
- **CDN (CloudFront):** $100
- **Monitoring:** $200
- **Total:** ~$2,250/month

### Scalability Plan
- Horizontal scaling via ECS auto-scaling
- Database read replicas at 10K concurrent users
- Redis cluster for cache at 50K users
- CDN for static assets globally`,

  hiring: (idea) => `# Engineering Roadmap

## Development Plan for "${idea}"

### Database Schema

\`\`\`sql
-- Core tables
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE listings (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    buyer_id UUID REFERENCES users(id),
    seller_id UUID REFERENCES users(id),
    listing_id UUID REFERENCES listings(id),
    amount DECIMAL(10,2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
\`\`\`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | User registration |
| POST | /api/auth/login | User login |
| GET | /api/users/me | Get current user |
| GET | /api/listings | List all listings |
| POST | /api/listings | Create listing |
| GET | /api/listings/:id | Get listing details |
| POST | /api/transactions | Create transaction |
| GET | /api/transactions | List user transactions |
| POST | /api/payments/webhook | Stripe webhook |

### Sprint Roadmap

**Sprint 1 (Weeks 1-2): Foundation**
- Project setup, CI/CD pipeline
- Auth service implementation
- Database schema and migrations
- Basic frontend scaffolding

**Sprint 2 (Weeks 3-4): Core Features**
- Listings CRUD API
- Search functionality
- Frontend: listing pages
- Payment integration

**Sprint 3 (Weeks 5-6): Polish**
- Real-time notifications
- User profiles and dashboards
- Mobile responsive design
- Performance optimization

**Sprint 4 (Weeks 7-8): Launch Prep**
- End-to-end testing
- Security audit
- Documentation
- Beta deployment

### Hiring Plan

| Role | Priority | Timing | Monthly Cost |
|------|----------|--------|-------------|
| Senior Full-Stack Dev | Critical | Week 1 | $12,000 |
| Frontend Engineer | High | Week 2 | $10,000 |
| DevOps Engineer | High | Week 4 | $11,000 |
| QA Engineer | Medium | Week 6 | $8,000 |
| Product Manager | Medium | Week 8 | $10,000 |

### Technical Debt Budget
- 20% of each sprint allocated to tech debt
- Weekly code review sessions
- Monthly architecture review meetings`
};

const AGENT_ORDER = [
  { key: "planner", label: "Planner", icon: "ClipboardList" },
  { key: "feasibility", label: "Feasibility", icon: "SearchCheck" },
  { key: "market", label: "Market", icon: "BarChart3" },
  { key: "growth", label: "Growth", icon: "Rocket" },
  { key: "hiring", label: "Hiring", icon: "Users" },
];

const AGENT_DELAYS = [3000, 3500, 4000, 3500, 3000];

function generateReport(idea) {
  return AGENT_ORDER.map(
    (agent) => `\n\n---\n\n${AGENT_RESPONSES[agent.key](idea)}`
  ).join("");
}

function generateDummyStrategy(idea) {
  return {
    id: crypto.randomUUID(),
    idea,
    budget: "$100K - $250K",
    team_size: "4-6",
    timeline: "3-4 months",
    report: generateReport(idea),
    created_at: new Date().toISOString(),
  };
}

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem("cto_history") || "[]");
  } catch {
    return [];
  }
}

function saveToHistory(strategy) {
  const history = loadHistory();
  history.unshift(strategy);
  localStorage.setItem("cto_history", JSON.stringify(history));
}

function clearHistory() {
  localStorage.removeItem("cto_history");
}

function getStrategyById(id) {
  return loadHistory().find((s) => s.id === id) || null;
}

export {
  AGENT_ORDER,
  AGENT_DELAYS,
  AGENT_RESPONSES,
  generateReport,
  generateDummyStrategy,
  loadHistory,
  saveToHistory,
  clearHistory,
  getStrategyById,
};
