from flask_frozen import Freezer
from app import app, db, BlogPost, generate_sample_posts
import os

# Ensure db directory exists
os.makedirs('db', exist_ok=True)

# Initialize Freezer
freezer = Freezer(app)

# Generate sample blog posts before freezing
with app.app_context():
    db.create_all()
    if not BlogPost.query.first():
        generate_sample_posts()

# Custom generator for dynamic blog routes
@freezer.register_generator
def blog():
    yield {}  # Generate /blog route

if __name__ == '__main__':
    freezer.freeze()