// frontend/src/api/payment.js
import { apiFetch } from "./api.js";

/**
 * Use POST /api/payment/ or /api/orders/ depending on what your backend expects.
 * Here we use /api/payment/ (registered in router earlier).
 */
async function createPayment(payload) {
  // payload example:
  // { amount: 1000, method: 'card', order_data: {...}, address_id: 2 }
  return apiFetch("/payment/", { method: "POST", body: payload });
}

export { createPayment };
