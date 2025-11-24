// frontend/src/api/wishlist.js
import { apiFetch } from "./api.js";

async function getWishlist() {
  return apiFetch("/wishlist/");
}

async function addToWishlist(product_id) {
  // some serializers accept { product: id } or { product_id: id } - try both patterns
  try {
    return await apiFetch("/wishlist/", { method: "POST", body: { product_id }});
  } catch (err) {
    // fallback
    return apiFetch("/wishlist/", { method: "POST", body: { product: product_id }});
  }
}

async function removeWishlist(id) {
  return apiFetch(`/wishlist/${id}/`, { method: "DELETE" });
}

export { getWishlist, addToWishlist, removeWishlist };
