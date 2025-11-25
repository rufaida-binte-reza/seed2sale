const pages = [
  { label: "Home", href: "/" },
  { label: "Catalog", href: "/catalog/" },
  { label: "Product Detail", href: "/product-detail/" },
  { label: "Login", href: "/login/" },
  { label: "Cart / Checkout", href: "/cart-checkout/" },
  { label: "Admin Dashboard", href: "/admin-dashboard/" },
  { label: "Customer Dashboard", href: "/customer-dashboard/" },
  { label: "Inventory", href: "/inventory/" },
  { label: "Farmer Profile", href: "/farmer-profile/" },
  { label: "Driver Jobs", href: "/driver-jobs/" },
  { label: "About / Contact / FAQ", href: "/about-contact-faq/" },
];

function loadMenu() {
  const nav = document.getElementById("nav-menu");
  if (!nav) return;

  nav.innerHTML = pages
    .map(p => `<li><a href="${p.href}">${p.label}</a></li>`)
    .join("");
}

loadMenu();
