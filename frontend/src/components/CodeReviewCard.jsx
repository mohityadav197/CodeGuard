import AgentBadge from "./AgentBadge";

const SEVERITY_STYLES = {
  high: "text-red-400",
  medium: "text-yellow-400",
  low: "text-blue-400",
};

export default function CodeReviewCard({ review }) {
  const { repo, pr_number, status, total_findings, findings = [] } = review;

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-white font-semibold">
            {repo} <span className="text-gray-500">#{pr_number}</span>
          </p>
          <p className="text-gray-400 text-sm capitalize">{status}</p>
        </div>
        <p className="text-gray-400 text-sm">{total_findings} finding(s)</p>
      </div>

      {findings.length > 0 && (
        <ul className="mt-4 space-y-2">
          {findings.map((finding) => (
            <li key={finding.id} className="flex items-start gap-3 text-sm">
              <AgentBadge agent={finding.agent} />
              <span className={SEVERITY_STYLES[finding.severity] || "text-gray-300"}>
                {finding.file}:{finding.line} — {finding.message}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
