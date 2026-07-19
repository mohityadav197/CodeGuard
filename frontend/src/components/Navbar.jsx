import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogOut, Menu, Shield, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";

/** Shared navbar for Landing and Dashboard. Adapts its right-hand side to
 * auth state: "Connect GitHub" when signed out, avatar + logout when in.
 * Pass showLinks={false} on pages without the marketing anchor sections
 * (e.g. the dashboard). */
export default function Navbar({ showLinks = true }) {
  const { isAuthenticated, user, logout } = useAuth();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav
      className="sticky top-0 z-50 transition-all duration-300"
      style={{
        backgroundColor: scrolled ? "rgba(11, 15, 26, 0.75)" : "transparent",
        backdropFilter: scrolled ? "blur(12px)" : "none",
        WebkitBackdropFilter: scrolled ? "blur(12px)" : "none",
        borderBottom: scrolled ? "1px solid #1E2640" : "1px solid transparent",
      }}
    >
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link
          to="/"
          className="flex items-center gap-2 font-bold text-lg transition-opacity duration-300 hover:opacity-80"
          style={{ color: "#E2E8F0" }}
        >
          <Shield size={22} style={{ color: "#0ED3CF" }} />
          CodeGuard
        </Link>

        {showLinks && (
          <div className="hidden md:flex items-center gap-8 text-sm">
            <a
              href="#features"
              className="transition-colors duration-300 hover:text-[#E2E8F0]"
              style={{ color: "#8892A8" }}
            >
              Features
            </a>
            <a
              href="#how-it-works"
              className="transition-colors duration-300 hover:text-[#E2E8F0]"
              style={{ color: "#8892A8" }}
            >
              How it works
            </a>
          </div>
        )}

        <div className="hidden md:flex items-center gap-4">
          {isAuthenticated ? (
            <>
              {user?.github_avatar_url && (
                <img
                  src={user.github_avatar_url}
                  alt={user.github_username}
                  className="w-8 h-8 rounded-full"
                  style={{ border: "1px solid #1E2640" }}
                />
              )}
              <span className="text-sm" style={{ color: "#E2E8F0" }}>
                {user?.github_username}
              </span>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 text-sm px-3 py-1.5 rounded-lg transition-all duration-300 hover:bg-[#1A2035]"
                style={{ color: "#8892A8" }}
              >
                <LogOut size={16} /> Logout
              </button>
            </>
          ) : (
            <a
              href="/auth/login"
              className="px-4 py-2 rounded-lg font-medium text-sm transition-all duration-300 hover:opacity-90"
              style={{ backgroundColor: "#0ED3CF", color: "#0B0F1A" }}
            >
              Connect GitHub
            </a>
          )}
        </div>

        <button
          className="md:hidden transition-colors duration-300"
          onClick={() => setMobileOpen((v) => !v)}
          style={{ color: "#E2E8F0" }}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {mobileOpen && (
        <div
          className="md:hidden px-6 pb-5 flex flex-col gap-4"
          style={{ borderTop: "1px solid #1E2640" }}
        >
          {showLinks && (
            <>
              <a
                href="#features"
                onClick={() => setMobileOpen(false)}
                className="pt-4 transition-colors duration-300 hover:text-[#E2E8F0]"
                style={{ color: "#8892A8" }}
              >
                Features
              </a>
              <a
                href="#how-it-works"
                onClick={() => setMobileOpen(false)}
                className="transition-colors duration-300 hover:text-[#E2E8F0]"
                style={{ color: "#8892A8" }}
              >
                How it works
              </a>
            </>
          )}
          {isAuthenticated ? (
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 transition-colors duration-300 hover:text-[#E2E8F0]"
              style={{ color: "#8892A8" }}
            >
              <LogOut size={16} /> Logout
            </button>
          ) : (
            <a
              href="/auth/login"
              className="px-4 py-2 rounded-lg font-medium text-sm text-center transition-all duration-300 hover:opacity-90"
              style={{ backgroundColor: "#0ED3CF", color: "#0B0F1A" }}
            >
              Connect GitHub
            </a>
          )}
        </div>
      )}
    </nav>
  );
}
