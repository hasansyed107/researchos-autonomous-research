import { useMemo, useState } from "react";
import API from "./api";
import { jsPDF } from "jspdf";

import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import ResearchForm from "./components/ResearchForm";
import ProgressPanel from "./components/ProgressPanel";
import ReportViewer from "./components/ReportViewer";
import HistoryPanel from "./components/HistoryPanel";

const AGENTS = [
  "Planner",
  "Market Research",
  "Technology Research",
  "Trends Research",
  "Reviewer",
  "Fact Checker",
  "Writer",
];

function App() {
  const [agentStatus, setAgentStatus] = useState({
    planner: "waiting",
    market: "waiting",
    technology: "waiting",
    trends: "waiting",
    reviewer: "waiting",
    factchecker: "waiting",
    writer: "waiting",
  });

  const [query, setQuery] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedAt, setGeneratedAt] = useState("");
  const [error, setError] = useState("");

  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem("research_history");
    return saved ? JSON.parse(saved) : [];
  });

  const statCards = useMemo(
    () => [
      {
        label: "AI Agents",
        value: AGENTS.length,
        subtext: "Autonomous workflow nodes",
      },
      {
        label: "Research Status",
        value: loading ? "Running" : "Ready",
        subtext: loading
          ? "Workflow currently executing"
          : "System ready for a new run",
      },
      {
        label: "Model Pipeline",
        value: "Cerebras → OpenRouter",
        subtext: "Primary generation + fallback stack",
      },
    ],
    [loading]
  );

  const resetAgentStatus = () => {
    setAgentStatus({
      planner: "waiting",
      market: "waiting",
      technology: "waiting",
      trends: "waiting",
      reviewer: "waiting",
      factchecker: "waiting",
      writer: "waiting",
    });
  };

  const completeAgentStatus = () => {
    setAgentStatus({
      planner: "complete",
      market: "complete",
      technology: "complete",
      trends: "complete",
      reviewer: "complete",
      factchecker: "complete",
      writer: "complete",
    });
  };

  const errorAgentStatus = () => {
    setAgentStatus({
      planner: "error",
      market: "error",
      technology: "error",
      trends: "error",
      reviewer: "error",
      factchecker: "error",
      writer: "error",
    });
  };

  const extractReportFromResponse = (responseData) => {
    const data =
      responseData?.result ||
      responseData?.data ||
      responseData ||
      {};

    console.log("NORMALIZED DATA:", data);

    if (typeof data.report === "string" && data.report.trim()) {
      return {
        report: data.report.trim(),
        generatedAt: data.generated_at || new Date().toLocaleString(),
        raw: data,
      };
    }

    if (
      data.writer &&
      typeof data.writer.report === "string" &&
      data.writer.report.trim()
    ) {
      return {
        report: data.writer.report.trim(),
        generatedAt: data.generated_at || new Date().toLocaleString(),
        raw: data,
      };
    }

    if (
      typeof data.research_summary === "string" &&
      data.research_summary.trim()
    ) {
      return {
        report: data.research_summary.trim(),
        generatedAt: data.generated_at || new Date().toLocaleString(),
        raw: data,
      };
    }

    const sections = [
      data.plan ? `# Research Plan\n\n${data.plan}` : "",
      data.market_research ? `# Market Research\n\n${data.market_research}` : "",
      data.technology_research
        ? `# Technology Research\n\n${data.technology_research}`
        : "",
      data.trends_research ? `# Trends Research\n\n${data.trends_research}` : "",
      data.research_summary
        ? `# Research Summary\n\n${data.research_summary}`
        : "",
      data.review ? `# Review\n\n${data.review}` : "",
      data.fact_check ? `# Fact Check\n\n${data.fact_check}` : "",
    ].filter(Boolean);

    if (sections.length > 0) {
      return {
        report: sections.join("\n\n---\n\n"),
        generatedAt: data.generated_at || new Date().toLocaleString(),
        raw: data,
      };
    }

    return {
      report: "",
      generatedAt: "",
      raw: data,
    };
  };

  const generateReport = async (file) => {
    if (!query.trim()) return;

    let timers = [];

    try {
      setLoading(true);
      setError("");
      setReport("");
      setGeneratedAt("");
      resetAgentStatus();

      const formData = new FormData();
      formData.append("query", query);

      if (file) {
        formData.append("file", file);
      }

      setAgentStatus({
        planner: "running",
        market: "waiting",
        technology: "waiting",
        trends: "waiting",
        reviewer: "waiting",
        factchecker: "waiting",
        writer: "waiting",
      });

      timers.push(
        setTimeout(() => {
          setAgentStatus((prev) => ({
            ...prev,
            planner: "complete",
            market: "running",
          }));
        }, 1000)
      );

      timers.push(
        setTimeout(() => {
          setAgentStatus((prev) => ({
            ...prev,
            market: "complete",
            technology: "running",
          }));
        }, 2500)
      );

      timers.push(
        setTimeout(() => {
          setAgentStatus((prev) => ({
            ...prev,
            technology: "complete",
            trends: "running",
          }));
        }, 4000)
      );

      timers.push(
        setTimeout(() => {
          setAgentStatus((prev) => ({
            ...prev,
            trends: "complete",
            reviewer: "running",
          }));
        }, 5500)
      );

      timers.push(
        setTimeout(() => {
          setAgentStatus((prev) => ({
            ...prev,
            reviewer: "complete",
            factchecker: "running",
          }));
        }, 7000)
      );

      timers.push(
        setTimeout(() => {
          setAgentStatus((prev) => ({
            ...prev,
            factchecker: "complete",
            writer: "running",
          }));
        }, 8500)
      );

      const response = await API.post("/research", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("FULL BACKEND RESPONSE:", response.data);

      timers.forEach(clearTimeout);

      const extracted = extractReportFromResponse(response.data);

      if (!extracted.report) {
        throw new Error(
          "Backend returned successfully, but no report content was found."
        );
      }

      setReport(extracted.report);
      setGeneratedAt(extracted.generatedAt);
      setError("");
      completeAgentStatus();

      const newReport = {
        id: Date.now(),
        query,
        report: extracted.report,
        generatedAt: extracted.generatedAt,
        raw: extracted.raw,
      };

      setHistory((prev) => {
        const updated = [newReport, ...prev];
        localStorage.setItem("research_history", JSON.stringify(updated));
        return updated;
      });
    } catch (err) {
      console.error("Research request failed:", err);
      console.error("Axios response:", err?.response);
      console.error("Axios response data:", err?.response?.data);

      timers.forEach(clearTimeout);
      errorAgentStatus();

      setReport("");
      setGeneratedAt("");
      setError(
        err?.response?.data?.detail ||
          err?.response?.data?.message ||
          err?.message ||
          "Failed to generate research report."
      );
    } finally {
      setLoading(false);
    }
  };

  const exportPDF = () => {
    if (!report) return;

    const doc = new jsPDF();
    const lines = doc.splitTextToSize(report, 180);
    doc.text(lines, 10, 10);
    doc.save(`${query || "research-report"}.pdf`);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex">
      <Sidebar />

      <div className="flex-1 overflow-y-auto">
        <div className="px-4 md:px-8 py-6 max-w-[1700px] mx-auto">
          <Header />

          {/* Stat cards */}
          <div className="grid md:grid-cols-3 gap-4 mb-6">
            {statCards.map((card) => (
              <div
                key={card.label}
                className="rounded-3xl border border-white/10 bg-slate-900/90 p-5 shadow-xl"
              >
                <p className="text-sm text-slate-400">{card.label}</p>
                <h2
                  className={`mt-3 font-bold tracking-tight ${
                    card.label === "Model Pipeline"
                      ? "text-xl md:text-2xl text-white"
                      : "text-3xl text-white"
                  } ${
                    card.label === "Research Status"
                      ? loading
                        ? "text-yellow-400"
                        : "text-emerald-400"
                      : ""
                  }`}
                >
                  {card.value}
                </h2>
                <p className="mt-2 text-sm text-slate-500">{card.subtext}</p>
              </div>
            ))}
          </div>

          {error && (
            <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/10 px-5 py-4 text-red-300">
              <div className="font-semibold mb-1">Research generation failed</div>
              <div className="text-sm text-red-200/90">{error}</div>
            </div>
          )}

          <div className="grid xl:grid-cols-4 gap-6 items-start">
            {/* Main content */}
            <div className="xl:col-span-3 space-y-6">
              <ResearchForm
                query={query}
                setQuery={setQuery}
                generateReport={generateReport}
                loading={loading}
              />

              <div className="panel-card p-0 overflow-hidden">
              <div className="flex items-center justify-between px-8 py-6 border-b border-white/10">
              <div>
              <h2 className="text-2xl font-bold text-white">Research Report</h2>
              <p className="text-sm text-slate-400">
              Multi-agent AI generated analysis
              </p>
              <p className="text-xs text-slate-500 mt-2">
              Generated: {generatedAt || "-"}
              </p>
              </div>

              <button
              onClick={exportPDF}
              disabled={!report}
              className={`px-4 py-2 rounded-xl font-medium transition ${
              report
              ? "bg-cyan-500/15 text-cyan-300 border border-cyan-400/20 hover:bg-cyan-500/25"
              : "bg-slate-800 text-slate-500 cursor-not-allowed"
              }`}
              >
              Export PDF
              </button>
              </div>

              <div className="p-8 min-h-[520px]">
              {loading ? (
              <div className="h-full flex flex-col justify-center">
              <div className="space-y-4 animate-pulse">
              <div className="h-5 rounded-xl bg-slate-800"></div>
              <div className="h-5 w-11/12 rounded-xl bg-slate-800"></div>
              <div className="h-5 w-10/12 rounded-xl bg-slate-800"></div>
              <div className="h-5 w-8/12 rounded-xl bg-slate-800"></div>
              <div className="h-40 rounded-2xl bg-slate-800 mt-6"></div>
              </div>
              </div>
              ) : (
              <ReportViewer report={report} />
              )}
              </div>
              </div>
            </div>

            {/* Right rail */}
            <div className="space-y-6 self-start xl:sticky xl:top-6">
              <ProgressPanel agentStatus={agentStatus} />
              <HistoryPanel
                history={history}
                setReport={setReport}
                setGeneratedAt={setGeneratedAt}
                setQuery={setQuery}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;