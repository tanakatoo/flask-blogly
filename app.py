"""Blogly application."""
from flask import Flask, request, jsonify, redirect, render_template, flash, session,url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

# controller layer
# instanciate a controller for each domain entity (user controller, a class)
# controller.newUser, import of models
# when it's done, communicate back to this layer

# more layers, another one aggregation layer/store layer
# ability to grab a bunch of different tables the same time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ohsosecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug=DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
# db.create_all()

@app.route('/')
def home():
    return redirect ('/users')

@app.route('/users')
def list_users():
    #all_users=User.query.all()
    all_users=User.get_all_users()
    return render_template('userListing.html', all_users=all_users)

@app.route('/users/new')
def new_user():
    return render_template('addUsers.html')

@app.route('/users/new', methods=["POST"])
def new_user_db():
    #add new user to db and then go back to users
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    image_url = request.form["imageURL"]
    user=User(first_name=first_name,last_name=last_name,image_url=image_url)
    # put this in the model?
    db.session.add(user)
    db.session.commit()
    return redirect ('/users')

@app.route('/users/<int:userid>')
def user_details(userid):
    user_details=User.get_user(userid)
    posts=user_details.posts
    #get user from userid then display in template
    return render_template('userDetails.html', user=user_details, posts=posts)

@app.route('/users/<int:userid>/edit')
def user_edit(userid):
    #get user from userid and posts then display in template
    user_details=User.get_user(userid)
    
    return render_template('editUsers.html', user=user_details)

@app.route('/users/<int:userid>/edit', methods=['POST'])
def user_edit_db(userid):

    #update user info in db and then display users page
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    image_url = request.form["imageURL"]
    user=User.get_user(userid)
    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_url
    # user=User(first_name=first_name,last_name=last_name,image_url=image_url)
    # put this in the model??
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:userid>/delete', methods=["POST"])
def user_delete(userid):
    #deete user from db and display /users listing
    user=User.get_user(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:userid>/posts/new')
def new_post(userid):
    return render_template('addPost.html',userid=userid)

@app.route('/users/<int:userid>/posts/new', methods=["POST"])
def add_post(userid):
    content=request.form["content"]
    title=request.form["title"]
    # add the new post to db
    new_post=Post(title=title,content=content,author=userid)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('user_details',userid=userid))

@app.route('/posts/<int:postid>')
def get_post(postid):
    # get the post
    p=Post.query.get(postid)
    return render_template('postDetails.html',p=p)

@app.route('/posts/<int:postid>/edit')
def edit_post(postid):
    # get the post
    p=Post.query.get(postid)
    return render_template('editPost.html', p=p)

@app.route('/posts/<int:postid>/edit', methods=["POST"])
def edit_post_db(postid):
    title=request.form["title"]
    content=request.form["content"]
    # code to edit post
    # get the post first
    p=Post.query.get(postid)
    p.title=title
    p.content=content
    db.session.add(p)
    db.session.commit()   
    return redirect(url_for('get_post',postid=postid))

@app.route('/posts/<int:postid>/delete', methods=["POST"])
def delete_post(postid):
    # code to delete post
    p=Post.query.get(postid)
    db.session.delete(p)
    db.session.commit()
    # get userid from the form
    userid=int(request.form["userid"])
    return redirect(url_for('user_details',userid=str(userid)))