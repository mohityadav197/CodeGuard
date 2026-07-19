import { useEffect, useRef } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

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

    login(token).then(() => navigate("/dashboard", { replace: true }));
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
