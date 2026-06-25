import { Activity, CheckCircle2, Clock3, AlertCircle, Bot } from "lucide-react";

function ProgressPanel({ agentStatus = {} }) {
  const agents = [
    ["Planner", "planner", "Breaks the topic into a research plan"],
    ["Market Research", "market", "Finds market, competition, pricing, growth"],
    ["Technology Research", "technology", "Analyzes stack, models, infra, architecture"],
    ["Trends Research", "trends", "Explores future trends and adoption signals"],
    ["Reviewer", "reviewer", "Reviews quality, gaps, and strategic usefulness"],
    ["Fact Checker", "factchecker", "Validates claims against evidence"],
    ["Writer", "writer", "Produces the final report"],
  ];

  const getStatusMeta = (status) => {
    switch (status) {
      case "complete":
        return {
          label: "Complete",
          icon: <CheckCircle2 size={16} className="text-emerald-400" />,
          badge: "bg-emerald-500/10 text-emerald-300 border-emerald-500/20",
          ring: "border-emerald-500/20 bg-emerald-500/5",
        };
      case "running":
        return {
          label: "Running",
          icon: <Activity size={16} className="text-yellow-400 animate-pulse" />,
          badge: "bg-yellow-500/10 text-yellow-300 border-yellow-500/20",
          ring: "border-yellow-500/20 bg-yellow-500/5",
        };
      case "error":
        return {
          label: "Error",
          icon: <AlertCircle size={16} className="text-red-400" />,
          badge: "bg-red-500/10 text-red-300 border-red-500/20",
          ring: "border-red-500/20 bg-red-500/5",
        };
      default:
        return {
          label: "Waiting",
          icon: <Clock3 size={16} className="text-slate-500" />,
          badge: "bg-slate-800 text-slate-400 border-slate-700",
          ring: "border-white/5 bg-slate-900/50",
        };
    }
  };

  const completedCount = Object.values(agentStatus).filter(
    (v) => v === "complete"
  ).length;
  const totalCount = agents.length;
  const progress = Math.round((completedCount / totalCount) * 100);

  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/90 p-5 shadow-xl">
      <div className="flex items-start justify-between gap-4 mb-5">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1 text-xs font-medium text-cyan-300 mb-3">
            <Bot size={14} />
            Multi-Agent Workflow
          </div>
          <h2 className="text-lg font-bold text-white">Agent Progress</h2>
          <p className="text-sm text-slate-400 mt-1">
            Live status of the autonomous research pipeline
          </p>
        </div>

        <div className="text-right">
          <div className="text-2xl font-bold text-white">{progress}%</div>
          <div className="text-xs text-slate-500">
            {completedCount}/{totalCount} completed
          </div>
        </div>
      </div>

      <div className="mb-5">
        <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="space-y-3">
        {agents.map(([label, key, description], index) => {
          const meta = getStatusMeta(agentStatus[key]);

          return (
            <div
              key={key}
              className={`rounded-2xl border p-4 transition ${meta.ring}`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-950 border border-white/5 text-slate-300">
                    <span className="text-sm font-semibold">{index + 1}</span>
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      {meta.icon}
                      <h3 className="text-sm font-semibold text-white">
                        {label}
                      </h3>
                    </div>
                    <p className="mt-1 text-xs leading-5 text-slate-400">
                      {description}
                    </p>
                  </div>
                </div>

                <span
                  className={`shrink-0 rounded-full border px-2.5 py-1 text-[11px] font-medium ${meta.badge}`}
                >
                  {meta.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-5 rounded-2xl border border-white/10 bg-slate-950/70 p-4">
        <h3 className="text-sm font-semibold text-white mb-2">
          Workflow Summary
        </h3>
        <p className="text-sm text-slate-400 leading-6">
          ResearchOS runs a structured 7-step workflow to turn a raw research
          topic into a synthesized report with review and fact-checking layers.
        </p>
      </div>
    </div>
  );
}

export default ProgressPanel;