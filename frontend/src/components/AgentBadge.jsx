// Colored pill badge for an agent name (bug/security/quality).
const AGENT_STYLES = {
  bug: { bg: "rgba(242, 166, 35, 0.15)", color: "#F2A623", label: "Bug" },
  security: { bg: "rgba(232, 89, 60, 0.15)", color: "#E8593C", label: "Security" },
  quality: { bg: "rgba(74, 222, 128, 0.15)", color: "#4ADE80", label: "Quality" },
};

export default function AgentBadge({ agent }) {
  const style = AGENT_STYLES[agent] || {
    bg: "rgba(136, 146, 168, 0.15)",
    color: "#8892A8",
    label: agent || "Unknown",
  };

  return (
    <span
      className="px-2.5 py-1 rounded-full text-xs font-medium inline-flex items-center transition-all duration-300"
      style={{ backgroundColor: style.bg, color: style.color }}
    >
      {style.label}
    </span>
  );
}
