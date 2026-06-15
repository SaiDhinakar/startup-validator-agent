import { motion } from "framer-motion";
import { Lightbulb, Settings, Rocket } from "lucide-react";

const steps = [
  {
    icon: Lightbulb,
    title: "Describe Your Idea",
    description: "Tell us what you want to build — a marketplace, SaaS tool, mobile app, or anything else.",
    number: "01",
  },
  {
    icon: Settings,
    title: "Set Constraints",
    description: "Define your budget and team size so we can tailor the strategy to your reality.",
    number: "02",
  },
  {
    icon: Rocket,
    title: "Get Your Strategy",
    description: "Receive architecture diagrams, database schemas, API specs, sprint plans, and hiring roadmaps.",
    number: "03",
  },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.15 } },
};

const item = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
            How It Works
          </h2>
          <p className="mt-4 text-gray-500 text-lg">Three steps to your engineering blueprint</p>
        </motion.div>

        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8 relative"
        >
          {/* Connecting line */}
          <div className="hidden md:block absolute top-16 left-[20%] right-[20%] h-px bg-gradient-to-r from-indigo-200 via-indigo-300 to-indigo-200" />

          {steps.map((step) => (
            <motion.div
              key={step.number}
              variants={item}
              className="relative bg-white rounded-2xl p-8 border border-gray-100 shadow-sm hover:shadow-md transition-shadow duration-300"
            >
              <div className="w-14 h-14 bg-indigo-50 rounded-xl flex items-center justify-center mb-6">
                <step.icon className="w-7 h-7 text-indigo-600" />
              </div>
              <div className="text-xs font-bold text-indigo-400 tracking-widest mb-2">{step.number}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">{step.title}</h3>
              <p className="text-gray-500 leading-relaxed">{step.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
