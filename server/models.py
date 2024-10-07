from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10),nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name is required.")
        # Check for uniqueness
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError("Author name must be unique.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly ten digits.")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
      # Validator for title
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required.")
        # Example clickbait check (adjust as needed)
        clickbait_phrases = ['You Won\'t Believe', 'Top', 'Best', 'Why', 'How', 'Secret']
        if any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title is clickbait.")
        return title
    # Validator for content length
    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    # Validator for summary length
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary cannot be more than 250 characters.")
        return summary

    # Validator for category
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']  # Adjust as necessary
        if category not in valid_categories:
            raise ValueError("Invalid category.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
