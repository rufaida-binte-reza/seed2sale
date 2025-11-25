// frontend/src/api/auth.js
import { apiFetch, setAuthToken } from "./api.js";

async function login(emailOrPhone, password) {
  // Prefer the project token endpoint: POST /api/token/ (returns { access, refresh }).
  const path = "/token/"; // will be prefixed by /api by apiFetch
  try {
    const data = await apiFetch(path, {
      method: "POST",
      auth: false,
      // simplejwt TokenObtainPairView expects 'username' and 'password' (or 'email').
      // If using a custom accounts EmailOrPhoneTokenObtainView it may accept 'identifier' instead.
      body: { identifier: emailOrPhone, password }
    });
    // simplejwt returns { access, refresh }.
    if (data && data.access) {
      setAuthToken(data.access);
    }
    return data;
  } catch (err) {
    throw err;
  }
}

async function register(payload) {
  // payload: { email, full_name, password, ... } - change keys to what your backend expects.
  const path = "/accounts/register/"; // if accounts registered under /api/accounts/
  return apiFetch(path, { method: "POST", auth: false, body: payload });
}

function logout() {
  setAuthToken(null);
  // optionally call backend logout endpoint here
}

export { login, register, logout };
