// frontend/src/api/addresses.js
import { apiFetch } from "./api.js";

async function getAddresses() { return apiFetch("/addresses/"); }
async function createAddress(payload) { return apiFetch("/addresses/", { method: "POST", body: payload }); }
async function updateAddress(id, payload) { return apiFetch(`/addresses/${id}/`, { method: "PATCH", body: payload }); }
async function deleteAddress(id) { return apiFetch(`/addresses/${id}/`, { method: "DELETE" }); }

export { getAddresses, createAddress, updateAddress, deleteAddress };
