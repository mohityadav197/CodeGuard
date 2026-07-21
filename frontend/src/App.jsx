// Top-level router: wraps the app in AuthProvider and defines all page routes.
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import CallbackPage from "./pages/CallbackPage";
import SuccessPage from "./pages/SuccessPage";

function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div
        className="min-h-screen flex items-center justify-center"
        style={{ backgroundColor: "#0B0F1A" }}
      >
        <div
          className="h-8 w-8 rounded-full border-2 animate-spin"
          style={{ borderColor: "#1E2640", borderTopColor: "#0ED3CF" }}
        />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="/auth/callback" element={<CallbackPage />} />
          <Route path="/auth/success" element={<SuccessPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
