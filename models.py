from app import app, db
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    topic = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean)
    created_at = db.Column(db.String(50), nullable=False)