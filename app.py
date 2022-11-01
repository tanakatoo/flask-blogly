"""Blogly application."""

from flask import Flask, request, jsonify, redirect, render_template, flash, session,url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

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
    return render_template ('home.html')

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
    # user=User.get_user(userid)
    user=User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:userid>/posts/new')
def new_post(userid):
    all_tags=Tag.query.all()
    return render_template('addPost.html',userid=userid, allTags=all_tags)

@app.route('/users/<int:userid>/posts/new', methods=["POST"])
def add_post(userid):

    content=request.form["content"]
    title=request.form["title"]
    checkedTags=request.form.getlist('tags')
    # add the new post to db
    t=Tag.query.filter(Tag.name.in_(checkedTags)).all()

    new_post=Post(title=title,content=content,author=userid)
    for ta in t:
        new_post.tags.append(ta)
    db.session.add(new_post)
    db.session.commit()
    #edit_add_post(new_post.id)
    return redirect(url_for('user_details',userid=userid))

@app.route('/posts/<int:postid>')
def get_post(postid):
    # get the post
    p=Post.query.get(postid)
    # need to add something if there are no tags
    tags=p.tags

    return render_template('postDetails.html',p=p, tags=tags)

@app.route('/posts/<int:postid>/edit')
def edit_post(postid):
    # get the post
    p=Post.query.get(postid)
    tags=p.tags
    all_tags=Tag.query.all()
    return render_template('editPost.html', p=p, tags=tags, allTags=all_tags)

@app.route('/posts/<int:postid>/edit', methods=["POST"])
def edit_post_db(postid):
    # edit_add_post(postid)
    title=request.form["title"]
    content=request.form["content"]
    checkedTags=request.form.getlist('tags')
    p=Post.query.get(postid)
    p.title=title
    p.content=content
    p.tags=Tag.query.filter(Tag.name.in_(checkedTags)).all()
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('get_post',postid=postid))

@app.route('/posts/<int:postid>/delete', methods=["POST"])
def delete_post(postid):
    # delete from posttag first
    
    # code to delete post
    p=Post.query.get(postid)
    
    db.session.delete(p)
    db.session.commit()
    # get userid from the form
    userid=int(request.form["userid"])
    return redirect(url_for('user_details',userid=str(userid)))

@app.route('/tags')
def get_tags():
    tags=Tag.query.all()
    return render_template('tags.html',tags=tags)

@app.route('/tags/<int:tag_id>')
def get_tag(tag_id):
    t=Tag.query.get(tag_id)
    # also get all the posts for this tag
    t_posts=t.posts
    return render_template('tagDetails.html', tag=t, posts=t_posts)

@app.route('/tags/new')
def new_tag():
    return render_template('addTag.html')

@app.route('/tags/new', methods=['POST'])
def new_tag_db():
    name=request.form['tagName']
    # write to db
    t=Tag(name=name)
    db.session.add(t)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    t=Tag.query.get(tag_id)
    return render_template('editTag.html',t=t)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_db(tag_id):
    name=request.form['tagName']
    t=Tag.query.get(tag_id)
    t.name=name
    db.session.add(t)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    t=Tag.query.get(tag_id)
    db.session.delete(t)
    return redirect('/tags')


def edit_add_post(postid):
    title=request.form["title"]
    content=request.form["content"]
    checkedTags=request.form.getlist('tags') #gets list of the values of checkboxes that are checked only
    
    
    #tags_in_db=Post.query.get(postid).tags #gets all the tags objects in the db associated with post
    # all_tags_in_db=Tag.query.all()
    # if the tag is still checked, leave it, otherwise, add it or remove it
    # print('********')
    # print(all_tags_in_db)
    # print(checkedTags)
    # for tag in all_tags_in_db: #for each tag in the db,
    #     pt=PostTag.query.get([postid,tag.id]) #try to get the data from posttag table
    #     print('********')
    #     print(pt)
        
    #     if tag.name in checkedTags: #if it is checked, see if it is in the db
    #         if not pt: #if it is not in the db
    #             #add it to the db
    #             print('********')
    #             print('not in d but tag checked in form')
    #             p=Post.query.get(postid)
    #             p.tags.append(tag)
    #             db.session.add(p)
    #             db.session.commit()
    #     elif not tag.name in checkedTags: #if it is not checked, see if it is in the db
    #         if pt:
    #             print('********')
    #             print('in d but tag not checked in form')
    #             PostTag.query.filter_by(post_id=postid,tag_id=tag.id).delete() #delete from db
    #             db.session.commit()
  
    # code to edit post
    # get the post first
    p=Post.query.get(postid)
    p.title=title
    p.content=content
    p.tags=Tag.query.filter(Tag.id.in_(checkedTags)).all()
    db.session.add(p)
    db.session.commit()
    return 