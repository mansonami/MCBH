from app import db

class Wxuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wx_uin=db.Column(db.String(126), index = True,unique = True)#微信唯一id
    wx_uid=db.Column(db.String(126))#微信临时id，发送信息需要
    nickname=db.Column(db.String(64))#微信网名
    remarkname=db.Column(db.String(64))#微信备注名
    right =db.Column(db.Integer,default=1)  # 权限

    def get_id(self,wx_uid):
        return Wxuser.query.filter_by(wx_uid=wx_uid).first().id

    def get_name(self,wx_uid):
        id=Wxuser.query.filter_by(wx_uid=wx_uid).first()
        if id.remarkname:
            return id.remarkname
        return id.nickname


    def save(self):
        db.session.add(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def get(self,wx_uid):
        return Wxuser.query.filter_by(wx_uid=wx_uid).first()


    def __repr__(self):
        return '<User %r>' % (self.wx_uin)

class Wxpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender=db.Column(db.String(126))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    wxuser_id = db.Column(db.String(140))

    def message_posts(self):
        return Wxpost.query.filter_by(sender='普通').order_by(Wxpost.timestamp.desc())

    def suggest_posts(self):
        return  Wxpost.query.filter_by(sender='建议').order_by(Wxpost.timestamp.desc())

    def save(self):
        db.session.add(self)
        db.session.commit()

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

class Wxsetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminphone=db.Column(db.String(64))#管理员电话
    OnSendalarmMsg=db.Column(db.Boolean)#是否启用报警短信
    Reboton=db.Column(db.Boolean)#是否启用小黄鸭
    Add_friend=db.Column(db.Boolean)#自动添加好友
    Get_vip_integral = db.Column(db.Boolean)  # 查询积分
    Send_bill_balance_teble= db.Column(db.Boolean)  # 对账单
    Sale_table= db.Column(db.Boolean)  # 销售报表
    Sale_today= db.Column(db.Boolean)  # 销售
    Sale_Brand_All= db.Column(db.Boolean)  # 专柜销售
    Sale_Brand_Table= db.Column(db.Boolean)  # 专柜详细

    def get(self):
        q=Wxsetting.query.get(1)
        if q:
            return q
        else:
            q=Wxsetting()
            return q

    def getsetting(self):
        q=self.get()
        return {
            'adminphone':q.adminphone,
            'OnSendalarmMsg':q.OnSendalarmMsg,
            'Reboton':q.Reboton,
            'Add_friend':q.Add_friend,
            'Get_vip_integral':q.Get_vip_integral,
            'Send_bill_balance_teble': q.Send_bill_balance_teble,
            'Sale_table': q.Sale_table,
            'Sale_today': q.Sale_today,
            'Sale_Brand_All': q.Sale_Brand_All,
            'Sale_Brand_Table': q.Sale_Brand_Table
        }
    def __repr__(self):
        return '<Wxsetting %r>' % (self.id)