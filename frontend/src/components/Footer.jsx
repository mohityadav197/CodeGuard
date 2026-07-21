// Shared site footer with branding and external links.
import { Github } from "lucide-react";

export default function Footer() {
  return (
    <footer style={{ borderTop: "1px solid #1E2640" }}>
      <div className="max-w-6xl mx-auto px-6 py-10 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="text-center md:text-left">
          <p className="font-bold text-lg" style={{ color: "#E2E8F0" }}>
            Code<span style={{ color: "#0ED3CF" }}>Guard</span>
          </p>
          <p className="text-sm mt-1" style={{ color: "#8892A8" }}>
            Built with LangGraph + Groq
          </p>
        </div>
        <div className="flex items-center gap-6 text-sm">
          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 transition-colors duration-300 hover:text-[#E2E8F0]"
            style={{ color: "#8892A8" }}
          >
            <Github size={16} /> GitHub
          </a>
          <a
            href="#"
            className="transition-colors duration-300 hover:text-[#E2E8F0]"
            style={{ color: "#8892A8" }}
          >
            Docs
          </a>
          <a
            href="#"
            className="transition-colors duration-300 hover:text-[#E2E8F0]"
            style={{ color: "#8892A8" }}
          >
            Blog
          </a>
        </div>
      </div>
    </footer>
  );
}
