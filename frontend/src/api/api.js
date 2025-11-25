// frontend/src/api/api.js
// Central fetch helpers and configuration.

const API_BASE = window.API_BASE || "http://127.0.0.1:8000"; // change if needed
const API_PREFIX = API_BASE.replace(/\/$/, "") + "/api";     // e.g. http://127.0.0.1:8000/api

function getAuthToken() {
  return localStorage.getItem("s2s_token") || null;
}

function setAuthToken(token) {
  if (token) localStorage.setItem("s2s_token", token);
  else localStorage.removeItem("s2s_token");
}

async function apiFetch(path, { method = "GET", body = null, auth = true, headers = {}, params = null } = {}) {
  let url = path.startsWith("http") ? path : `${API_PREFIX}${path.startsWith("/") ? path : "/" + path}`;

  if (params && typeof params === "object") {
    const query = new URLSearchParams(params).toString();
    if (query) url += (url.includes("?") ? "&" : "?") + query;
  }

  const baseHeaders = { "Accept": "application/json" };
  if (!(body instanceof FormData)) baseHeaders["Content-Type"] = "application/json";

  const token = getAuthToken();
  // Backend expects a JWT Bearer token (simplejwt). Use `Bearer <token>`.
  if (auth && token) baseHeaders["Authorization"] = `Bearer ${token}`;

  const resp = await fetch(url, {
    method,
    headers: { ...baseHeaders, ...headers },
    body: body && !(body instanceof FormData) ? JSON.stringify(body) : body,
  });

  const text = await resp.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = text; }

  if (!resp.ok) {
    // Provide detailed error
    const err = new Error(`HTTP ${resp.status}`);
    err.status = resp.status;
    err.data = data;
    throw err;
  }
  return data;
}

export { API_BASE, API_PREFIX, apiFetch, getAuthToken, setAuthToken };
