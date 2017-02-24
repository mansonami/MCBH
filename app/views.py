from flask import render_template, flash, redirect,g,url_for,session,request,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import get_debug_queries
from app import app,lm,db
from .forms import LoginForm,RegistrationForm,PostForm
from .models import User,Post
from datetime import datetime
from config import POSTS_PER_PAGE,DATABASE_QUERY_TIMEOUT
from .wxchat import wx_login_bat,wx_is_login_state,wx_logout,sendmsg,WXsetting
from bot.models.Boxfriends import Wxuser,Wxpost
from bot.models.view import Get_vip_integral


@app.before_request
def before_request():
    g.user = current_user

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated:
        return render_template('index.html',
                               username=g.user.username)
    else:
        return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/<int:page>', methods=['GET', 'POST'])
@login_required
def home(page=1):
    flash('未开放')
    return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user,sender='admin')
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('home'))
    posts = g.user.message_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('home.html',
                           username=g.user.username,
                           form=form,
                           posts=posts)


@app.route('/myself', methods=['GET', 'POST'])
@login_required
def myself():
    return render_template('myself.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    # g 对象 存储生命周期内已经登录的用户，不用再次登录 直接重定向至 主页
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            session['remember_me'] = form.remember_me.data
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))

        flash('Invalid username or password.')
    return render_template('login.html',
                           title='Sign In',
                           form=form)
#注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    flash('未开放，注册请联系管理员  邮箱：woaiwoq@vip.qq.com')
    return redirect(request.args.get('next') or url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    wxpid=999999)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请使用注册帐号登录吧！')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#退出登录
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

###微信视图
@app.route('/wechat', methods=['GET', 'POST'])
@login_required
def wechat():
    ret=wx_is_login_state()
    if not ret:
        flash('微信掉线,请尽快重新登录')
        return render_template('wechat.html',
                               is_wxchat=ret)
    posts = Wxpost.select().order_by(Wxpost.timestamp.desc()).paginate(1,15)
    return render_template('wechat.html',
                           posts=posts,
                           is_wxchat=ret)

@app.route('/wechat/login/', methods=['GET', 'POST'])
@login_required
def wechat_login():
    ret=wx_is_login_state()
    if not ret:
        temp = request.args.get('timestamp')
        WX_PID = wx_login_bat(temp)
        if WX_PID:
            flash('Please scan the QR code to log in.')
            return render_template('wxchat/wxlogin.html',
                                   posts=[],
                                   img_path='%s.jpg' % temp,
                                   is_wxchat=ret)
        flash('Log in time out,Please get the qr code again.')
        wx_logout()
        return render_template('wxchat/wxlogin.html',
                               posts=[],
                               img_path=False,
                               is_wxchat=ret)
    return redirect(url_for('wechat'))

@app.route('/wechat/wxfriends/', methods=['GET', 'POST'])
@login_required
def wechat_wxfriends():
    ret=wx_is_login_state()
    if not ret:
        flash('微信未登录,不能发送消息')
    page = request.args.get('page', 1, type=int)
    #计算页数
    prev_num=page-1
    if prev_num==0:
        prev_num=False
    next_num=page+1
    #计算页数
    posts = Wxpost.select().order_by(Wxpost.timestamp.desc()).paginate(1,15)
    users=Wxuser.select().paginate(page, 15)
    if len(users)<15:
        next_num=False
    return render_template('wxchat/wxfriends.html',
                           posts=posts,
                           users=users,
                           is_wxchat=ret,
                           prev_num=prev_num,  #上一页
                           next_num=next_num,  #下一页
                           )

@app.route('/wechat/wxlogout/', methods=['GET', 'POST'])
@login_required
def wechat_wxlogout():
    ret = wx_is_login_state()
    if ret:
        a = wx_logout()
        flash(a)
        return redirect(url_for('wechat'))
    flash('未登录微信')
    return redirect(url_for('wechat'))


#发送消息ajax
@app.route('/wechat/sendmsg', methods = ['POST'])
@login_required
def wechat_sendmsg():
    if wx_is_login_state():
        id = request.form['id']
        text = request.form['text']
        if len(request.form['text']) < 1:
            return jsonify({
                'text': '请输入发送内容'
            })
        sendmsg(id, text)
        return jsonify({
            'text': '发送成功'
        })
    return jsonify({
        'text': '微信帐号未登陆'
    })


#修改设置ajax
@app.route('/wechat/setting', methods = ['POST','GET'])
@login_required
def wechat_setting():
    if wx_is_login_state():
        id=request.form['id']
        remarkname=request.form['remarkname']
        right=request.form['right']
        return jsonify({
            'text': WXsetting(id,remarkname,right)
        })
    return 'False'

@app.route('/wechat/queryvip', methods = ['POST','GET'])
def wechat_queryvip():
    phone = request.form['phone']
    return jsonify({
        'text': Get_vip_integral('phone %s' % phone)
    })


@app.errorhandler(404)
def internal_error(error):
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return redirect(url_for('index'))