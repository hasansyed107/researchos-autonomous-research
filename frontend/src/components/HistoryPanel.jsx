import { Clock3, FileText, History as HistoryIcon } from "lucide-react";

function HistoryPanel({ history = [], setReport, setGeneratedAt, setQuery }) {
  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/90 p-5 shadow-xl">
      <div className="mb-5">
        <div className="inline-flex items-center gap-2 rounded-full border border-violet-500/20 bg-violet-500/10 px-3 py-1 text-xs font-medium text-violet-300 mb-3">
          <HistoryIcon size={14} />
          Saved Sessions
        </div>

        <h2 className="text-lg font-bold text-white">Research History</h2>
        <p className="text-sm text-slate-400 mt-1">
          Re-open previously generated reports from local session history
        </p>
      </div>

      <div className="space-y-3 max-h-[560px] overflow-y-auto pr-1">
        {history.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-950/60 p-5 text-center">
            <p className="text-sm text-slate-400">
              No reports generated yet. Your completed research runs will appear
              here.
            </p>
          </div>
        ) : (
          history.map((item, index) => (
            <button
              key={item.id}
              onClick={() => {
                setReport(item.report);
                setGeneratedAt?.(item.generatedAt || "");
                setQuery?.(item.query || "");
              }}
              className="w-full rounded-2xl border border-white/10 bg-slate-950/70 p-4 text-left transition hover:border-cyan-400/20 hover:bg-slate-950"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex gap-3 min-w-0">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 border border-white/5">
                    <FileText size={16} className="text-cyan-300" />
                  </div>

                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-medium text-slate-500">
                        #{history.length - index}
                      </span>
                      <span className="text-sm font-semibold text-white truncate">
                        {item.query}
                      </span>
                    </div>

                    <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
                      <Clock3 size={13} />
                      <span>{item.generatedAt || "Unknown time"}</span>
                    </div>
                  </div>
                </div>
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
}

export default HistoryPanel;