// Defensive fallback handler for /auth/callback in case it ever receives a
// token directly; SuccessPage is the primary post-OAuth handler.
import { useEffect, useRef } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

// The real OAuth redirect_uri (backend -> GitHub -> here) never carries a
// token -- the backend now redirects the token-bearing hop to /auth/success
// instead (see vite.config.js / backend/auth/routes.py for why). This route
// stays registered as a defensive fallback in case anything ever lands here
// with a token directly, using the same success/failure handling as
// SuccessPage.
export default function CallbackPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuth();
  const ranOnce = useRef(false);

  useEffect(() => {
    if (ranOnce.current) return;
    ranOnce.current = true;

    const token = searchParams.get("token");
    if (!token) {
      navigate("/", { replace: true });
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
