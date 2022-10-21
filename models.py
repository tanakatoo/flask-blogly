from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()



"""Models for Blogly."""

class User(db.Model):
    """User Model"""
    __tablename__="User"
    def __repr__(self):
        return f""
    
    id=db.column(db.Integer,
                 primary_key=True,
                autoincrement=True)
    first_name=db.column(db.String(50), 
                         nullable=False)
    last_name=db.column(db.String(50))
    image_url=db.column(db.LargeBinary)
    
    
    
    