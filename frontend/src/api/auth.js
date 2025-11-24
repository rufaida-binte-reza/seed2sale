// frontend/src/api/auth.js
import { apiFetch, setAuthToken } from "./api.js";

async function login(emailOrPhone, password) {
  // Adapt endpoint if your accounts app exposes a specific endpoint.
  // Many projects use /accounts/token/ or /api/auth/login/. Try /accounts/login/ first.
  const path = "/accounts/login/"; // if your backend uses different, change here
  try {
    const data = await apiFetch(path, {
      method: "POST",
      auth: false,
      body: { email: emailOrPhone, password }
    });
    // expected response includes token (adjust field name if different)
    if (data && (data.token || data.key)) {
      const token = data.token || data.key;
      setAuthToken(token);
      return data;
    }
    return data;
  } catch (err) {
    throw err;
  }
}

async function register(payload) {
  // payload: { email, full_name, password, ... } - change keys to what your backend expects.
  const path = "/accounts/register/";
  return apiFetch(path, { method: "POST", auth: false, body: payload });
}

function logout() {
  setAuthToken(null);
  // optionally call backend logout endpoint here
}

export { login, register, logout };
