// api/cart_ui_helpers.js
export function formatCurrency(v) {
  if (v == null) return "";
  return parseFloat(v).toFixed(2);
}

export function createProductCardHTML(product) {
  return `
    <div class="product-card">
      <img src="${product.image || ''}" alt="${product.name}" />
      <h3>${product.name}</h3>
      <p>${formatCurrency(product.base_price || product.price)} BDT</p>
      <div>
        <a href="product_detail.html?id=${product.id}">View</a>
        <button data-id="${product.id}" class="add-to-cart">Add</button>
      </div>
    </div>`;
}
