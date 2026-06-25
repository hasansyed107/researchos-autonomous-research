import {
  FileText,
  History,
  Search,
  Sparkles,
  Activity,
  Database,
} from "lucide-react";

export default function Sidebar() {
  const navItems = [
    {
      label: "New Research",
      icon: Search,
      active: true,
    },
    {
      label: "History",
      icon: History,
      active: false,
    },
    {
      label: "Reports",
      icon: FileText,
      active: false,
    },
  ];

  return (
    <aside className="hidden md:flex w-72 min-h-screen bg-slate-950 border-r border-white/10 flex-col px-5 py-6">
      {/* Brand */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-3 rounded-2xl border border-cyan-500/20 bg-cyan-500/10 px-4 py-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 shadow-lg shadow-cyan-500/20">
            <Sparkles size={20} className="text-white" />
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-tight text-white">
              ResearchOS
            </h1>
            <p className="text-xs text-slate-400">
              Autonomous Research Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <div className="space-y-2">
        <p className="px-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
          Workspace
        </p>

        <nav className="space-y-2">
          {navItems.map(({ label, icon: Icon, active }) => (
            <button
              key={label}
              className={`group flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left transition-all ${
                active
                  ? "bg-gradient-to-r from-cyan-500/15 to-blue-500/10 border border-cyan-400/20 text-white shadow-lg shadow-cyan-500/5"
                  : "border border-transparent text-slate-300 hover:bg-slate-900 hover:border-white/10 hover:text-white"
              }`}
            >
              <div
                className={`flex h-10 w-10 items-center justify-center rounded-xl ${
                  active
                    ? "bg-cyan-400/10 text-cyan-300"
                    : "bg-slate-900 text-slate-400 group-hover:text-cyan-300"
                }`}
              >
                <Icon size={18} />
              </div>

              <div className="flex flex-col">
                <span className="text-sm font-medium">{label}</span>
                <span className="text-xs text-slate-500">
                  {label === "New Research" && "Start a new multi-agent run"}
                  {label === "History" && "Review previous research sessions"}
                  {label === "Reports" && "Open generated analysis outputs"}
                </span>
              </div>
            </button>
          ))}
        </nav>
      </div>

      {/* Platform status */}
      <div className="mt-8 rounded-3xl border border-white/10 bg-slate-900/80 p-4">
        <div className="mb-3 flex items-center gap-2">
          <Activity size={16} className="text-emerald-400" />
          <h3 className="text-sm font-semibold text-white">Platform Status</h3>
        </div>

        <div className="space-y-3">
          <div className="rounded-2xl border border-white/5 bg-slate-950/70 p-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">Workflow</span>
              <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-300">
                Ready
              </span>
            </div>
            <p className="mt-2 text-sm text-slate-200">
              Planner → Researchers → Reviewer → Writer
            </p>
          </div>

          <div className="rounded-3xl border border-white/10 bg-slate-900/90 p-5 mt-auto">
            <div className="flex items-center gap-2 text-slate-300">
              <Database size={14} className="text-cyan-300" />
              <span className="text-xs">Model pipeline</span>
            </div>
            <p className="mt-2 text-sm font-medium text-white">
              Cerebras → OpenRouter
            </p>
          </div>
        </div>
      </div>

 
      {/* Footer */}
      <div className="mt-auto pt-6">
      <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900 to-slate-950 p-5">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
      Why ResearchOS
      </p>

      <h3 className="mt-3 text-sm font-semibold text-white">
      Multi-agent research workflow for structured analysis
      </h3>

      <div className="mt-4 space-y-3">
      {[
      "Planning → market → technology → trends → review → fact check → writing",
      "Source-backed synthesis with fallback-safe reporting",
      "PDF-grounded analysis and exportable research outputs",
      ].map((item) => (
      <div key={item} className="flex items-start gap-3">
      <div className="mt-1 h-2 w-2 rounded-full bg-cyan-400" />
      <p className="text-sm leading-6 text-slate-300">{item}</p>
      </div>
      ))}
      </div>
      </div>
      </div>
    </aside>
  );
}