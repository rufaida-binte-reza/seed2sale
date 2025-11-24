// frontend/src/api/products.js
import { apiFetch } from "./api.js";

/**
 * Endpoints used:
 *  - GET /api/products/           -> list & filter
 *  - GET /api/products/<id>/      -> detail
 *  - GET /api/categories/         -> categories (if available)
 *  - GET /api/products/<id>/reviews/ -> product-specific reviews
 *
 * Adjust endpoints if your products app uses different paths.
 */

async function fetchCategories() {
  try {
    return await apiFetch("/categories/"); // or "/categories" depending on trailing slash config
  } catch (err) {
    // fallback: try /api/products/categories if your project nests categories
    try {
      return await apiFetch("/products/categories/");
    } catch (e) {
      console.warn("categories endpoint not found", e);
      return [];
    }
  }
}

async function fetchProducts(params = {}) {
  // params example: { page: 1, category: 2, search: 'apple' }
  return apiFetch("/products/", { params });
}

async function fetchProduct(id) {
  return apiFetch(`/products/${id}/`);
}

async function fetchProductReviews(productId) {
  return apiFetch(`/products/${productId}/reviews/`);
}

/* Render helpers - adapt DOM selectors to match your HTML */
function renderProductCard(product, containerEl) {
  // product: { id, name, slug, price, category, description, image_url, ...}
  const div = document.createElement("div");
  div.className = "product-card p-4 bg-white rounded shadow";
  div.innerHTML = `
    <a href="/product_detail.html?product=${product.id}">
      <img src="${product.image || product.image_url || '/static/img/placeholder.png'}" alt="${product.name}" class="w-full h-48 object-cover"/>
      <h3 class="mt-2 font-semibold">${product.name}</h3>
      <div class="mt-1 text-lg font-bold">${product.price ? '৳' + product.price : ''}</div>
    </a>
    <div class="mt-2 flex gap-2">
      <button data-product="${product.id}" class="add-to-cart btn">Add to cart</button>
      <button data-product="${product.id}" class="wishlist-btn btn-ghost">♡</button>
    </div>
  `;
  containerEl.appendChild(div);
}

export { fetchProducts, fetchProduct, fetchCategories, fetchProductReviews, renderProductCard };
