from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()



"""Models for Blogly."""

class User(db.Model):
    """User Model"""
    __tablename__="users"
    
    @classmethod
    def get_all_users(cls):
        all_users=cls.query.order_by(cls.last_name,cls.first_name).all()
        return all_users

    @classmethod
    def get_user(cls, userid):
        return cls.query.get_or_404(userid)
    
    def __repr__(self):
        return f"<id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>"

    id=db.Column(db.Integer,
                 primary_key=True,
                autoincrement=True)
    first_name=db.Column(db.String(50), 
                         nullable=False)
    last_name=db.Column(db.String(50))
    image_url=db.Column(db.Text)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
  
    posts=db.relationship('Post',cascade='all, delete')
    
class Post(db.Model):
    __tablename__="posts"
    
    def __repr__(self):
        return f"<title:{self.title}, author:{self.author}>"

    id=db.Column(db.Integer,
                 primary_key=True,
                autoincrement=True)
    title=db.Column(db.Text,nullable=False)
    content=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime, nullable=False, default=datetime.now())
    author=db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user=db.relationship('User')
    
    tags=db.relationship('Tag', secondary="posttags", cascade='all, delete',backref='posts')
    
    def get_all_posts(self):
        posts=User.posts.title
        return posts

class Tag(db.Model):
    __tablename__="tags"
    
    def __repr__(self):
        return f"<id={self.id}, name={self.name}"
    
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    name=db.Column(db.Text,nullable=False, unique=True)


class PostTag(db.Model):
    __tablename__="posttags"
    
    def __repr__(self):
        return f"<post_id={self.post_id}, tag_id={self.tag_id}>"
    
    post_id= db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False,primary_key=True)
    tag_id= db.Column(db.Integer,db.ForeignKey('tags.id'), nullable=False,primary_key=True)