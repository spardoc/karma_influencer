from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    last_scrape = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Influencer {self.name}>"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'), nullable=False)
    platform = db.Column(db.String(32), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(16))
    score = db.Column(db.Float)

    influencer = db.relationship('Influencer', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"<Comment {self.id} on {self.platform}>"