import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const getHealth = () => api.get("/health").then((res) => res.data);
export const getReviews = () => api.get("/reviews").then((res) => res.data);
export const getReview = (reviewId) => api.get(`/reviews/${reviewId}`).then((res) => res.data);
export const getStats = () => api.get("/stats").then((res) => res.data);

export default api;
