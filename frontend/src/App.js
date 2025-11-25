import React, { useState } from "react";

const pages = [
  { label: "Home", href: "/home.html" },
  { label: "Catalog", href: "/catalog.html" },
  { label: "Product Detail", href: "/product_detail.html" },
  { label: "Login", href: "/login.html" },
  { label: "Cart / Checkout", href: "/cart_checkout.html" },
  { label: "Admin Dashboard", href: "/admin_dashboard.html" },
  { label: "Customer Dashboard", href: "/customer_dashboard.html" },
  { label: "Inventory", href: "/inventory.html" },
  { label: "Farmer Profile", href: "/farmer_profile.html" },
  { label: "Driver Jobs", href: "/driver_jobs.html" },
  { label: "About / Contact / FAQ", href: "/about_contact_faq.html" },
];

export default function App() {
  const [apiResponse, setApiResponse] = useState(null);
  const BACKEND_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
  const [iframeSrc, setIframeSrc] = useState(BACKEND_BASE + "/home.html");

  const testAuthMe = async () => {
    try {
      const res = await fetch(BACKEND_BASE + "/api/auth/me/");
      const data = await res.json();
      setApiResponse({ ok: res.ok, status: res.status, body: data });
    } catch (err) {
      setApiResponse({ ok: false, error: err.message });
    }
  };

  return (
    <div style={{ padding: 0, margin: 0, fontFamily: "Inter, Arial, Helvetica, sans-serif" }}>
      <header style={{ background: "#3B7A57", color: "#fff", padding: "12px 20px", position: 'sticky', top: 0, zIndex: 50 }}>
        <div style={{ maxWidth: 1100, margin: '0 auto', display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <img src="https://res.cloudinary.com/dyjltf4tr/image/upload/v1761586959/logo_a2etx6_6ab91a.png" alt="logo" style={{ width: 40, height: 40 }} />
            <strong style={{ fontSize: 18, letterSpacing: -0.2 }}>Seed2Sale</strong>
          </div>

          <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, width: '100%', maxWidth: 700 }}>
              <select id="categorySelect" style={{ padding: '8px 10px', borderRadius: 999, border: 'none', minWidth: 140 }}>
                <option>All Categories</option>
                <option>Vegetables</option>
                <option>Fruits</option>
                <option>Dairy</option>
                <option>Fish & Meat</option>
              </select>
              <input id="searchInput" placeholder="Search produce, farmers or items (e.g. tomatoes)" style={{ flex: 1, padding: '10px 12px', borderRadius: 999, border: 'none' }} />
              <button onClick={() => setIframeSrc(BACKEND_BASE + '/catalog.html')} style={{ background: '#2f6b4b', color: '#fff', padding: '8px 12px', borderRadius: 999, border: 'none', cursor: 'pointer' }}>Search</button>
            </div>
          </div>

          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <button style={{ padding: '6px 10px', borderRadius: 8, background: 'rgba(255,255,255,0.08)', color: '#fff', border: 'none' }}>EN</button>
            <button onClick={() => setIframeSrc(BACKEND_BASE + '/login.html')} style={{ padding: '8px 12px', borderRadius: 8, background: '#A67B5B', color: '#fff', border: 'none', cursor: 'pointer' }}>Login</button>
            <button style={{ position: 'relative', padding: '8px 10px', borderRadius: 999, background: 'rgba(255,255,255,0.08)', color: '#fff', border: 'none' }} onClick={() => setIframeSrc(BACKEND_BASE + '/cart_checkout.html')}>Cart <span style={{ position: 'absolute', top: -8, right: -8, background: '#F6AD55', color: '#4a2310', width: 20, height: 20, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', borderRadius: 999, fontSize: 12 }}>2</span></button>
          </div>
        </div>
      </header>

      <nav style={{ marginBottom: 24, maxWidth: 1100, marginLeft: 'auto', marginRight: 'auto', paddingTop: 12 }}>
        <ul style={{ listStyle: "none", padding: 0, display: "flex", flexWrap: "wrap", gap: 12 }}>
          {pages.map((p) => (
            <li key={p.href} style={{ display: 'flex', alignItems: 'center' }}>
              <button onClick={() => setIframeSrc(BACKEND_BASE + p.href)} style={{ textDecoration: "none", padding: "8px 12px", background: iframeSrc === BACKEND_BASE + p.href ? "#e6f4ea" : "#f3f3f3", borderRadius: 6, color: "#333", border:'none', cursor:'pointer' }}>
                {p.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      <section style={{ marginBottom: 24 }}>
        <h2 style={{ maxWidth: 1100, margin: '0 auto 8px' }}>API test</h2>
        <div style={{ maxWidth: 1100, margin: '0 auto' }}>
          <p>This checks GET <code>/api/auth/me/</code> on the backend without credentials (should return 401).</p>
          <button onClick={testAuthMe} style={{ padding: "8px 12px", cursor: "pointer" }}>Test /api/auth/me</button>
          {apiResponse && (
            <pre style={{ background: "#f9f9f9", padding: 12, marginTop: 12 }}>{JSON.stringify(apiResponse, null, 2)}</pre>
          )}
        </div>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2 style={{ maxWidth: 1100, margin: '0 auto 8px' }}>Preview</h2>
        <div style={{ maxWidth: 1100, margin: '0 auto', border: '1px solid #e6e6e6', borderRadius: 6, overflow: 'hidden', height: '70vh' }}>
          <iframe title="seed2sale-preview" src={iframeSrc} style={{ width: '100%', height: '100%', border: 'none' }} />
        </div>
      </section>

      <footer style={{ marginTop: 40, textAlign: "center", color: "#888" }}>
        <small>Dev helper: Links open in a new tab. If pages are not available on your dev server, open the HTML files directly from <code>frontend/</code>.</small>
      </footer>
    </div>
  );
}
/* <app>/static/js/app.js  – optional polish, NOT a router */
(() => {
  // 1. Highlight current nav link
  const current = location.pathname;
  document.querySelectorAll('nav a').forEach(a => {
    if (a.getAttribute('href') === current) {
      a.classList.add('active');
    }
  });

  // 2. Auto CSRF token for fetch() posts
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
                 || document.cookie
                     .split('; ')
                     .find(row => row.startsWith('csrftoken='))
                     ?.split('=')[1];

  const safeMethods = ['GET', 'HEAD', 'OPTIONS', 'TRACE'];
  if (csrftoken) {
    document.addEventListener('submit', e => {
      const form = e.target;
      if (form.method && !safeMethods.includes(form.method.toUpperCase())) {
        if (!form.querySelector('[name=csrfmiddlewaretoken]')) {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = 'csrfmiddlewaretoken';
          input.value = csrftoken;
          form.appendChild(input);
        }
      }
    });
  }

  // 3. Small utility: flash-message fade
  const flash = document.querySelector('.flash');
  if (flash) {
    setTimeout(() => flash.classList.add('fade-out'), 3000);
  }
})();