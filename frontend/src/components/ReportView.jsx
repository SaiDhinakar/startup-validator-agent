import { useRef, useState } from "react";
import { Download, ClipboardList, SearchCheck, BarChart3, Rocket, Users } from "lucide-react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { cn } from "../lib/utils";

const ICON_MAP = {
  planner: ClipboardList,
  feasibility: SearchCheck,
  market: BarChart3,
  growth: Rocket,
  hiring: Users,
};

const LABEL_MAP = {
  planner: "Plan",
  feasibility: "Feasibility",
  market: "Market",
  growth: "Growth",
  hiring: "Hiring",
};

function HtmlContent({ content }) {
  if (!content) return <p className="text-[var(--color-muted)] italic">No data available.</p>;

  return (
    <div
      className="report-content"
      dangerouslySetInnerHTML={{ __html: content }}
    />
  );
}

export default function ReportView({ agents, idea, selectedAgents, productType, timelineMonths, targetUsers }) {
  const reportRef = useRef(null);

  const availableTabs = selectedAgents
    ? ["planner", ...selectedAgents.filter((a) => a !== "planner")]
    : ["planner", "feasibility", "market", "growth", "hiring"];

  const tabsWithContent = availableTabs.filter((key) => agents?.[key]);
  const [activeTab, setActiveTab] = useState(() => tabsWithContent[0] || "planner");

  const handleDownload = async () => {
    if (!reportRef.current) return;
    const canvas = await html2canvas(reportRef.current, {
      scale: 2,
      useCORS: true,
      backgroundColor: "#ffffff",
    });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();
    const imgWidth = pdfWidth - 20;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    let heightLeft = imgHeight;
    let position = 10;
    pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
    heightLeft -= pdfHeight - 20;
    while (heightLeft > 0) {
      position = heightLeft - imgHeight + 10;
      pdf.addPage();
      pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
      heightLeft -= pdfHeight - 20;
    }
    pdf.save(`startup-report-${Date.now()}.pdf`);
  };

  const currentContent = agents?.[activeTab] || "";

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold text-[var(--color-foreground)]">
            Startup CTO Report
          </h2>
          <p className="text-xs text-[var(--color-muted)] mt-0.5">{idea}</p>
          {(productType || timelineMonths || targetUsers) && (
            <div className="flex items-center gap-3 mt-1.5">
              {productType && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#f4f4f5] text-[var(--color-muted)] font-medium">
                  {productType}
                </span>
              )}
              {timelineMonths > 0 && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#f4f4f5] text-[var(--color-muted)] font-medium">
                  {timelineMonths} months
                </span>
              )}
              {targetUsers && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#f4f4f5] text-[var(--color-muted)] font-medium">
                  {targetUsers}
                </span>
              )}
            </div>
          )}
        </div>
        <button
          onClick={handleDownload}
          className={cn(
            "flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium",
            "bg-[var(--color-accent)] text-white hover:bg-[#3f3f46] transition-colors"
          )}
        >
          <Download size={14} />
          Download PDF
        </button>
      </div>

      <div className="bg-white border border-[var(--color-border)] rounded-xl shadow-sm overflow-hidden">
        <div className="flex border-b border-[var(--color-border)] bg-[#fafafa] overflow-x-auto">
          {tabsWithContent.map((key) => {
            const Icon = ICON_MAP[key] || ClipboardList;
            const label = LABEL_MAP[key] || key;
            return (
              <button
                key={key}
                onClick={() => setActiveTab(key)}
                className={cn(
                  "flex items-center gap-1.5 px-4 py-3 text-sm font-medium transition-colors relative whitespace-nowrap",
                  activeTab === key
                    ? "text-[var(--color-foreground)]"
                    : "text-[var(--color-muted)] hover:text-[var(--color-foreground)]"
                )}
              >
                <Icon size={14} />
                {label}
                {activeTab === key && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[var(--color-accent)]" />
                )}
              </button>
            );
          })}
        </div>

        <div ref={reportRef} className="p-6 md:p-8 min-h-[400px]">
          <HtmlContent content={currentContent} />
        </div>
      </div>
    </div>
  );
}
