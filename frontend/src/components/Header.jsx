import { Sparkles, ShieldCheck, Cpu } from "lucide-react";

export default function Header() {
  return (
    <div className="mb-8">
      <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 p-6 shadow-2xl shadow-cyan-500/5">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1 text-xs font-medium text-cyan-300 mb-4">
              <Sparkles size={14} />
              Autonomous Research Intelligence Platform
            </div>

            <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white">
              ResearchOS
            </h1>

            <p className="mt-3 max-w-3xl text-slate-400 text-base md:text-lg leading-7">
              A multi-agent research system for market analysis, technology
              intelligence, trend discovery, fact checking, and final report
              generation — built as an end-to-end research workflow product.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 min-w-[280px]">
            <div className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <div className="flex items-center gap-2 text-slate-300">
                <Cpu size={16} className="text-cyan-300" />
                <span className="text-sm font-medium">Agent Workflow</span>
              </div>
              <p className="mt-2 text-sm text-slate-400 leading-6">
                Planner → Researchers → Reviewer → Fact Checker → Writer
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <div className="flex items-center gap-2 text-slate-300">
                <ShieldCheck size={16} className="text-emerald-300" />
                <span className="text-sm font-medium">Report Quality</span>
              </div>
              <p className="mt-2 text-sm text-slate-400 leading-6">
                Grounded synthesis with source-backed research and fallback-safe
                reporting.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}