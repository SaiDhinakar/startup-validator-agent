import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Zap, Loader2 } from "lucide-react";

export function InputForm() {
  const navigate = useNavigate();
  const [idea, setIdea] = useState("");
  const [budget, setBudget] = useState("");
  const [teamSize, setTeamSize] = useState("5");
  const [loading, setLoading] = useState(false);

  const budgetOptions = [
    "₹5,00,000",
    "₹10,00,000",
    "₹25,00,000",
    "₹50,00,000",
    "₹1,00,00,000",
    "₹2,50,00,000",
    "₹5,00,00,000+",
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!idea.trim()) return;
    setLoading(true);
    setTimeout(() => {
      navigate("/results", { state: { idea, budget, teamSize } });
    }, 1200);
  };

  return (
    <section id="generate" className="py-24 px-6">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
            Generate Your Strategy
          </h2>
          <p className="mt-4 text-gray-500 text-lg">
            Fill in the details below and let AI build your engineering plan
          </p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
          onSubmit={handleSubmit}
          className="bg-white rounded-2xl p-8 border border-gray-100 shadow-lg shadow-gray-100/50 space-y-6"
        >
          {/* Product Idea */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Product Idea
            </label>
            <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Build an Uber clone for grocery delivery..."
              rows={3}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 transition-all duration-200 resize-none"
              required
            />
          </div>

          {/* Budget */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Budget
            </label>
            <select
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-gray-200 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 transition-all duration-200 bg-white"
              required
            >
              <option value="" disabled>
                Select your budget
              </option>
              {budgetOptions.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </div>

          {/* Team Size */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Team Size — <span className="text-indigo-600 font-bold">{teamSize} members</span>
            </label>
            <input
              type="range"
              min="1"
              max="20"
              value={teamSize}
              onChange={(e) => setTeamSize(e.target.value)}
              className="w-full h-2 bg-gray-100 rounded-full appearance-none cursor-pointer accent-indigo-600"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>1</span>
              <span>5</span>
              <span>10</span>
              <span>15</span>
              <span>20</span>
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading || !idea.trim()}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold py-4 rounded-xl transition-all duration-200 shadow-lg shadow-indigo-200 hover:shadow-xl hover:shadow-indigo-200 hover:-translate-y-0.5 disabled:translate-y-0 disabled:shadow-none disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating Strategy...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                Generate Strategy
              </>
            )}
          </button>
        </motion.form>
      </div>
    </section>
  );
}
