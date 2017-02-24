from app import db

class Wxuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wx_uin=db.Column(db.String(126), index = True,unique = True)#微信唯一id
    wx_uid=db.Column(db.String(126))#微信临时id，发送信息需要
    nickname=db.Column(db.String(64))#微信网名
    remarkname=db.Column(db.String(64))#微信备注名
    right =db.Column(db.Integer,default=1)  # 权限
    posts = db.relationship('Wxpost', backref='author', lazy='dynamic')

    # def __init__(self,wx_uid):
    #     self.wx_uid=wx_uid

    def get_id(self,wx_uid):
        return Wxuser.query.filter_by(wx_uid=wx_uid).first().id

    def get(self,wx_uid):
        return Wxuser.query.filter_by(wx_uid=wx_uid).first()


    def __repr__(self):
        return '<User %r>' % (self.wx_uin)

class Wxpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender=db.Column(db.String(126))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    wxuser_id = db.Column(db.Integer, db.ForeignKey('wxuser.id'))

    def message_posts(self):
        return Wxpost.query.order_by(Wxpost.timestamp.desc())

    def __repr__(self):
        return '<WXPost %r>' % (self.body)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), index = True, unique = True)#网站邮箱
    username=db.Column(db.String(64),index = True)#网站用户名
    password = db.Column(db.String(126))#网站密码
    wxpid=db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True
    #is_authenticated 方法有一个具有迷惑性的名称。一般而言，这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证。

    def is_active(self):
        return True
    #is_active 方法应该返回 True，除非是用户是无效的，比如因为他们的账号是被禁止。

    def is_anonymous(self):
        return False
    #is_anonymous 方法应该返回 True，除非是伪造的用户不允许登录系统。

    def verify_password(self, password):
        #对比用户密码
        if self.password==password:
            return True
        else:
            return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def set_wxpid(self,pid):
        try:
            self.wxpid = pid
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


    def get_wxpid(self):
        return self.wxpid


    def message_posts(self):
        return Post.query.order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % (self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender=db.Column(db.String(126))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Post %r>' % (self.body)


class Statemsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg=db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Statemsg %r>' % (self.msg)

class Logmsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg=db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Statemsg %r>' % (self.msg)