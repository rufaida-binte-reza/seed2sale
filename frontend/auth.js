const API = 'http://localhost:8000/api';

async function login(email, password) {
  const res = await fetch(`${API}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) throw new Error('Invalid credentials');
  const data = await res.json();
  localStorage.setItem('s2s_token', data.access);
  window.location = 'catalog.html';
}

function logout() {
  localStorage.removeItem('s2s_token');
  window.location = 'login.html';
}

function authedFetch(url, options = {}) {
  const token = localStorage.getItem('s2s_token');
  if (!token) { window.location = 'login.html'; return; }
  options.headers ||= {};
  options.headers.Authorization = `Bearer ${token}`;
  return fetch(url, options);
}

export { login, logout, authedFetch };