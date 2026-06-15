import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { useCountUp } from "../hooks/useCountUp";

const stats = [
  { label: "Strategies Generated", value: 500, suffix: "+" },
  { label: "Budgets Planned", value: 2, prefix: "₹", suffix: "Cr+" },
  { label: "Startups Launched", value: 50, suffix: "+" },
];

function StatItem({ label, value, prefix = "", suffix = "" }: { label: string; value: number; prefix?: string; suffix?: string }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });
  const { count, start } = useCountUp(value, 2000);

  if (isInView) start();

  return (
    <div ref={ref} className="text-center">
      <div className="text-4xl md:text-5xl font-extrabold text-gray-900">
        {prefix}
        {count}
        {suffix}
      </div>
      <div className="mt-2 text-sm text-gray-500 font-medium">{label}</div>
    </div>
  );
}

export function Stats() {
  return (
    <section className="py-20 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-3 gap-8"
        >
          {stats.map((s) => (
            <StatItem key={s.label} {...s} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
