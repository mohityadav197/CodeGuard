// React context providing auth state (user, isAuthenticated) plus login()/logout() actions.
import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { getMe } from "../utils/api";

const TOKEN_KEY = "codeguard_token";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchUser = useCallback(async () => {
    try {
      const data = await getMe();
      setUser(data);
      return data;
    } catch {
      localStorage.removeItem(TOKEN_KEY);
      setUser(null);
      return null;
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      setIsLoading(false);
      return;
    }
    fetchUser().finally(() => setIsLoading(false));
  }, [fetchUser]);

  // Called by CallbackPage right after OAuth redirects back with a token --
  // stores it, then re-checks auth so isAuthenticated is correct *before*
  // navigating to /dashboard (avoids a race where the protected route
  // bounces back to "/" because the initial mount-time check ran first).
  const login = useCallback(
    async (token) => {
      localStorage.setItem(TOKEN_KEY, token);
      setIsLoading(true);
      const data = await fetchUser();
      setIsLoading(false);
      return data;
    },
    [fetchUser]
  );

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
  }, []);

  const value = {
    user,
    isLoading,
    isAuthenticated: Boolean(user),
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return ctx;
}
