from exts import db
from datetime import datetime


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50))
    source = db.Column(db.String(100))
    send_time = db.Column(db.DateTime, default=datetime.now)
    digest = db.Column(db.Text, nullable=False)
