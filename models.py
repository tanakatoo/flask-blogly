from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()



"""Models for Blogly."""

class User(db.Model):
    """User Model"""
    __tablename__="users"
    
    # ********** this one not working **************
    @classmethod
    def get_all_users(cls):
        all_users=cls.query.all()
        return cls.query.all()

    @classmethod
    def get_user(cls, userid):
        return cls.query.get(userid)
    
    def __repr__(self):
        return f"<id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}"

    id=db.Column(db.Integer,
                 primary_key=True,
                autoincrement=True)
    first_name=db.Column(db.String(50), 
                         nullable=False)
    last_name=db.Column(db.String(50))
    image_url=db.Column(db.String)
    
  
    
    
    
    