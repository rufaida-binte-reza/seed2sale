// frontend/src/js/home.js
// Module to power home.html with real API calls to your Django backend.
// Assumptions:
// - API base at /api/
// - Auth token (if used) stored at localStorage.s2s_token (Bearer JWT).
// - Endpoints used: /api/products/, /api/cart/, /api/cart-items/, /api/wishlist/, /api/reviews/, /api/categories/ (best-effort).
// - If backend uses session auth, browser cookies will be used automatically (fetch includes credentials).
// - To use token auth, set localStorage.s2s_token = "<your token>" in console.

const BASE = '/api';
const DEFAULT_HEADERS = () => {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('s2s_token');
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
};

// Utility: fetch wrapper with error handling
async function apiFetch(path, opts = {}) {
  const url = `${BASE}${path}`;
  const defaultOpts = { headers: DEFAULT_HEADERS(), credentials: 'include' }; // include cookies for session auth
  const merged = { ...defaultOpts, ...opts };

  // If opts.body is a plain object and Content-Type is application/json, stringify
  if (merged.body && typeof merged.body === 'object' && !(merged.body instanceof FormData)) {
    merged.body = JSON.stringify(merged.body);
  }

  const res = await fetch(url, merged);
  const contentType = res.headers.get('content-type') || '';
  let data = null;
  if (contentType.includes('application/json')) data = await res.json();
  else data = await res.text();

  if (!res.ok) {
    const err = new Error(`API ${res.status} ${res.statusText}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}


/* -------------------------
   DOM references & helpers
   ------------------------- */
const productGrid = document.getElementById('productGrid');
const tpl = document.getElementById('productTemplate');
const shownCount = document.getElementById('shownCount');
const loadMoreBtn = document.getElementById('loadMore');

const searchInput = document.getElementById('searchInput');
const categorySelect = document.getElementById('categorySelect');
const searchBtn = document.getElementById('searchBtn');

const mobileMenu = document.getElementById('mobileMenu');
const mobileToggle = document.getElementById('mobileToggle');
const searchInputMobile = document.getElementById('searchInputMobile');
const categorySelectMobile = document.getElementById('categorySelectMobile');
const searchBtnMobile = document.getElementById('searchBtnMobile');

const cartToggle = document.getElementById('cartToggle');
const cartDropdown = document.getElementById('cartDropdown');
const cartCount = document.getElementById('cartCount');

if (!productGrid || !tpl) {
  console.warn('home.js could not find #productGrid or #productTemplate — ensure script included on home page.');
}

/* -------------------------
   State
   ------------------------- */
let allProducts = []; // full list from server (page 1 or all depending on API)
let currentProducts = []; // filtered / displayed
let nextPageUrl = null; // optional pagination support

/* -------------------------
   Render helpers
   ------------------------- */

function formatPrice(p) {
  if (p === null || p === undefined) return '৳—';
  // assume integer or number
  return `৳${p}`;
}

// render product list from a list of product objects
function renderProducts(list) {
  if (!productGrid || !tpl) return;
  productGrid.innerHTML = '';
  list.forEach((p) => {
    const el = tpl.content.cloneNode(true);
    const img = el.querySelector('img');
    const title = el.querySelector('h4');
    const meta = el.querySelector('p');
    const priceEl = el.querySelector('.text-amber-600');

    img.src = p.image || p.thumbnail || p.photo || p.img || '/static/img/product-fallback.jpg';
    img.alt = p.name || 'Product';

    title.textContent = p.name || 'Unnamed product';
    // farmer & category
    const farmerName = (p.farmer && (p.farmer.full_name || p.farmer.email)) || (p.seller && p.seller.name) || 'Farmer';
    const catName = (p.category && (p.category.name || p.category)) || (p.category_slug || 'General');
    meta.textContent = `${farmerName} • ${catName}`;

    // price display: product may have price field
    priceEl.textContent = (p.price !== undefined && p.price !== null) ? `${formatPrice(p.price)}` : (p.display_price || '৳—');

    // hook up Add to cart & quick actions (use dataset product-id)
    const addBtn = el.querySelectorAll('button')[1]; // second button is add-to-cart by template order
    if (addBtn) {
      addBtn.setAttribute('aria-label', `Add ${p.name} to cart`);
      addBtn.addEventListener('click', (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        addToCart(p.id || p.pk || p.product_id, 1)
          .then(() => {
            showToast(`${p.name} added to cart`);
            refreshCartCount();
          })
          .catch(err => {
            console.error('Add to cart error', err);
            if (err.status === 401) showAuthRequired();
            else showToast('Could not add to cart');
          });
      });
    }

    // clicking card goes to product detail
    const article = el.querySelector('article');
    if (article) {
      article.style.cursor = 'pointer';
      article.addEventListener('click', () => {
        const pid = p.id || p.pk || p.product_id;
        if (!pid) return;
        // route to product page (you should create product.html)
        window.location.href = `/product.html?id=${pid}`;
      });
    }

    productGrid.appendChild(el);
  });

  shownCount.textContent = list.length;
}

/* -------------------------
   UI small helpers
   ------------------------- */

function showToast(msg, timeout = 2500) {
  // simple toast
  const t = document.createElement('div');
  t.textContent = msg;
  t.className = 'fixed bottom-6 right-6 bg-black/80 text-white px-4 py-2 rounded shadow';
  document.body.appendChild(t);
  setTimeout(() => t.remove(), timeout);
}

function showAuthRequired() {
  showToast('Please login to perform that action');
  // optionally redirect to login page
  // window.location.href = '/login.html';
}

/* -------------------------
   API actions
   ------------------------- */

async function fetchProducts(force = false) {
  // try to fetch categories/products from backend.
  // If server supports pagination, adapt to nextPageUrl
  if (allProducts.length && !force) return allProducts;

  try {
    // fetch first page of products
    const data = await apiFetch('/products/'); // expects /api/products/
    // data might be {results: [...], next: '...', count: ...} or a plain array
    let results = [];
    if (Array.isArray(data)) results = data;
    else if (data.results) {
      results = data.results;
      nextPageUrl = data.next || null;
    } else {
      // some custom shape
      results = data;
    }
    allProducts = results;
    currentProducts = [...allProducts];
    return allProducts;
  } catch (err) {
    console.error('Could not fetch products', err);
    showToast('Unable to fetch products from server');
    // fallback: keep current mock or empty
    return [];
  }
}

async function fetchCategories() {
  try {
    const cats = await apiFetch('/categories/'); // try /api/categories/
    if (Array.isArray(cats)) return cats;
    if (cats.results) return cats.results;
    return [];
  } catch (err) {
    console.warn('categories fetch failed, will derive from products', err);
    // derive categories from products
    const derived = [...new Map(allProducts.map(p => [(p.category && p.category.name) || p.category, (p.category && p.category.name) || p.category])).values()];
    return derived.filter(Boolean);
  }
}

async function getCart() {
  try {
    const carts = await apiFetch('/cart/'); // GET /api/cart/
    // router might return array; pick first for logged in user
    if (Array.isArray(carts)) return carts[0] || null;
    return carts;
  } catch (err) {
    console.warn('getCart error', err);
    return null;
  }
}

async function refreshCartCount() {
  try {
    const cart = await getCart();
    let count = 0;
    if (cart) {
      // if cart has items relation
      if (Array.isArray(cart.items)) count = cart.items.reduce((s,i) => s + (i.quantity || 0), 0);
      else if (typeof cart.total_items === 'number') count = cart.total_items;
      else if (cart.count) count = cart.count;
    }
    cartCount.textContent = count;
  } catch (err) {
    console.warn('refreshCartCount', err);
    cartCount.textContent = '0';
  }
}

async function addToCart(productId, quantity = 1) {
  if (!productId) throw new Error('Missing product id');
  // CartItem serializer on backend expects "product_id" (write_only -> source 'product')
  const body = { product_id: productId, quantity };
  return apiFetch('/cart-items/', { method: 'POST', body });
}

/* -------------------------
   Search & filters
   ------------------------- */
function applyFilter({ category = 'all', q = '' } = {}) {
  let list = [...allProducts];
  if (category && category !== 'all') {
    // handle categories that might be slug or name
    list = list.filter(p => {
      const cat = p.category && (p.category.name || p.category);
      const slug = p.category && p.category.slug;
      return (String(cat || '').toLowerCase() === String(category).toLowerCase()) || (String(slug || '').toLowerCase() === String(category).toLowerCase()) || (String(p.category_slug || '').toLowerCase() === String(category).toLowerCase());
    });
  }
  if (q) {
    const qq = q.toLowerCase();
    list = list.filter(p => (p.name || '').toLowerCase().includes(qq) || (p.description || '').toLowerCase().includes(qq));
  }
  currentProducts = list;
  renderProducts(list);
}

/* -------------------------
   Init logic
   ------------------------- */

async function init() {
  // setup small UI toggles (mobile menu & cart dropdown)
  if (mobileToggle) mobileToggle.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
  if (cartToggle) cartToggle.addEventListener('click', (e) => { e.stopPropagation(); cartDropdown.classList.toggle('hidden'); });
  if (cartDropdown) cartDropdown.addEventListener('click', (e) => e.stopPropagation());
  document.addEventListener('click', () => cartDropdown.classList.add('hidden'));

  // wire search buttons
  if (searchBtn) searchBtn.addEventListener('click', () => applyFilter({ category: categorySelect.value, q: searchInput.value }));
  if (searchBtnMobile) searchBtnMobile.addEventListener('click', () => {
    applyFilter({ category: categorySelectMobile.value, q: searchInputMobile.value });
    mobileMenu.classList.add('hidden');
  });

  // enter key to search
  if (searchInput) searchInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') searchBtn.click(); });
  if (searchInputMobile) searchInputMobile.addEventListener('keydown', (e) => { if (e.key === 'Enter') searchBtnMobile.click(); });

  // load initial data
  await fetchProducts(true);
  renderProducts(allProducts.slice(0, 12)); // show first 12 for speed
  shownCount.textContent = Math.min(allProducts.length, 12);

  // load categories into selects (best-effort)
  const categories = await fetchCategories();
  populateCategorySelects(categories);

  // wire load more
  if (loadMoreBtn) loadMoreBtn.addEventListener('click', () => {
    // if nextPageUrl present, attempt paginated fetch (not implemented here - backend should return next)
    if (nextPageUrl) {
      // naive: fetch next page via full url
      fetch(nextPageUrl).then(r => r.json()).then(d => {
        const more = d.results || d;
        allProducts = allProducts.concat(more);
        renderProducts(allProducts);
      }).catch(()=> showToast('Could not load more'));
    } else {
      // simply show all for now
      renderProducts(allProducts);
    }
  });

  await refreshCartCount();
}

function populateCategorySelects(categories) {
  function toOption(c) {
    if (typeof c === 'string') return { value: c.toLowerCase(), label: c };
    return { value: (c.slug || c.name || c).toLowerCase(), label: c.name || c };
  }
  const opts = [{value: 'all', label: 'All Categories'}, ...(Array.isArray(categories) ? categories.map(toOption) : [])];

  // desktop
  if (categorySelect) {
    categorySelect.innerHTML = '';
    opts.forEach(o => {
      const op = document.createElement('option');
      op.value = o.value;
      op.textContent = o.label;
      categorySelect.appendChild(op);
    });
  }
  // mobile
  if (categorySelectMobile) {
    categorySelectMobile.innerHTML = '';
    opts.forEach(o => {
      const op = document.createElement('option');
      op.value = o.value;
      op.textContent = o.label;
      categorySelectMobile.appendChild(op);
    });
  }
}

/* -------------------------
   Kick off
   ------------------------- */

document.addEventListener('DOMContentLoaded', () => {
  init().catch(err => {
    console.error('init error', err);
    showToast('Initialization error (open console)');
  });
});

// Expose some helpers to window for quick debugging in dev console
window.seed2sale = {
  fetchProducts,
  allProducts,
  addToCart,
  getCart,
  refreshCartCount,
  apiFetch
};
