#!/usr/bin/env python3
import os
import sys
from datetime import datetime

# Add the current directory to path so we can import our app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from extensions import db
from models import (
    User, Category, Product, Banner,
    Review, Order, OrderItem, CartItem
)
from werkzeug.security import generate_password_hash

app = create_app()

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("Creating sample users...")
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin123"),
            is_admin=True,
            first_name="Admin",
            last_name="User",
            address="123 Admin St",
            city="New Delhi",
            state="Delhi",
            postal_code="110001",
            country="India",
            phone="+91 9876543210"
        )

        # Create regular user
        user = User(
            username="user",
            email="user@example.com",
            password_hash=generate_password_hash("user123"),
            first_name="Regular",
            last_name="User",
            address="456 User St",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            country="India",
            phone="+91 9876543211"
        )

        db.session.add_all([admin, user])
        db.session.commit()

        print("Creating categories...")
        # Create sample categories
        # categories = [
        #     Category(name="Electronics", description="Electronic devices and gadgets"),
        #     Category(name="Mobiles", description="Smartphones and mobile accessories"),
        #     Category(name="Computers", description="Laptops, desktops and accessories"),
        #     Category(name="Home & Kitchen", description="Appliances and kitchen gadgets"),
        #     Category(name="Books", description="Books in various genres"),
        #     Category(name="Clothing", description="Men's, women's and kids clothing"),
        #     Category(name="Sports", description="Sports equipment and fitness gear"),
        #     Category(name="Toys & Games", description="Toys and games for all ages")
        # ]
        categories = [
    Category(name="Electronics", description="Electronic devices and gadgets", image_url="/static/images/categories/electronics.jpg"),
    Category(name="Mobiles", description="Smartphones and mobile accessories", image_url="/static/images/categories/mobiles.jpg"),
    Category(name="Computers", description="Laptops, desktops and accessories", image_url="/static/images/categories/computers.jpg"),
    Category(name="Home & Kitchen", description="Appliances and kitchen gadgets", image_url="/static/images/categories/home_kitchen.jpg"),
    Category(name="Books", description="Books in various genres", image_url="/static/images/categories/books.jpg"),
    Category(name="Clothing", description="Men's, women's and kids clothing", image_url="/static/images/categories/clothing.jpg"),
    Category(name="Sports", description="Sports equipment and fitness gear", image_url="/static/images/categories/sports.jpg"),
    Category(name="Toys & Games", description="Toys and games for all ages", image_url="/static/images/categories/toys_games.jpg")
]

        # Create subcategories
        subcategories = [
            Category(name="Headphones", description="Wired and wireless headphones", parent_id=1),
            Category(name="Speakers", description="Bluetooth and wired speakers", parent_id=1),
            Category(name="Smart Home", description="Smart home devices", parent_id=1),
            Category(name="Smartphones", description="Mobile phones from various brands", parent_id=2),
            Category(name="Phone Cases", description="Protection for your device", parent_id=2),
            Category(name="Laptops", description="Portable computers", parent_id=3),
            Category(name="Tablets", description="Tablet computers", parent_id=3),
            Category(name="Kitchen Appliances", description="Appliances for cooking", parent_id=4),
            Category(name="Fiction", description="Fictional literature", parent_id=5),
            Category(name="Non-fiction", description="Factual books", parent_id=5)
        ]

        # Add categories to session
        db.session.add_all(categories)
        db.session.commit()  # Commit to get IDs for subcategories parent_id

        # Set parent_id for subcategories
        for i, subcat in enumerate(subcategories):
            parent_id = (i // 3) + 1  # This assigns 3 subcategories to each main category
            if parent_id <= len(categories):
                subcat.parent_id = parent_id
            else:
                subcat.parent_id = len(categories)

        db.session.add_all(subcategories)
        db.session.commit()

        # Get all categories for products
        all_categories = Category.query.all()
        categories_dict = {cat.name: cat for cat in all_categories}

        print("Creating products...")
        # Create sample products
        products = [
            # Electronics
            Product(
                name="Amazon Echo (2nd Generation)",
                description="Smart speaker with Alexa voice control. Play music, get news, set alarms, control smart home devices and more.",
                price=9999.00,
                discount_price=7999.00,
                stock=50,
                image_url="/static/images/products/echo.png",
                brand="Amazon",
                is_featured=True,
                categories=[categories_dict["Smart Home"], categories_dict["Speakers"]]
            ),
            Product(
                name="Fire TV Stick 4K with Alexa Voice Remote",
                description="Streaming media player with 4K Ultra HD, Dolby Vision, HDR, and HDR10+. Control your TV and compatible soundbar with the Alexa Voice Remote.",
                price=5999.00,
                discount_price=4999.00,
                stock=100,
                image_url="/static/images/products/firetv.png",
                brand="Amazon",
                is_featured=True,
                categories=[categories_dict["Electronics"]]
            ),
            Product(
                name="Anker PowerCore 26800mAh Portable Charger",
                description="External battery with high capacity, 3 USB ports for simultaneously charging multiple devices.",
                price=2999.00,
                discount_price=2499.00,
                stock=75,
                image_url="/static/images/products/anker.png",
                brand="Anker",
                is_featured=False,
                categories=[categories_dict["Electronics"]]
            ),
            # Mobiles
            Product(
                name="iPhone 15 Pro",
                description="Apple's latest flagship smartphone with A17 Pro chip, titanium design, and an improved camera system.",
                price=129900.00,
                discount_price=None,
                stock=25,
                image_url="/static/images/products/iphone.png",
                brand="Apple",
                is_featured=True,
                categories=[categories_dict["Smartphones"], categories_dict["Mobiles"]]
            ),
            Product(
                name="OnePlus 12",
                description="Flagship smartphone with Snapdragon 8 Gen 3, 50MP triple camera, and 100W fast charging.",
                price=64999.00,
                discount_price=59999.00,
                stock=40,
                image_url="/static/images/products/smartphone.png",
                brand="OnePlus",
                is_featured=True,
                categories=[categories_dict["Smartphones"], categories_dict["Mobiles"]]
            ),
            # Home & Kitchen
            Product(
                name="Wacaco Nanopresso Portable Espresso Maker",
                description="Compact and versatile, this portable espresso maker is perfect for travel or home use.",
                price=4999.00,
                discount_price=3999.00,
                stock=30,
                image_url="/static/images/products/espresso.png",
                brand="Wacaco",
                is_featured=False,
                categories=[categories_dict["Kitchen Appliances"], categories_dict["Home & Kitchen"]]
            ),
            # Sports
            Product(
                name="Onewheel Pint X Electric Skateboard",
                description="Self-balancing electric skateboard with a range of up to 18 miles and a top speed of 18 mph.",
                price=89990.00,
                discount_price=79990.00,
                stock=10,
                image_url="/static/images/products/skateboard.png",
                brand="Onewheel",
                is_featured=True,
                categories=[categories_dict["Sports"]]
            ),
            # Music (Sub of Electronics)
            Product(
                name="Jackson Dinky Arch Top JS32 DKA Electric Guitar",
                description="The Jackson JS32 Dinky DKA Electric Guitar has a poplar body, and bolt-on maple speed neck with graphite reinforcement.",
                price=19999.00,
                discount_price=17999.00,
                stock=15,
                image_url="/static/images/products/guitar.png",
                brand="Jackson",
                is_featured=False,
                categories=[categories_dict["Electronics"]]
            ),
        ]

        db.session.add_all(products)
        db.session.commit()

        print("Creating reviews...")
        # Create sample reviews
        reviews = [
            Review(
                user_id=2,  # Regular user
                product_id=1,  # Echo
                rating=5,
                comment="Great smart speaker! The sound quality is excellent and Alexa works perfectly.",
                created_at=datetime(2025, 1, 10)
            ),
            Review(
                user_id=2,
                product_id=1,
                rating=4,
                comment="Good speaker but sometimes Alexa doesn't understand my accent.",
                created_at=datetime(2025, 2, 5)
            ),
            Review(
                user_id=2,
                product_id=2,  # Fire TV Stick
                rating=5,
                comment="Transformed my old TV into a smart TV. Highly recommend!",
                created_at=datetime(2025, 1, 20)
            ),
            Review(
                user_id=2,
                product_id=4,  # iPhone
                rating=4,
                comment="Great phone but very expensive! Camera quality is outstanding.",
                created_at=datetime(2025, 2, 15)
            ),
        ]

        db.session.add_all(reviews)
        db.session.commit()

        print("Creating banners...")
        # Create sample banners
        banners = [
            Banner(
                title="Great Indian Festival",
                description="Huge discounts on electronics, fashion and more!",
                image_url="/static/images/banners/default-banner.jpg",
                link_url="#",
                position=1,
                is_active=True
            ),
            Banner(
                title="New iPhone Launch",
                description="Get the latest iPhone with exciting offers!",
                image_url="/static/images/banners/default-banner.jpg",
                link_url="#",
                position=2,
                is_active=True
            ),
            Banner(
                title="Books Sale",
                description="Up to 50% off on bestselling books!",
                image_url="/static/images/banners/default-banner.jpg",
                link_url="#",
                position=3,
                is_active=True
            ),
        ]

        db.session.add_all(banners)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
