from datetime import datetime

import flask_login
from app import db,login_manager
from flask_login import  UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# this is the user Model/Sql table
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    ##password = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_url = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    Posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_url}')"

# Not used so ignore but dont touch
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    data_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"User('{self.title}','{self.data_posted}'"

#This is used to stored information about successfully uploaded files
class FileUpload(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    author_email = db.Column(db.String(120), unique=False, nullable=False)
    staff_email = db.Column(db.String(120), unique=False, nullable=False)
    data_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    file_Path = db.Column(db.String(50),nullable=False)
    def __repr__(self):
        return f"User('{self.name}','{self.data_posted}'"