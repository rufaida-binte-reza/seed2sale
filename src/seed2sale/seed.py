import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seed2sale.settings")
django.setup()

from accounts.models import User, Address, FarmerProfile
from products.models import Category, Product, Review, Wishlist
from cart.models import Cart, CartItem

print("📌 Seeding database...")


# -------------------------
# USERS
# -------------------------
def seed_users():
    print("👤 Seeding Users...")

    sample_users = [
        {"email": "john@example.com", "full_name": "John Doe", "password": "pass123", "is_customer": True},
        {"email": "sara@example.com", "full_name": "Sara Ali", "password": "pass123", "is_customer": True},
        {"email": "farmer1@example.com", "full_name": "Farmer One", "password": "pass123", "is_farmer": True},
        {"email": "farmer2@example.com", "full_name": "Farmer Two", "password": "pass123", "is_farmer": True},
    ]

    created_users = []

    for u in sample_users:
        user, created = User.objects.get_or_create(
            email=u["email"],
            defaults={
                "full_name": u["full_name"],
                "is_customer": u.get("is_customer", False),
                "is_farmer": u.get("is_farmer", False),
            },
        )

        if created:
            user.set_password(u["password"])
            user.save()

        created_users.append(user)

    print("✔ Users done")
    return created_users


# -------------------------
# ADDRESSES
# -------------------------
def seed_addresses(users):
    print("🏠 Seeding Addresses...")

    for user in users:
        Address.objects.get_or_create(
            user=user,
            full_name=user.full_name,
            phone="0123456789",
            address_line="Sample Address Line",
            city="Dhaka",
            postal_code="1200",
            is_default=True,
        )

    print("✔ Addresses done")


# -------------------------
# FARMER PROFILES
# -------------------------
def seed_farmer_profiles(users):
    print("🚜 Seeding Farmer Profiles...")

    for user in users:
        if user.is_farmer:
            FarmerProfile.objects.get_or_create(
                user=user,
                defaults={
                    "farm_name": f"{user.full_name} Farm",
                    "farm_location": "Rangpur",
                    "farm_size": random.randint(5, 50),
                    "bio": "Experienced farmer producing organic food.",
                },
            )

    print("✔ Farmer Profiles done")


# -------------------------
# CATEGORY
# -------------------------
def seed_categories():
    print("📦 Seeding Categories...")

    names = ["Electronics", "Fashion", "Grocery", "Fruits", "Vegetables"]

    categories = []
    for name in names:
        cat, _ = Category.objects.get_or_create(
            name=name,
            defaults={"slug": slugify(name)}
        )
        categories.append(cat)

    print("✔ Categories done")
    return categories


# -------------------------
# PRODUCTS
# -------------------------
def seed_products(categories):
    print("🛒 Seeding Products...")

    # Get farmer users only
    farmers = User.objects.filter(is_farmer=True)

    if not farmers.exists():
        raise Exception("❌ No farmers found! Unable to seed products because farmer_id is required.")

    products = []

    for cat in categories:
        for i in range(3):
            name = f"{cat.name} Product {i+1}"

            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    "slug": slugify(name),
                    "category": cat,
                    "price": random.randint(100, 500),
                    "stock": random.randint(5, 50),
                    "description": f"This is a sample product under {cat.name} category.",
                    "farmer": random.choice(farmers),  # 🔥 FIXED
                },
            )

            products.append(product)

    print("✔ Products done")
    return products



# -------------------------
# REVIEWS
# -------------------------
def seed_reviews(users, products):
    print("⭐ Seeding Reviews...")

    for user in users:
        for product in random.sample(products, 2):
            Review.objects.get_or_create(
                user=user,
                product=product,
                defaults={
                    "rating": random.randint(3, 5),
                    "comment": "Great product!",
                }
            )

    print("✔ Reviews done")


# -------------------------
# WISHLIST
# -------------------------
def seed_wishlist(users, products):
    print("💚 Seeding Wishlist...")

    for user in users:
        Wishlist.objects.get_or_create(
            user=user,
            product=random.choice(products)
        )

    print("✔ Wishlist done")


# -------------------------
# CART + CART ITEMS
# -------------------------
def seed_cart(users, products):
    print("🛒 Seeding Cart...")

    for user in users:
        cart, _ = Cart.objects.get_or_create(user=user)

        for product in random.sample(products, 2):
            CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    "quantity": random.randint(1, 3),
                    "unit_price": product.price,
                }
            )

    print("✔ Cart done")


# -------------------------
# RUN EVERYTHING
# -------------------------

users = seed_users()
seed_addresses(users)
seed_farmer_profiles(users)

categories = seed_categories()
products = seed_products(categories)

seed_reviews(users, products)
seed_wishlist(users, products)
seed_cart(users, products)

print("\n🎉 DONE! Database successfully seeded.")
