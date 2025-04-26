from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
# Use absolute path for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), "db", "blog.db"))}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Blog Post Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Static Data for Index Page
services = [
    {
        "title": "Strategy & Content",
        "description": "Build a powerful online presence",
        "items": [
            {"name": "Social Media Strategy", "detail": "Tailored plans to meet your goals."},
            {"name": "Content Creation", "detail": "Engaging text, images, and videos."},
            {"name": "Content Marketing", "detail": "Blogs and guides to attract customers."},
            {"name": "Account Setup", "detail": "Professional social media profiles."}
        ]
    },
    {
        "title": "Advertising & Engagement",
        "description": "Reach and connect with audiences",
        "items": [
            {"name": "Social Media Ads", "detail": "Targeted campaigns for Pretoria."},
            {"name": "PPC Advertising", "detail": "Google Ads for instant traffic."},
            {"name": "Engagement Management", "detail": "Build loyalty through interaction."},
            {"name": "Influencer Collaboration", "detail": "Expand reach with influencers."}
        ]
    },
    {
        "title": "Analytics & Support",
        "description": "Measure and optimize performance",
        "items": [
            {"name": "Analytics & Reporting", "detail": "Track progress with insights."},
            {"name": "Email Marketing", "detail": "Nurture leads with campaigns."},
            {"name": "Crisis Management", "detail": "Protect your brand reputation."},
            {"name": "Social Media Training", "detail": "Empower your team."}
        ]
    },
    {
        "title": "SEO & Website Optimization",
        "description": "Drive organic growth",
        "items": [
            {"name": "SEO Services", "detail": "Improve Google rankings."},
            {"name": "Website Design", "detail": "User-friendly, SEO-optimized sites."}
        ]
    }
]

benefits = [
    {"name": "Expertise", "detail": "Deep knowledge of digital and social media marketing."},
    {"name": "Time-Saving", "detail": "Outsource marketing to focus on your business."},
    {"name": "Increased Reach", "detail": "Expand your audience in Pretoria and beyond."},
    {"name": "Measurable Results", "detail": "Track performance with analytics."},
    {"name": "Flexibility", "detail": "Scalable services tailored to your needs."}
]

testimonials = [
    {
        "content": "Khumoitsile Consulting transformed our social media strategy...",
        "author": "Sarah Johnson",
        "company": "CEO, Bright Ideas Inc."
    },
    {
        "content": "Their SEO and PPC campaigns helped us rank higher on Google...",
        "author": "Michael Thompson",
        "company": "Marketing Director, Tech Solutions"
    },
    {
        "content": "Working with Khumoitsile on our email marketing was a game-changer...",
        "author": "Rebecca Williams",
        "company": "Founder, Innovative Services"
    }
]

# Routes
@app.route('/')
def index():
    return render_template('index.html', services=services, benefits=benefits, testimonials=testimonials)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('poster-design.html', services=services)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts, admin=False)

def generate_sample_posts():
    """Generate sample blog posts using Ollama during build."""
    prompts = [
        "Tips for social media marketing in Pretoria",
        "How to improve SEO for businesses in Mabopane Lebanon",
        "Benefits of PPC advertising for small businesses"
    ]
    for prompt in prompts:
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({
                    'model': 'llama3.2',
                    'prompt': f'Write a 500-word blog post about {prompt} for a digital marketing agency in Pretoria, Mabopane Lebanon. Include a catchy title and format in HTML with <h2>, <p>, and <ul> where appropriate.',
                    'stream': False
                })
            )
            if response.status_code == 200:
                data = response.json()
                content = data.get('response', '')
                title_start = content.find('<h2>') + 4
                title_end = content.find('</h2>')
                title = content[title_start:title_end] if title_start > 3 and title_end > title_start else prompt
                post = BlogPost(title=title, content=content)
                db.session.add(post)
                db.session.commit()
            else:
                print(f"Error generating post for {prompt}: {response.status_code}")
        except Exception as e:
            print(f"Error generating post for {prompt}: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not BlogPost.query.first():
            generate_sample_posts()
    app.run(debug=True)