import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AlertTriangle, BarChart3, Info, User as UserIcon } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import StatCard from "../components/StatCard";
import CodeReviewCard from "../components/CodeReviewCard";
import { getReviews, getStats } from "../utils/api";

const AGENT_COLORS = { bug: "#F2A623", security: "#E8593C", quality: "#4ADE80" };
const AGENT_LABELS = { bug: "Bug", security: "Security", quality: "Quality" };

function topAgentLabel(findingsByAgent) {
  const entries = Object.entries(findingsByAgent || {});
  if (entries.length === 0) return "—";
  const [agent] = entries.reduce((best, cur) => (cur[1] > best[1] ? cur : best));
  return AGENT_LABELS[agent] || agent;
}

function SkeletonBlock({ className = "" }) {
  return (
    <div
      className={`animate-pulse rounded-xl ${className}`}
      style={{ backgroundColor: "#131825", border: "1px solid #1E2640" }}
    />
  );
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [reviews, setReviews] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [statsData, reviewsData] = await Promise.all([getStats(), getReviews()]);
        if (cancelled) return;
        setStats(statsData);
        setReviews(reviewsData.reviews || []);
      } catch (err) {
        // Especially on 401 (expired/invalid token), bounce back to landing
        // rather than showing a broken authenticated dashboard.
        if (!cancelled) navigate("/");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [navigate]);

  const pieData = useMemo(() => {
    if (!stats) return [];
    return Object.entries(stats.findings_by_agent || {}).map(([agent, count]) => ({
      name: AGENT_LABELS[agent] || agent,
      value: count,
      color: AGENT_COLORS[agent] || "#8892A8",
    }));
  }, [stats]);

  return (
    <div style={{ backgroundColor: "#0B0F1A", minHeight: "100vh" }}>
      <Navbar showLinks={false} />

      <main className="max-w-6xl mx-auto px-6 py-10">
        <h1 className="text-2xl font-bold mb-8" style={{ color: "#E2E8F0" }}>
          Dashboard
        </h1>

        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
            {[0, 1, 2, 3].map((i) => (
              <SkeletonBlock key={i} className="h-28" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
            <StatCard icon={BarChart3} value={stats.total_reviews} label="Total Reviews" animate />
            <StatCard icon={Info} value={stats.total_findings} label="Total Findings" animate />
            <StatCard
              icon={AlertTriangle}
              value={stats.findings_by_severity?.critical ?? 0}
              label="Critical Issues"
              accent="#E8593C"
              animate
            />
            <StatCard
              icon={UserIcon}
              value={topAgentLabel(stats.findings_by_agent)}
              label="Top Agent"
              accent="#4ADE80"
            />
          </div>
        )}

        {!loading && stats && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">
            <div className="rounded-xl border p-6" style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}>
              <h2 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>
                Review activity (last 7 days)
              </h2>
              {stats.recent_activity && stats.recent_activity.length > 0 ? (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={stats.recent_activity}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E2640" vertical={false} />
                    <XAxis dataKey="date" stroke="#8892A8" fontSize={12} tickLine={false} axisLine={{ stroke: "#1E2640" }} />
                    <YAxis stroke="#8892A8" fontSize={12} tickLine={false} axisLine={{ stroke: "#1E2640" }} allowDecimals={false} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#0F1420", border: "1px solid #1E2640", borderRadius: 8 }}
                      labelStyle={{ color: "#E2E8F0" }}
                      itemStyle={{ color: "#0ED3CF" }}
                    />
                    <Bar dataKey="count" fill="#0ED3CF" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-sm py-16 text-center" style={{ color: "#8892A8" }}>
                  No activity in the last 7 days.
                </p>
              )}
            </div>

            <div className="rounded-xl border p-6" style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}>
              <h2 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>
                Findings by agent
              </h2>
              {pieData.length > 0 ? (
                <div className="relative">
                  <ResponsiveContainer width="100%" height={240}>
                    <PieChart>
                      <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={60} outerRadius={90} paddingAngle={2}>
                        {pieData.map((entry) => (
                          <Cell key={entry.name} fill={entry.color} stroke="none" />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{ backgroundColor: "#0F1420", border: "1px solid #1E2640", borderRadius: 8 }}
                        labelStyle={{ color: "#E2E8F0" }}
                      />
                      <Legend
                        verticalAlign="bottom"
                        height={36}
                        formatter={(value) => <span style={{ color: "#8892A8", fontSize: 12 }}>{value}</span>}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                  <div
                    className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none"
                    style={{ top: 0, bottom: 36 }}
                  >
                    <p className="text-2xl font-bold" style={{ color: "#E2E8F0" }}>
                      {stats.total_findings}
                    </p>
                    <p className="text-xs" style={{ color: "#8892A8" }}>
                      findings
                    </p>
                  </div>
                </div>
              ) : (
                <p className="text-sm py-16 text-center" style={{ color: "#8892A8" }}>
                  No findings recorded yet.
                </p>
              )}
            </div>
          </div>
        )}

        <h2 className="text-lg font-semibold mb-4" style={{ color: "#E2E8F0" }}>
          Recent reviews
        </h2>

        {loading ? (
          <div className="flex flex-col gap-3">
            {[0, 1, 2].map((i) => (
              <SkeletonBlock key={i} className="h-20" />
            ))}
          </div>
        ) : reviews && reviews.length > 0 ? (
          <div className="flex flex-col gap-3">
            {reviews.map((review) => (
              <CodeReviewCard key={review.id} review={review} />
            ))}
          </div>
        ) : (
          <div
            className="rounded-xl border p-10 text-center"
            style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}
          >
            <p style={{ color: "#E2E8F0" }} className="font-semibold mb-1">
              No reviews yet
            </p>
            <p className="text-sm" style={{ color: "#8892A8" }}>
              Open a pull request on a connected repo and CodeGuard will review it automatically.
            </p>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
