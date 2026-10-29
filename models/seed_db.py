
from flask import Flask
from extensions import db
from models import Category, Part, User, UserStock
import random

"""
Database seed file for testing.

Creates:
- Categories
- Parts assigned to categories
- Users
- User stock entries with random quantities
"""

categories = [
    "Connectors",
    "Sensors",
    "Power",
    "Protection",
    "ICs",
    "Diodes",
    "Resistors",
]

usernames = ["Alice", "Bob", "Simon", "Henry", "Andrew", "Steve"]

parts_per_category = 20

def seed_db(app: Flask):
    db.init_app(app)

    with app.app_context():
        # WARNING: This deletes all existing database data.
        db.drop_all()
        db.create_all()

        # Seed categories
        category_objects = []

        for name in categories:
            category = Category(name=name)
            db.session.add(category)
            category_objects.append(category)

        db.session.flush()

        # Seed parts
        part_objects = []

        for category in category_objects:
            for i in range(1, parts_per_category + 1):
                part = Part(
                    name=f"{category.name} Part {i}",
                    cat_id=category.id,
                )
                db.session.add(part)
                part_objects.append(part)

        # Seed users
        user_objects = []

        for name in usernames:
            user = User(
                username=name.lower(),
                email=f"{name.lower()}@gmail.com",
            )
            db.session.add(user)
            user_objects.append(user)

        # Ensure users and parts have IDs before creating stock entries
        db.session.flush()

        # Seed user stock
        for user in user_objects:
            # Each user owns a random selection of parts
            owned_parts = random.sample(
                part_objects,
                k=random.randint(10, min(40, len(part_objects))),
            )

            for part in owned_parts:
                stock = UserStock(
                    user_id=user.id,
                    part_id=part.id,
                    quantity=random.randint(1, 100),
                )
                db.session.add(stock)

        db.session.commit()

        print(f"Created {len(category_objects)} categories")
        print(f"Created {len(part_objects)} parts")
        print(f"Created {len(user_objects)} users")
        print(f"Created {UserStock.query.count()} stock entries")


if __name__ == "__main__":
    # Import your Flask app here if needed.
    # Example:
    # from app import app
    # seed_db(app)
    pass
