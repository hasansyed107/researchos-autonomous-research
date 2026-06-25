import { useState } from "react";
import { Upload, FileText, Sparkles, ArrowRight } from "lucide-react";

export default function ResearchForm({
  query,
  setQuery,
  generateReport,
  loading,
}) {
  const [file, setFile] = useState(null);

  const exampleTopics = [
    "quantum computing",
    "AI coding assistants",
    "EV battery market",
    "robotics in manufacturing",
  ];

  return (
    <div className="rounded-3xl border border-white/10 bg-slate-900/90 p-6 md:p-7 shadow-xl">
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-300 mb-3">
            <Sparkles size={14} />
            Launch a new research workflow
          </div>

          <h2 className="text-2xl font-bold text-white">Research Topic</h2>
          <p className="mt-2 text-slate-400 max-w-2xl">
            Enter a company, technology, market, product category, or strategic
            theme. Optionally upload a PDF to ground the analysis with your own
            source material.
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Query input */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Topic / Research Query
          </label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. quantum computing market outlook"
            className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-4 text-white placeholder:text-slate-500 outline-none transition focus:border-cyan-400/60 focus:ring-2 focus:ring-cyan-500/20"
          />

          <div className="mt-3 flex flex-wrap gap-2">
            {exampleTopics.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => setQuery(item)}
                className="rounded-full border border-slate-700 bg-slate-950 px-3 py-1.5 text-xs text-slate-300 hover:border-cyan-400/30 hover:text-white transition"
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {/* Upload */}
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Optional PDF grounding document
          </label>

          <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-950/80 px-6 py-8 text-center transition hover:border-cyan-400/40 hover:bg-slate-950">
            <Upload className="mb-3 text-cyan-300" size={24} />
            <p className="text-sm font-medium text-white">
              Upload a PDF for retrieval-augmented research
            </p>
            <p className="mt-1 text-sm text-slate-400">
              Annual reports, market reports, internal memos, whitepapers, or
              product docs
            </p>

            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>

          {file && (
            <div className="mt-3 flex items-center gap-3 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3">
              <FileText size={18} className="text-emerald-300" />
              <div className="min-w-0">
                <p className="text-sm font-medium text-emerald-200 truncate">
                  {file.name}
                </p>
                <p className="text-xs text-emerald-300/80">
                  PDF attached for research grounding
                </p>
              </div>
            </div>
          )}
        </div>

        {/* CTA */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 pt-2">
          <div className="text-sm text-slate-400 leading-6">
            ResearchOS will run a 7-agent workflow:
            <span className="text-slate-200">
              {" "}
              planning, market research, technology research, trends analysis,
              review, fact check, and final report writing.
            </span>
          </div>

          <button
            onClick={() => generateReport(file)}
            disabled={loading || !query.trim()}
            className={`inline-flex items-center justify-center gap-2 rounded-2xl px-6 py-3 font-semibold transition-all ${
              loading || !query.trim()
                ? "cursor-not-allowed bg-slate-700 text-slate-400"
                : "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20 hover:-translate-y-0.5 hover:shadow-cyan-500/30"
            }`}
          >
            {loading ? "Generating Research..." : "Generate Research"}
            {!loading && <ArrowRight size={18} />}
          </button>
        </div>
      </div>
    </div>
  );
}