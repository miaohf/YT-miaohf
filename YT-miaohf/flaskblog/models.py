from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    ytuserid = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __table_args__ = {"useexisting": True}

    #id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(100), nullable=False)
    #date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #content = db.Column(db.Text, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
             #<td class="text-center">{{ postdtl.receiveprice }}*{{ postdtl.numexp }}*{{ postdtl.copys }}</td>

    id = db.Column(db.Integer, primary_key=True)
    ytid = db.Column(db.String(15), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    customer = db.Column(db.Text, nullable=False)
    custid = db.Column(db.String(10), nullable=False)
    contacts = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(10), nullable=False)
    togatheramount = db.Column(db.String(10), nullable=False)
    thumb = db.Column(db.String(100), nullable=False)
    flowid = db.Column(db.Integer, nullable=False)
    ischecked = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.String(10), db.ForeignKey('user.ytuserid'), nullable=False)
    dealuser = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Postdtl(db.Model):
    __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    ytid = db.Column(db.String(15), unique=True, nullable=False)
    businame = db.Column(db.String(50), nullable=False)
    busisubname = db.Column(db.String(50), nullable=False)
    busisubunit = db.Column(db.String(10), nullable=False)
    receiveprice = db.Column(db.Float, nullable=False)
    renderimg = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    copys = db.Column(db.Integer, nullable=False)
    numexp = db.Column(db.Integer, nullable=False)
    remark = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Post('{self.renderimg}', '{self.create_time}')"
