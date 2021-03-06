# from __main__ import db
from Intro import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as S
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin): # will have a table name of user (small u)
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False) # string of max 20 len
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy='subquery') # backref is for... lazy (select,joined,dynamic,subquery)

    def get_reset_token(self,expires_sec=1800):
        s = S(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = S(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f'User( {self.username}, {self.email}, {self.image_file})'

class Post(db.Model): # will have a table name of post (small p)
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False) #

    def __repr__(self):
        return f"Post( {self.title}, {self.date_posted} )"


# when we run directly from python, python calls the file "__main__"
# circular import : remember