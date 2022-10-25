"""Blogly application."""
from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

# controller layer
# instanciate a controller for each domain entity (user controller, a class)
# controller.newUser, import of models
# when it's done, communicate back to this layer

# more layers, another one aggregation layer/store layer
# ability to grab a bunch of different tables the same time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
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
    #get user from userid then display in template
    return render_template('userDetails.html', user=user_details)

@app.route('/users/<int:userid>/edit')
def user_edit(userid):
    user_details=User.get_user(userid)
    #get user from userid then display in template
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