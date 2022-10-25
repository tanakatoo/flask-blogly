from app import app
from models import db, User
from unittest import TestCase

app.config['TESTING']=True
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///blogly-test'
app.config['SQLALCHEMY_ECHO']=False

db.drop_all()
db.create_all()

class TestRoutes(TestCase):
    @classmethod
    def setUpClass(cls):
        User.query.delete()
        # make a new user
        user=User(first_name="Karmen",last_name="Too",image_url="https://eloquentjavascript.net/img/chapter_picture_6.jpg")
        db.session.add(user)
        db.session.commit()
    
    # @classmethod
    # def tearDownClass(cls):
        # db.session.rollback()
        
    def test_new(self):
        with app.test_client() as client:
            res=client.post('/users/new', data={'firstName':'John','lastName':'Doe', 'imageURL':'https://eloquentjavascript.net/img/chapter_picture_6.jpg'})
            html=res.get_data(as_text=True)
            
            self.assertIn('Karmen', html)
            self.assertIn('Doe', html)
    
    def test_edit(self):
        with app.test_client() as client:
            res=client.post('/users/1/', data={'firstName':'Karmen The Second','lastName':'Too', 'imageURL':'https://eloquentjavascript.net/img/chapter_picture_6.jpg'})
            html=res.get_data(as_text=True)
            
