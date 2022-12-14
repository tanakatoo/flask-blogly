from app import app
from models import db, User, Post, connect_db
from unittest import TestCase


app.config['TESTING']=True

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///blogly-test'
app.config['SQLALCHEMY_ECHO']=True
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']



class TestRoutes(TestCase):
    def setUp(self):
        # make a new user and post
        db.drop_all()
        db.create_all()
        print('************dropping and creting all tables again *****************')
        user=User(first_name="Karmen",last_name="Too",image_url="https://eloquentjavascript.net/img/chapter_picture_6.jpg")
        post=Post(title="First Post",author=1,content="First post content")
        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()
    
    def tearDown(self):
        db.session.rollback()
        
        
    def test_allListings(self):
    # user=User(first_name="Jane",last_name="Two",image_url="https://eloquentjavascript.net/img/chapter_picture_6.jpg")
    # db.session.add(user)
    # db.session.commit()

        with app.test_client() as client:
            res=client.get('/users')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('Karmen', html) 
            print("***************** 1 test all listings")
            print(User.query.all())
    def test_new(self):
        with app.test_client() as client:
            res=client.post('/users/new', data={'firstName':'John','lastName':'Doe', 'imageURL':'https://eloquentjavascript.net/img/chapter_picture_6.jpg'}, follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('John', html)
            self.assertIn('Doe', html)
            self.assertIn('Karmen', html)
            self.assertIn('Too', html)
            print("***************** 2 test_new")
            print(User.query.all())
    
    def test_edit(self):
        with app.test_client() as client:
            res=client.post('/users/1/edit', data={'firstName':'Karmen The Second','lastName':'Too', 'imageURL':'https://eloquentjavascript.net/img/chapter_picture_6.jpg'}, follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('Karmen The Second',html)
    
            print("***************** 3 test edit user")
            print(User.query.all())
            
   
    
    def test_display_post(self):
         with app.test_client() as client:
            res=client.get('/users/1')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('First Post', html)
            print("***************** 4 test display post, but user is")
            print(User.query.all())
    
    def test_post_details(self):
        with app.test_client() as client:
            res=client.get('/posts/1')
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('First post content', html)
            
            print("***************** 5 test post details, but user is")
            print(User.query.all())
            
    def test_post_insert(self):
        with app.test_client() as client:
            res=client.post('/users/1/posts/new', data={'title': 'Second Post','author':'1','content':'Second post content'},follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('First Post', html)
            self.assertIn('Second Post', html)
    
            print("***************** 6 test post insert, but user is")
            print(User.query.all())
    def test_post_edit(self):
        with app.test_client() as client:
            res=client.post('/posts/1/edit', data={'title': 'Changed Second Post','author':'1','content':'Changed second post content 2'},follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertIn('Changed Second Post', html)
            self.assertIn('Changed second post content 2', html)
            print("***************** 7 test post edit, but user is")
            print(User.query.all())   
    
    def test_post_delete(self):
        with app.test_client() as client:
            res=client.post('/posts/1/delete', data={'userid': '1'},follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertNotIn('Changed Second Post', html)
            print("***************** 8 test post delete, but user is")
            print(User.query.all())
    def test_delete(self):
        with app.test_client() as client:
            res=client.post('/users/1/delete', follow_redirects=True)
            html=res.get_data(as_text=True)
            
            self.assertEqual(res.status_code,200)
            self.assertNotIn('Karmen', html)