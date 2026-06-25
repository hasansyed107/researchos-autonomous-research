import ReactMarkdown from "react-markdown";
import { FileText, BarChart3, Cpu, TrendingUp } from "lucide-react";

function EmptyState() {
  const items = [
    {
      title: "Market",
      desc: "Sizing, competitors, growth drivers, and business signals.",
      icon: BarChart3,
    },
    {
      title: "Technology",
      desc: "Architecture, models, infrastructure, and technical constraints.",
      icon: Cpu,
    },
    {
      title: "Trends",
      desc: "Future outlook, adoption patterns, and strategic signals.",
      icon: TrendingUp,
    },
  ];

  return (
    <div className="min-h-[420px] flex flex-col justify-center">
      <div className="text-center max-w-2xl mx-auto">
        <div className="w-16 h-16 mx-auto rounded-2xl bg-cyan-500/10 border border-cyan-400/20 flex items-center justify-center mb-5">
          <FileText className="w-8 h-8 text-cyan-300" />
        </div>

        <h3 className="text-2xl font-bold text-white mb-3">
          No report generated yet
        </h3>

        <p className="text-slate-400 leading-7">
          Enter a research topic and run the multi-agent workflow to generate a
          source-backed report with market analysis, technology insights, future
          trends, review, and fact-checking.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-4 mt-10">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.title}
              className="rounded-2xl border border-white/10 bg-slate-950/50 p-5"
            >
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-400/20 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-cyan-300" />
              </div>
              <h4 className="text-white font-semibold mb-2">{item.title}</h4>
              <p className="text-sm text-slate-400 leading-6">{item.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function ReportViewer({ report }) {
  if (!report || !report.trim()) {
    return <EmptyState />;
  }

  return (
    <div className="report-markdown prose prose-invert max-w-none">
      <ReactMarkdown>{report}</ReactMarkdown>
    </div>
  );
}