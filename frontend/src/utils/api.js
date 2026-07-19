import axios from "axios";

const TOKEN_KEY = "codeguard_token";

// baseURL is intentionally empty -- the Vite dev server proxies /api, /auth,
// and /webhook to the backend (see vite.config.js), and in production this
// is served from the same origin as the API.
const api = axios.create({
  baseURL: "",
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
