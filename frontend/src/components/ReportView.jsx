import { useRef } from "react";
import ReactMarkdown from "react-markdown";
import { Download } from "lucide-react";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { cn } from "../lib/utils";

export default function ReportView({ report, idea }) {
  const reportRef = useRef(null);

  const handleDownload = async () => {
    if (!reportRef.current) return;

    const element = reportRef.current;
    const canvas = await html2canvas(element, {
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

  return (
    <div className="w-full max-w-3xl">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-[var(--color-foreground)]">
          Report
        </h2>
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

      <div
        ref={reportRef}
        className="bg-white border border-[var(--color-border)] rounded-xl p-6 md:p-8 shadow-sm markdown-content"
      >
        <div className="mb-6 pb-4 border-b border-[var(--color-border)]">
          <h1 className="text-xl font-bold text-[var(--color-foreground)]">
            Startup CTO Report
          </h1>
          <p className="text-sm text-[var(--color-muted)] mt-1">{idea}</p>
        </div>
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </div>
  );
}
