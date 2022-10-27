from app import app
from models import db, User, Post, connect_db
from unittest import TestCase


app.config['TESTING']=True
connect_db(app)

class TestRoutes(TestCase):
    @classmethod
    def setUpClass(cls):
        # make a new user and post
        db.drop_all()
        db.create_all()
        print('**************')
        print(app.config['TESTING'])
        user=User(first_name="Karmen",last_name="Too",image_url="https://eloquentjavascript.net/img/chapter_picture_6.jpg")
        post=Post(title="First Post",author=1,content="First post content")
        db.session.add(user)
        db.session.commit()
        db.session.add(post)
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
            
   
    
    def test_display_post(self):
         with app.test_client() as client:
            res=client.get('/users/1')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('First Post', html)
    
    def test_post_details(self):
        with app.test_client() as client:
            res=client.post('/posts/1')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('First post content', html)
            
    def test_post_insert(self):
        # post=Post(title="Second Post",author=1,content="Second post content")
        # db.session.add(post)
        # db.session.commit()
        with app.test_client() as client:
            res=client.post('/users/1/posts/new', data={'title': 'Second Post','author':'1','content':'Second post content'},follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('First post content', html)
    
    def test_post_edit(self):
        with app.test_client() as client:
            res=client.post('/posts/1/edit', data={'title': 'Changed Second Post','author':'1','content':'Changed second post content 2'},follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('Changed Second Post', html)
            self.assertIn('Changed second post content 2', html)
            
    
    def test_post_delete(self):
        with app.test_client() as client:
            res=client.post('/posts/1/delete')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertNotIn('Changed Second Post', html)
            
    def test_delete(self):
        with app.test_client() as client:
            res=client.post('/users/1/delete', follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertNotIn('Karmen', html)