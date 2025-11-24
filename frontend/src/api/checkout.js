import { fetchJson } from "./api.js";

export async function processPayment(orderData) {
  return await fetchJson(`/api/payment/`, {
    method: "POST",
    body: orderData,
  });
}
