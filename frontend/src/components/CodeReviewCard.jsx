import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import AgentBadge from "./AgentBadge";
import { getReview } from "../utils/api";

// Findings are stored with the pipeline's own high/medium/low vocabulary;
// normalize to the dashboard's critical/warning/info vocabulary for display.
const SEVERITY_ALIASES = {
  critical: "critical",
  high: "critical",
  warning: "warning",
  medium: "warning",
  info: "info",
  low: "info",
};

const SEVERITY_STYLES = {
  critical: { bg: "rgba(232, 89, 60, 0.15)", color: "#E8593C", label: "Critical" },
  warning: { bg: "rgba(242, 166, 35, 0.15)", color: "#F2A623", label: "Warning" },
  info: { bg: "rgba(14, 211, 207, 0.15)", color: "#0ED3CF", label: "Info" },
};

function normalizeSeverity(severity) {
  return SEVERITY_ALIASES[(severity || "").toLowerCase()] || "info";
}

function timeAgo(dateStr) {
  const diffMs = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins} minute${mins === 1 ? "" : "s"} ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  const days = Math.floor(hours / 24);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}

export default function CodeReviewCard({ review }) {
  const [expanded, setExpanded] = useState(false);
  const [findings, setFindings] = useState(null);
  const [loading, setLoading] = useState(false);

  const toggle = async () => {
    if (!expanded && findings === null) {
      setLoading(true);
      try {
        const data = await getReview(review.id);
        setFindings(data.findings || []);
      } catch {
        setFindings([]);
      } finally {
        setLoading(false);
      }
    }
    setExpanded((v) => !v);
  };

  return (
    <div
      className="rounded-xl border transition-all duration-300"
      style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}
    >
      <button
        onClick={toggle}
        className="w-full flex items-center justify-between p-5 text-left rounded-xl transition-colors duration-300 hover:bg-[#1A2035]"
      >
        <div>
          <p className="font-semibold" style={{ color: "#E2E8F0" }}>
            {review.repo}{" "}
            <span className="font-normal" style={{ color: "#8892A8" }}>
              #{review.pr_number}
            </span>
          </p>
          <p className="text-sm mt-1" style={{ color: "#8892A8" }}>
            {timeAgo(review.created_at)} · {review.total_findings} finding
            {review.total_findings === 1 ? "" : "s"}
          </p>
        </div>
        {expanded ? (
          <ChevronUp size={18} style={{ color: "#8892A8" }} />
        ) : (
          <ChevronDown size={18} style={{ color: "#8892A8" }} />
        )}
      </button>

      {expanded && (
        <div className="px-5 pb-5" style={{ borderTop: "1px solid #1E2640" }}>
          {loading && (
            <p className="pt-4 text-sm" style={{ color: "#8892A8" }}>
              Loading findings...
            </p>
          )}
          {!loading && findings && findings.length === 0 && (
            <p className="pt-4 text-sm" style={{ color: "#8892A8" }}>
              No findings recorded for this review.
            </p>
          )}
          {!loading &&
            findings &&
            findings.map((f) => {
              const sev = SEVERITY_STYLES[normalizeSeverity(f.severity)];
              return (
                <div key={f.id} className="pt-4 flex flex-col gap-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <AgentBadge agent={f.agent} />
                    <span
                      className="px-2 py-0.5 rounded-full text-xs font-medium"
                      style={{ backgroundColor: sev.bg, color: sev.color }}
                    >
                      {sev.label}
                    </span>
                    <span
                      className="text-xs"
                      style={{ color: "#8892A8", fontFamily: '"SF Mono", "Fira Code", monospace' }}
                    >
                      {f.file}:{f.line}
                    </span>
                  </div>
                  <p className="text-sm" style={{ color: "#E2E8F0" }}>
                    {f.message}
                  </p>
                  {f.suggestion && (
                    <p className="text-sm" style={{ color: "#8892A8" }}>
                      Suggestion: {f.suggestion}
                    </p>
                  )}
                </div>
              );
            })}
        </div>
      )}
    </div>
  );
}
