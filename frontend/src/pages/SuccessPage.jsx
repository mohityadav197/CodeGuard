import { useEffect, useRef } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

/** Lands here after the backend finishes the GitHub OAuth exchange and
 * redirects with a JWT in the query string. Kept at a distinct path from
 * /auth/callback (the real OAuth redirect_uri) so the Vite dev proxy can't
 * confuse the two -- see vite.config.js. */
export default function SuccessPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();
  const ranOnce = useRef(false);

  useEffect(() => {
    if (ranOnce.current) return;
    ranOnce.current = true;

    const token = searchParams.get("token");
    if (!token) {
      navigate("/?error=auth_failed", { replace: true });
      return;
    }

    login(token).then((user) => {
      navigate(user ? "/dashboard" : "/?error=auth_failed", { replace: true });
    });
  }, [searchParams, navigate, login]);

  return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{ backgroundColor: "#0B0F1A" }}
    >
      <div className="flex flex-col items-center gap-4">
        <Loader2 className="animate-spin" size={32} style={{ color: "#0ED3CF" }} />
        <p style={{ color: "#8892A8" }}>Logging you in...</p>
      </div>
    </div>
  );
}
