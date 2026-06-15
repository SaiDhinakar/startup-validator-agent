import { motion } from "framer-motion";
import {
  Database,
  Code2,
  Server,
  CalendarRange,
  Users,
  DollarSign,
} from "lucide-react";

const features = [
  {
    icon: Server,
    title: "Architecture Diagrams",
    description: "System design with service boundaries, data flow, and technology choices.",
  },
  {
    icon: Database,
    title: "Database Design",
    description: "Complete schema with tables, relationships, and indexing strategies.",
  },
  {
    icon: Code2,
    title: "API Specifications",
    description: "RESTful endpoints with methods, paths, and request/response contracts.",
  },
  {
    icon: DollarSign,
    title: "Infrastructure Estimates",
    description: "Cloud cost breakdown by service with monthly and annual projections.",
  },
  {
    icon: CalendarRange,
    title: "Sprint Plans",
    description: "Phased delivery roadmap with tasks, milestones, and time estimates.",
  },
  {
    icon: Users,
    title: "Hiring Plans",
    description: "Team composition recommendations with roles, priorities, and salary ranges.",
  },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

export function FeatureGrid() {
  return (
    <section className="py-24 px-6 bg-gray-50/50">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
            Everything You Need
          </h2>
          <p className="mt-4 text-gray-500 text-lg">
            A complete engineering strategy, generated in seconds
          </p>
        </motion.div>

        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features.map((f) => (
            <motion.div
              key={f.title}
              variants={item}
              whileHover={{ y: -4, boxShadow: "0 12px 40px rgba(0,0,0,0.08)" }}
              className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm cursor-default transition-all duration-300"
            >
              <div className="w-11 h-11 bg-indigo-50 rounded-xl flex items-center justify-center mb-4">
                <f.icon className="w-5 h-5 text-indigo-600" />
              </div>
              <h3 className="font-bold text-gray-900 mb-2">{f.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{f.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
