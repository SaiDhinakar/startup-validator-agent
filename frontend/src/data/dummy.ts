export type GeneratedOutput = {
  idea: string;
  budget: string;
  teamSize: string;
  architecture: {
    components: { name: string; type: "frontend" | "backend" | "database" | "service" | "external" }[];
    connections: { from: string; to: string; label: string }[];
  };
  database: { tables: { name: string; columns: string[] }[] };
  api: { endpoints: { method: string; path: string; description: string }[] };
  infrastructure: { items: { name: string; cost: number; provider: string; category: string }[] };
  sprints: { name: string; tasks: string[]; duration: string }[];
  hiring: { role: string; priority: "critical" | "high" | "medium"; cost: string; reason: string }[];
};

export const mockOutput: GeneratedOutput = {
  idea: "Build Uber clone with ₹10 lakh budget",
  budget: "₹10,00,000",
  teamSize: "5",
  architecture: {
    components: [
      { name: "React Native App", type: "frontend" },
      { name: "Admin Dashboard", type: "frontend" },
      { name: "API Gateway", type: "service" },
      { name: "Auth Service", type: "service" },
      { name: "Ride Service", type: "service" },
      { name: "Payment Service", type: "service" },
      { name: "Notification Service", type: "service" },
      { name: "PostgreSQL", type: "database" },
      { name: "Redis Cache", type: "database" },
      { name: "Stripe API", type: "external" },
      { name: "Firebase FCM", type: "external" },
      { name: "Google Maps API", type: "external" },
    ],
    connections: [
      { from: "React Native App", to: "API Gateway", label: "REST/WebSocket" },
      { from: "Admin Dashboard", to: "API Gateway", label: "REST" },
      { from: "API Gateway", to: "Auth Service", label: "gRPC" },
      { from: "API Gateway", to: "Ride Service", label: "gRPC" },
      { from: "API Gateway", to: "Payment Service", label: "gRPC" },
      { from: "Ride Service", to: "PostgreSQL", label: "SQL" },
      { from: "Ride Service", to: "Redis Cache", label: "Cache" },
      { from: "Payment Service", to: "Stripe API", label: "HTTPS" },
      { from: "Notification Service", to: "Firebase FCM", label: "HTTPS" },
      { from: "Ride Service", to: "Google Maps API", label: "HTTPS" },
    ],
  },
  database: {
    tables: [
      {
        name: "users",
        columns: ["id (PK)", "name", "email", "phone", "role", "created_at"],
      },
      {
        name: "rides",
        columns: ["id (PK)", "rider_id (FK)", "driver_id (FK)", "status", "pickup", "dropoff", "fare", "created_at"],
      },
      {
        name: "drivers",
        columns: ["id (PK)", "user_id (FK)", "vehicle_type", "rating", "is_available", "current_lat", "current_lng"],
      },
      {
        name: "payments",
        columns: ["id (PK)", "ride_id (FK)", "amount", "method", "status", "stripe_id", "created_at"],
      },
      {
        name: "reviews",
        columns: ["id (PK)", "ride_id (FK)", "reviewer_id", "rating", "comment", "created_at"],
      },
    ],
  },
  api: {
    endpoints: [
      { method: "POST", path: "/auth/register", description: "Register new user" },
      { method: "POST", path: "/auth/login", description: "Login and receive JWT" },
      { method: "GET", path: "/rides/nearby", description: "Find nearby drivers" },
      { method: "POST", path: "/rides/request", description: "Request a new ride" },
      { method: "PATCH", path: "/rides/:id/accept", description: "Driver accepts ride" },
      { method: "PATCH", path: "/rides/:id/complete", description: "Complete ride" },
      { method: "POST", path: "/payments/charge", description: "Process payment" },
      { method: "GET", path: "/users/:id/history", description: "Ride history" },
      { method: "POST", path: "/reviews", description: "Submit ride review" },
      { method: "GET", path: "/drivers/:id/location", description: "Real-time driver location" },
    ],
  },
  infrastructure: {
    items: [
      { name: "AWS EC2 (t3.medium)", cost: 4800, provider: "AWS", category: "Compute" },
      { name: "AWS RDS PostgreSQL", cost: 3500, provider: "AWS", category: "Database" },
      { name: "AWS ElastiCache Redis", cost: 2000, provider: "AWS", category: "Cache" },
      { name: "AWS S3 + CloudFront", cost: 1200, provider: "AWS", category: "Storage/CDN" },
      { name: "Stripe Processing", cost: 2500, provider: "Stripe", category: "Payments" },
      { name: "Domain + SSL", cost: 1500, provider: "Cloudflare", category: "Networking" },
      { name: "Monitoring (Datadog)", cost: 3000, provider: "Datadog", category: "Observability" },
    ],
  },
  sprints: [
    {
      name: "Sprint 1 — Foundation",
      duration: "2 weeks",
      tasks: [
        "Setup monorepo with Turborepo",
        "Configure CI/CD pipeline",
        "Database schema + migrations",
        "Auth service (register/login/JWT)",
        "Basic React Native navigation",
      ],
    },
    {
      name: "Sprint 2 — Core Ride Flow",
      duration: "2 weeks",
      tasks: [
        "Ride request + matching algorithm",
        "Driver location tracking (WebSocket)",
        "Real-time map integration",
        "Ride status lifecycle",
        "Push notifications",
      ],
    },
    {
      name: "Sprint 3 — Payments & Reviews",
      duration: "2 weeks",
      tasks: [
        "Stripe integration",
        "Payment processing flow",
        "Ride fare calculation",
        "Review + rating system",
        "Ride history",
      ],
    },
    {
      name: "Sprint 4 — Polish & Launch",
      duration: "2 weeks",
      tasks: [
        "Admin dashboard",
        "Analytics basics",
        "Performance optimization",
        "Security audit",
        "App Store submission",
      ],
    },
  ],
  hiring: [
    { role: "Full-Stack Developer", priority: "critical", cost: "₹8-12 LPA", reason: "Core development — rides, payments, auth" },
    { role: "React Native Developer", priority: "critical", cost: "₹6-10 LPA", reason: "Mobile app is the primary product" },
    { role: "DevOps Engineer", priority: "high", cost: "₹8-12 LPA", reason: "CI/CD, AWS infrastructure, monitoring" },
    { role: "UI/UX Designer", priority: "high", cost: "₹4-7 LPA", reason: "Rider + driver experience design" },
    { role: "QA Engineer", priority: "medium", cost: "₹4-6 LPA", reason: "Automated testing, release quality" },
  ],
};
