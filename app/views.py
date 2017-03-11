from flask import render_template, flash, redirect,g,url_for,session,request,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import get_debug_queries
from app import app,lm,db
from .forms import LoginForm,RegistrationForm,PostForm
from .models import User,Post,Wxsetting,Wxuser,Wxpost
from datetime import datetime
from config import POSTS_PER_PAGE,DATABASE_QUERY_TIMEOUT
from .wxchat import wx_login_bat,wx_is_login_state,wx_logout,sendmsg,WX_user_setting,Update_setting
from bot.models.wudebit import Select_vip_code


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
            return redirect(request.args.get('next') or url_for('wechat'))

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
                               is_wxchat=ret,
                               active_page='wechat')
    return render_template('wechat.html',
                           is_wxchat=ret,
                           active_page='wechat')

@app.route('/wechat/login/', methods=['GET', 'POST'])
@login_required
def wechat_login():
    ret=wx_is_login_state()
    if not ret:
        wx_logout()
        temp = request.args.get('timestamp')
        WX_PID = wx_login_bat(temp)
        if WX_PID:
            flash('Please scan the QR code to log in.')
            return render_template('wxchat/wxlogin.html',
                                   posts=[],
                                   img_path='%s.jpg' % temp,
                                   is_wxchat=ret,
                                   active_page='wechat_login')
        flash('Log in time out,Please get the qr code again.')
        wx_logout()
        return render_template('wxchat/wxlogin.html',
                               posts=[],
                               img_path=False,
                               is_wxchat=ret,
                               active_page='wechat_login')
    flash('请勿重复登录')
    return redirect(url_for('wechat'))

@app.route('/wechat/wxfriends/', methods=['GET', 'POST'])
@login_required
def wechat_wxfriends():
    ret=wx_is_login_state()
    if not ret:
        flash('微信未登录,部分功能无法正常使用')
    page = request.args.get('page', 1, type=int)
    users=Wxuser.query.paginate(page, 15, False)
    return render_template('wxchat/wxfriends.html',
                           users=users,
                           is_wxchat=ret,
                           active_page='wechat_wxfriends'
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
    ret=wx_is_login_state()
    if request.method=='GET':
        return render_template('wxchat/setting.html',
                               is_wxchat=ret,
                               active_page='wechat_setting',
                               function_list=Wxsetting().getsetting())

    post_type = request.form['type']
    if ret:
        if post_type == 'usersetting':
            id = request.form['id']
            remarkname = request.form['remarkname']
            right = request.form['right']
            return jsonify({
                'text': WX_user_setting(id, remarkname, right)
            })
    if post_type == 'adminphoneset':
        ph1 = request.form['phone1']
        ph2 = request.form['phone2']
        if len(ph1)==11 and len(ph2)==11:
            setting=Wxsetting().get()
            setting.adminphone='%s,%s'%(ph1,ph2)
            db.session.add(setting)
            db.session.commit()
            Update_setting()
            return jsonify({
                'text':'更新成功'
            })
            #操作写进数据库
        return jsonify({
            'text':'Error:电话号码不正确'
        })
    elif post_type=='Advanced_Settings':
        if 'true' in request.form['OnSendalarmMsg']:
            ret1 =True
        else:
            ret1=False
        if 'true' in request.form['Reboton']:
            ret2 =True
        else:
            ret2=False
        q=Wxsetting().get()
        q.OnSendalarmMsg = ret1
        q.Reboton=ret2
        db.session.add(q)
        db.session.commit()
        Update_setting()
        return jsonify({
            'text': '操作成功'
        })
    elif post_type=='Feature_Settings':
        if 'true' in request.form['Add_friend']:
            ret1 =True
        else:
            ret1=False
        if 'true' in request.form['Get_vip_integral']:
            ret2 =True
        else:
            ret2=False
        if 'true' in request.form['Send_bill_balance_teble']:
            ret3 =True
        else:
            ret3=False
        if 'true' in request.form['Sale_table']:
            ret4 =True
        else:
            ret4=False
        if 'true' in request.form['Sale_today']:
            ret5 =True
        else:
            ret5=False
        if 'true' in request.form['Sale_Brand_All']:
            ret6 =True
        else:
            ret6=False
        if 'true' in request.form['Sale_Brand_Table']:
            ret7 =True
        else:
            ret7=False
        q = Wxsetting().get()
        q.Add_friend = ret1
        q.Get_vip_integral = ret2
        q.Send_bill_balance_teble = ret3
        q.Sale_table = ret4
        q.Sale_today = ret5
        q.Sale_Brand_All = ret6
        q.Sale_Brand_Table = ret7
        db.session.add(q)
        db.session.commit()
        Update_setting()
        return jsonify({
            'text': '操作成功'
        })
    return jsonify({
        'text': '操作失败'
    })


@app.route('/wechat/queryvip', methods = ['POST','GET'])
def wechat_queryvip():
    phone = request.form['phone']
    print(phone)
    if len(phone)!=11:
        return jsonify({
        'text': '不是电话号码'
    })
    return jsonify({
        'text': Select_vip_code('%s' % phone)
    })

@app.errorhandler(404)
def internal_error(error):
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return redirect(url_for('index'))