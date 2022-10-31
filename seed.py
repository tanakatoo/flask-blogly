from app import app
from models import db, User,Post, Tag, PostTag

#db.drop_all()
db.create_all()

# empty all of the info
# User.query.delete()
# Tag.query.delete()
# PostTag.query.delete()
# Post.query.delete()

u1=User(first_name="Karmen",last_name="Too",image_url="https://s0.2mdn.net/simgad/15022311863685636752")
u2=User(first_name="Tim",last_name="BB",image_url="https://eloquentjavascript.net/img/chapter_picture_6.jpg")
t1=Tag(name="Kitchen")
t2=Tag(name="Living")
t3=Tag(name="Books")
t4=Tag(name="Travel")
p1=Post(title="K1 post",content="nothing to write",author=1)
p2=Post(title="K1 post again", content="nothing again to write",author=1)
p3=Post(title="T1 post ", content="nothing again to write ttt",author=2)
p4=Post(title="T1 post again", content="nothing again to write again ttt",author=2)


db.session.add(u1)
db.session.add(u2)
db.session.add(t1)
db.session.add(t2)
db.session.add(t3)
db.session.add(t4)
db.session.commit()

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.commit()

p1.tags.append(t1)
p1.tags.append(t2)
p2.tags.append(t1)
p2.tags.append(t4)
p3.tags.append(t3)
p3.tags.append(t1)
p4.tags.append(t3)
p4.tags.append(t2)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.commit()
