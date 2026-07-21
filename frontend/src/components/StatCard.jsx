// Reusable stat card with an optional count-up animation for numeric values.
import { useEffect, useRef, useState } from "react";

/** Reusable stat card. When `animate` is true and `value` is a number, the
 * displayed number counts up from 0 via requestAnimationFrame. Otherwise
 * `value` is rendered as-is (for static marketing copy like "< 30s"). */
export default function StatCard({ icon: Icon, value, label, accent = "#0ED3CF", animate = false }) {
  const [display, setDisplay] = useState(animate && typeof value === "number" ? 0 : value);
  const frameRef = useRef();

  useEffect(() => {
    if (!animate || typeof value !== "number") {
      setDisplay(value);
      return;
    }

    const duration = 900;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(eased * value));
      if (progress < 1) {
        frameRef.current = requestAnimationFrame(tick);
      }
    }

    frameRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameRef.current);
  }, [value, animate]);

  return (
    <div
      className="rounded-xl p-6 border transition-all duration-300 hover:scale-105"
      style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}
    >
      <div className="flex items-center justify-between mb-3">
        {Icon && <Icon size={20} style={{ color: accent }} />}
      </div>
      <p
        className="text-3xl font-bold"
        style={{ color: accent, fontFamily: '"SF Mono", "Fira Code", monospace' }}
      >
        {display}
      </p>
      <p className="text-sm mt-1" style={{ color: "#8892A8" }}>
        {label}
      </p>
    </div>
  );
}
