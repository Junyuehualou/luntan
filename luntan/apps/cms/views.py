from flask import Blueprint, render_template, views, request, session, redirect, url_for, g, flash
from .forms import LoginForm, ChangeSecret, NewsWrite
from .models import CMSUser
from ..front.models import News
import config
from .decorators import login_required
from exts import db
from datetime import datetime
import time


bp = Blueprint('cms', __name__, url_prefix="/cms")


# 首页
@bp.route('/')
def index():
    return render_template('cms/css_index.html')


# 注销
@bp.route('/logout/', endpoint="logout")
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 个人中心
@bp.route('/profile/',endpoint='profile')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 登录验证
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.password == password:
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # session 的持久化  为31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="用户名或者密码错误")
        else:
            message = form.get_errors()
            return self.get(message=message)


bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))


# 更换密码
class ChangeView(views.MethodView):
    def get(self):
        return render_template('cms/cms_change_secret.html')

    def post(self):
        print("开始")
        form = ChangeSecret(request.form)
        if form.validate():
            old_password = form.old_password.data
            password_repeat = form.password_repeat.data
            user = CMSUser.query.filter_by(password=old_password).first()
            if user:
                user.password = password_repeat
                db.session.commit()
                flash("密码更改成功， 请重新登录")
                return redirect(url_for('cms.login'))
            else:
                flash("修改密码失败")
                return render_template('cms/cms_change_secret.html')
        else:
            flash("修改密码失败")
            return render_template('cms/cms_change_secret.html')


bp.add_url_rule('/change/',view_func=ChangeView.as_view('change'))


# 转到新闻版块
@bp.route('/news/', endpoint="news")
@login_required
def news():
    return render_template('front/front_index.html')


# 写新闻  并将信息渲染到新闻版块
@bp.route('/write/', methods=["POST", "GET"])
@login_required
def write_news():
    if request.method == "GET":
        return render_template('front/news_editor.html')
    else:
        form = NewsWrite(request.form)
        if form.validate():
            title = form.title.data
            category_id = form.category_id.data
            digest = form.digest.data
            content = form.content.data
            new = News(title=title, content=content, author="Junyue", digest=digest, source="东湖日报")
            db.session.add(new)
            db.session.commit()
            message = "提交成功"
            time = datetime.now()
            send_time = time.strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "title": title,
                "category_id": category_id,
                "digest": digest,
                "content": content,
                "author": "Junyue",
                "source": "东湖日报",
                "send_time": send_time
            }
            flag = 1
            news_info = []
            # 将前端提交的新闻渲染到页面
            if flag:
                news_info.append(data)
                return render_template('front/front_index.html', news_info=news_info)
            else:
                return render_template('front/news_editor.html', message=message)
        else:
            return redirect(url_for('cms.profile'))


