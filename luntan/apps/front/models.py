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
    status = db.Column(db.Integer, nullable=False, default=1)
    category_id = db.Column(db.Integer, default=0)


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50))
    comment_time = db.Column(db.DateTime, default=datetime.now)
    new_id = db.Column(db.Integer, db.ForeignKey("news.id"))
    new = db.relationship("News", backref="comments")