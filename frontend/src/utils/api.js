// Axios instance with an auth-token interceptor and wrapper functions for
// every backend endpoint the frontend calls.
import axios from "axios";

const TOKEN_KEY = "codeguard_token";

// In dev, the Vite proxy (see vite.config.js) forwards /api, /auth, and
// /webhook to the backend, so an empty baseURL works. In production (e.g.
// Vercel), the frontend and backend are on different origins, so
// VITE_API_URL must point at the deployed backend.
const BASE_URL = import.meta.env.VITE_API_URL || "";
const api = axios.create({
  baseURL: BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getMe = () => api.get("/auth/me").then((res) => res.data);

export const getReviews = (params = {}) =>
  api.get("/api/reviews", { params }).then((res) => res.data);

export const getReview = (id) => api.get(`/api/reviews/${id}`).then((res) => res.data);

export const getStats = () => api.get("/api/stats").then((res) => res.data);

export const getRepos = () => api.get("/api/repos").then((res) => res.data);

export default api;
