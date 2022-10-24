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
    
    def __repr__(self):
        return f"<id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}"
    
    id=db.Column(db.Integer,
                 primary_key=True,
                 autoincrement=True
                 )
    
    id=db.column(db.Integer,
                 primary_key=True,
                autoincrement=True)
    first_name=db.column(db.String(50), 
                         nullable=False)
    last_name=db.column(db.String(50))
    image_url=db.column(db.LargeBinary)
    
    
    
    