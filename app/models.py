from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

likes = db.Table('likes', 
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                 db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                 )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(300))
    password = db.Column(db.String(100))
    posts = db.relationship('Post')
    comments = db.relationship('Comment')
    like_posts = db.relationship('Post', secondary='likes', backref='liked_by')



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(5000))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment')
    author = db.relationship('User', backref='user_posts')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(5000))
    like = db.Column(db.Integer, default=0)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))