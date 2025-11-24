// frontend/src/api/cart.js
import { apiFetch } from "./api.js";

/**
 * Endpoints used (from your router names):
 *  - GET /api/cart/           -> list user's carts (or user's single cart)
 *  - POST /api/cart/          -> create cart (not typically used)
 *  - GET /api/cart-items/     -> list items
 *  - POST /api/cart-items/    -> add item (payload expects product_id, quantity, unit_price)
 *  - PATCH /api/cart-items/<id>/  -> update quantity
 *  - DELETE /api/cart-items/<id>/ -> remove
 */

async function getMyCart() {
  return apiFetch("/cart/"); // might return list or single object; handle both in calling code
}

async function getCartItems() {
  return apiFetch("/cart-items/");
}

async function addToCart({ product_id, quantity = 1, unit_price = null }) {
  // payload keys follow your CartItem serializer: product_id maps to product FK
  const payload = { product_id, quantity };
  if (unit_price !== null) payload.unit_price = unit_price;
  return apiFetch("/cart-items/", { method: "POST", body: payload });
}

async function updateCartItem(id, { quantity }) {
  return apiFetch(`/cart-items/${id}/`, { method: "PATCH", body: { quantity } });
}

async function removeCartItem(id) {
  return apiFetch(`/cart-items/${id}/`, { method: "DELETE" });
}

export { getMyCart, getCartItems, addToCart, updateCartItem, removeCartItem };
