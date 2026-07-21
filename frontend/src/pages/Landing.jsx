// Landing page: hero, animated code-review demo, features, how-it-works, and CTA sections.
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  AlertTriangle,
  ArrowRight,
  Bug,
  Check,
  Clock,
  GitPullRequest,
  Play,
  Shield,
  Sparkles,
  Star,
  X,
  Zap,
} from "lucide-react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import StatCard from "../components/StatCard";

const ERROR_MESSAGES = {
  auth_failed: "Login failed. Please try again.",
  server_error: "Something went wrong. Please try again.",
};

const MONO = '"SF Mono", "Fira Code", monospace';

const CODE_LINES = [
  { num: 1, text: "import stripe", type: "plain" },
  { num: 2, text: "", type: "plain" },
  { num: 3, text: 'STRIPE_API_KEY = "sk_live_51Hc3x9K8e2nP..."', type: "security" },
  { num: 4, text: "", type: "plain" },
  { num: 5, text: "def get_user(user_id):", type: "plain" },
  { num: 6, text: '    query = f"SELECT * FROM users WHERE id = {user_id}"', type: "security" },
  { num: 7, text: "    return db.execute(query)", type: "plain" },
  { num: 8, text: "", type: "plain" },
  { num: 9, text: "def refund_rate(refunds, total):", type: "plain" },
  { num: 10, text: "    return refunds / total", type: "bug" },
];

const COMMENTS = [
  {
    line: 3,
    type: "security",
    title: "Security Agent",
    message: "Hardcoded Stripe secret key. Move this to an environment variable or secrets manager.",
    delay: 800,
  },
  {
    line: 6,
    type: "security",
    title: "Security Agent",
    message: "SQL injection risk: user_id is interpolated directly into the query. Use parameterized queries.",
    delay: 2000,
  },
  {
    line: 10,
    type: "bug",
    title: "Bug Agent",
    message: "Division by zero when total is 0. Add a guard clause before dividing.",
    delay: 3200,
  },
];

const FEATURES = [
  {
    icon: Bug,
    accent: "#F2A623",
    title: "Bug Detection",
    description:
      "Catches logic errors, off-by-one bugs, null dereferences, unhandled edge cases, and type mismatches before they hit production.",
  },
  {
    icon: Shield,
    accent: "#E8593C",
    title: "Security Analysis",
    description:
      "Flags SQL injection, hardcoded secrets, insecure dependencies, and OWASP top-10 vulnerabilities with fix suggestions.",
  },
  {
    icon: Star,
    accent: "#4ADE80",
    title: "Code Quality",
    description:
      "Reviews naming conventions, dead code, code duplication, complexity, and adherence to your team's style guide.",
  },
];

const STEPS = [
  {
    title: "Open a pull request",
    description: "Push your branch and open a PR on GitHub like you normally would.",
  },
  {
    title: "Agents analyze the diff",
    description: "Three specialized agents review for bugs, security holes, and code quality in parallel.",
  },
  {
    title: "Get inline comments",
    description: "Findings appear as contextual comments right on the lines that matter.",
  },
  {
    title: "Fix and merge",
    description: "Address the issues, push again, and merge with confidence.",
  },
];

const STATS = [
  { icon: Zap, value: "3", label: "Parallel agents" },
  { icon: Clock, value: "< 30s", label: "Review time" },
  { icon: Check, value: "94%", label: "Catch rate" },
  { icon: GitPullRequest, value: "0", label: "Setup required" },
];

function ErrorBanner({ message, onDismiss }) {
  return (
    <div
      className="fixed top-4 left-1/2 -translate-x-1/2 z-[60] flex items-center gap-3 px-4 py-3 rounded-lg border shadow-lg"
      style={{ backgroundColor: "#131825", borderColor: "#E8593C", color: "#E2E8F0" }}
    >
      <AlertTriangle size={18} style={{ color: "#E8593C" }} />
      <span className="text-sm">{message}</span>
      <button
        onClick={onDismiss}
        className="transition-colors duration-300 hover:text-[#E2E8F0]"
        style={{ color: "#8892A8" }}
        aria-label="Dismiss"
      >
        <X size={16} />
      </button>
    </div>
  );
}

export default function Landing() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    const error = searchParams.get("error");
    if (error && ERROR_MESSAGES[error]) {
      setErrorMessage(ERROR_MESSAGES[error]);
    }
  }, [searchParams]);

  const dismissError = () => {
    setErrorMessage(null);
    const next = new URLSearchParams(searchParams);
    next.delete("error");
    setSearchParams(next, { replace: true });
  };

  return (
    <div style={{ backgroundColor: "#0B0F1A", minHeight: "100vh" }}>
      {errorMessage && <ErrorBanner message={errorMessage} onDismiss={dismissError} />}
      <Navbar />
      <Hero />
      <CodeDemo />
      <StatsBar />
      <Features />
      <HowItWorks />
      <CtaSection />
      <Footer />
    </div>
  );
}

function Hero() {
  return (
    <section className="px-6 pt-20 pb-16 md:pt-28 md:pb-24">
      <div className="max-w-[700px] mx-auto text-center flex flex-col items-center">
        <div
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm mb-6 border transition-all duration-300 hover:border-[#0ED3CF]"
          style={{ backgroundColor: "#131825", borderColor: "#1E2640", color: "#8892A8" }}
        >
          <Sparkles size={14} style={{ color: "#0ED3CF" }} />
          Multi-agent AI code review
        </div>

        <h1
          className="font-bold leading-tight mb-6"
          style={{ fontSize: "clamp(32px, 5vw, 52px)", color: "#E2E8F0" }}
        >
          Three agents. Zero blind spots.
        </h1>

        <p className="text-lg mb-10" style={{ color: "#8892A8" }}>
          CodeGuard reviews every pull request with dedicated bug, security, and quality agents —
          posting findings as inline comments before your team even looks at it.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4">
          <a
            href="/auth/login"
            className="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all duration-300 hover:opacity-90 hover:scale-105"
            style={{ backgroundColor: "#0ED3CF", color: "#0B0F1A" }}
          >
            Get started free <ArrowRight size={18} />
          </a>
          <a
            href="#demo"
            className="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold border transition-all duration-300 hover:bg-[#131825]"
            style={{ borderColor: "#1E2640", color: "#E2E8F0" }}
          >
            <Play size={18} /> Watch demo
          </a>
        </div>
      </div>
    </section>
  );
}

function accentForLine(type) {
  if (type === "security") return "#E8593C";
  if (type === "bug") return "#F2A623";
  return "transparent";
}

function CodeDemo() {
  const sectionRef = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return undefined;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section id="demo" ref={sectionRef} className="px-6 py-16 md:py-24">
      <div className="max-w-3xl mx-auto">
        <div className="rounded-xl overflow-hidden border" style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}>
          <div className="flex items-center gap-2 px-4 py-3" style={{ borderBottom: "1px solid #1E2640" }}>
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#E8593C" }} />
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#F2A623" }} />
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: "#4ADE80" }} />
            <span className="ml-3 text-xs" style={{ color: "#8892A8", fontFamily: MONO }}>
              payment_service.py
            </span>
          </div>

          <div className="p-4 md:p-6 overflow-x-auto">
            {CODE_LINES.map((line) => (
              <div key={line.num} className="flex flex-col">
                <div
                  className="flex items-start gap-4 py-0.5"
                  style={{
                    borderLeft: `3px solid ${accentForLine(line.type)}`,
                    paddingLeft: "12px",
                    backgroundColor: line.type !== "plain" ? "rgba(255,255,255,0.02)" : "transparent",
                  }}
                >
                  <span
                    className="text-xs select-none shrink-0"
                    style={{ color: "#4A5578", fontFamily: MONO, minWidth: "18px" }}
                  >
                    {line.num}
                  </span>
                  <span className="text-sm whitespace-pre" style={{ color: "#E2E8F0", fontFamily: MONO }}>
                    {line.text || " "}
                  </span>
                </div>
                {COMMENTS.filter((c) => c.line === line.num).map((comment) => (
                  <AgentComment key={comment.line} comment={comment} visible={visible} />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function AgentComment({ comment, visible }) {
  const accent = comment.type === "security" ? "#E8593C" : "#F2A623";
  const Icon = comment.type === "security" ? Shield : Bug;

  return (
    <div
      className="ml-8 my-2 p-3 rounded-lg border"
      style={{
        backgroundColor: "#0F1420",
        borderColor: accent,
        borderLeftWidth: "3px",
        opacity: visible ? 1 : 0,
        transform: visible ? "translateY(0)" : "translateY(-8px)",
        transitionProperty: "opacity, transform",
        transitionDuration: "0.5s",
        transitionTimingFunction: "ease",
        transitionDelay: visible ? `${comment.delay}ms` : "0ms",
      }}
    >
      <div className="flex items-center gap-2 mb-1">
        <Icon size={14} style={{ color: accent }} />
        <span className="text-xs font-semibold" style={{ color: accent }}>
          {comment.title}
        </span>
      </div>
      <p className="text-sm" style={{ color: "#8892A8" }}>
        {comment.message}
      </p>
    </div>
  );
}

function StatsBar() {
  return (
    <section className="px-6 py-8">
      <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4">
        {STATS.map((s) => (
          <StatCard key={s.label} icon={s.icon} value={s.value} label={s.label} />
        ))}
      </div>
    </section>
  );
}

function Features() {
  return (
    <section id="features" className="px-6 py-16 md:py-24">
      <div className="max-w-5xl mx-auto text-center mb-12">
        <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: "#E2E8F0" }}>
          Three agents, one mission
        </h2>
        <p className="text-lg" style={{ color: "#8892A8" }}>
          Each agent is laser-focused on its domain so nothing slips through.
        </p>
      </div>

      <div className="max-w-5xl mx-auto flex flex-wrap justify-center gap-6">
        {FEATURES.map((f) => {
          const Icon = f.icon;
          return (
            <div
              key={f.title}
              className="group flex-1 min-w-[260px] max-w-sm p-6 rounded-xl border transition-all duration-300 hover:-translate-y-1"
              style={{ backgroundColor: "#131825", borderColor: "#1E2640" }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = `0 0 32px ${f.accent}33`;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = "none";
              }}
            >
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-transform duration-300 group-hover:scale-110"
                style={{ backgroundColor: `${f.accent}22` }}
              >
                <Icon size={22} style={{ color: f.accent }} />
              </div>
              <h3 className="text-lg font-semibold mb-2" style={{ color: "#E2E8F0" }}>
                {f.title}
              </h3>
              <p className="text-sm" style={{ color: "#8892A8" }}>
                {f.description}
              </p>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function HowItWorks() {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActive((v) => (v + 1) % STEPS.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section id="how-it-works" className="px-6 py-16 md:py-24">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center" style={{ color: "#E2E8F0" }}>
          How it works
        </h2>

        <div className="flex flex-col gap-1">
          {STEPS.map((step, i) => {
            const isActive = i === active;
            return (
              <button
                key={step.title}
                onClick={() => setActive(i)}
                className="flex items-start gap-4 text-left py-4 px-4 rounded-lg transition-all duration-300"
                style={{
                  borderLeft: isActive ? "3px solid #0ED3CF" : "3px solid transparent",
                  backgroundColor: isActive ? "#131825" : "transparent",
                }}
              >
                <span
                  className="flex items-center justify-center w-8 h-8 rounded-full text-sm font-semibold shrink-0 transition-all duration-300"
                  style={{
                    backgroundColor: isActive ? "#0ED3CF" : "#1E2640",
                    color: isActive ? "#0B0F1A" : "#8892A8",
                  }}
                >
                  {i + 1}
                </span>
                <div>
                  <p
                    className="font-semibold transition-colors duration-300"
                    style={{ color: isActive ? "#E2E8F0" : "#8892A8" }}
                  >
                    {step.title}
                  </p>
                  <div
                    style={{
                      maxHeight: isActive ? "60px" : "0px",
                      overflow: "hidden",
                      transition: "max-height 0.3s ease",
                    }}
                  >
                    <p className="text-sm mt-1" style={{ color: "#8892A8" }}>
                      {step.description}
                    </p>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function CtaSection() {
  return (
    <section className="px-6 py-16 md:py-24">
      <div
        className="max-w-4xl mx-auto rounded-2xl border p-10 md:p-16 text-center"
        style={{
          background: "linear-gradient(135deg, #131825 0%, #0F1420 100%)",
          borderColor: "#1E2640",
        }}
      >
        <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: "#E2E8F0" }}>
          Ship cleaner code, starting now
        </h2>
        <p className="text-lg mb-8 max-w-xl mx-auto" style={{ color: "#8892A8" }}>
          Connect your GitHub repo in one click. Your next PR gets reviewed by three AI agents in
          under 30 seconds.
        </p>
        <a
          href="/auth/login"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all duration-300 hover:opacity-90 hover:scale-105"
          style={{ backgroundColor: "#0ED3CF", color: "#0B0F1A" }}
        >
          Connect GitHub <ArrowRight size={18} />
        </a>
      </div>
    </section>
  );
}
