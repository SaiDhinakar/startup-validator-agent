import { Hero } from "../components/Hero";
import { HowItWorks } from "../components/HowItWorks";
import { FeatureGrid } from "../components/FeatureGrid";
import { InputForm } from "../components/InputForm";
import { Stats } from "../components/Stats";
import { Footer } from "../components/Footer";

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <Hero />
      <HowItWorks />
      <FeatureGrid />
      <InputForm />
      <Stats />
      <Footer />
    </div>
  );
}
