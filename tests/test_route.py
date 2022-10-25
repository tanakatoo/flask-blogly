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
    
    @classmethod
    def tearDownClass(cls):
        db.session.rollback()
        
    def test_new(self):
        with app.test_client() as client:
            res=client.post('/users/new', data={'firstName':'John','lastName':'Doe', 'imageURL':'https://eloquentjavascript.net/img/chapter_picture_6.jpg'}, follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('John', html)
            self.assertIn('Doe', html)
    
    def test_edit(self):
        with app.test_client() as client:
            res=client.post('/users/1/edit', data={'firstName':'Karmen The Second','lastName':'Too', 'imageURL':'https://eloquentjavascript.net/img/chapter_picture_6.jpg'}, follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('Karmen The Second',html)
    
    def test_allListings(self):
        user=User(first_name="Jane",last_name="Two",image_url="https://eloquentjavascript.net/img/chapter_picture_6.jpg")
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:
            res=client.get('/users')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('Jane', html)
            self.assertIn('Karmen', html)
            
    def test_delete(self):
        with app.test_client() as client:
            res=client.post('/users/1/delete', follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertNotIn('Karmen', html)