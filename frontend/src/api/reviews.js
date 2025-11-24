// frontend/src/api/reviews.js
import { apiFetch } from "./api.js";

async function listProductReviews(productId) {
  return apiFetch(`/products/${productId}/reviews/`);
}

async function createProductReview(productId, { rating, comment }) {
  return apiFetch(`/products/${productId}/reviews/`, { method: "POST", body: { rating, comment }});
}

export { listProductReviews, createProductReview };
