const STYLES = {
  bug: "bg-red-500/15 text-red-400",
  security: "bg-orange-500/15 text-orange-400",
  quality: "bg-blue-500/15 text-blue-400",
};

export default function AgentBadge({ agent }) {
  const style = STYLES[agent] || "bg-gray-500/15 text-gray-400";
  return (
    <span className={`px-2.5 py-1 rounded-full text-xs font-medium capitalize ${style}`}>
      {agent}
    </span>
  );
}
