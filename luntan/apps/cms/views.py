# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, views, request, session, redirect, url_for, g, flash, Response, jsonify
from .forms import LoginForm, ChangeSecret, NewsWrite, Register, ChangeXinxi, ResetPwdForm
from .models import CMSUser
from ..front.models import News, Comment
import config
from .decorators import login_required
from exts import db
from flask_paginate import Pagination, get_page_parameter
from utils import aliyun_sms
from utils import cache


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


# 用户注册
@bp.route('/register/', endpoint='register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form = Register(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = CMSUser(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
        # return render_template('cms/cms_login.html', register_info="<script>alert('注册成功')</script>")
        return redirect(url_for('cms.login'))
    else:
        return render_template('cms/cms_register.html')


# 更换密码
class ChangeView(views.MethodView):
    decorators = [login_required]

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


bp.add_url_rule('/change/', view_func=ChangeView.as_view('change'))


# 电话号码验证
@bp.route('/telephone_validate/', methods=["POST", "GET"])
def telephone_validate():
    if request.method == "GET":
        return render_template('cms/cms_telephone_validate.html')
    else:
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        print(telephone)
        user = CMSUser.query.filter_by(email=email).first()
        print(user)
        if user:
            string = aliyun_sms.random_number()
            code_dict = {"code": string}
            cache.set("validate_code", string)
            aliyun_sms.aliyun_code(telephone, code_dict)
            message = "验证码发送成功, 如果接收不到短信，请过60s后请求"
            return jsonify({"message": message})
        else:
            message = "邮箱不存在"
            return jsonify({"message": message})


# 验证验证码
@bp.route('/validate_code/', methods=["POST"])
def validate_code():
    email = request.form.get("email")
    code = request.form.get("validate_code")
    user = CMSUser.query.filter_by(email=email).first()
    print(user)
    if user and cache.get("validate_code") == code:
        # print("ok")
        return jsonify({"message": "验证成功"})
    else:
        return jsonify({"message": "验证码填写错误或者邮箱填写与之前不一致"})


# 重置密码
class ResetPwdView(views.MethodView):
    def get(self):
        return render_template('cms/cms_reset_secret.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            email = form.email.data
            password_repeat = form.password_repeat.data
            user = CMSUser.query.filter_by(email=email).first()
            if user:
                user.password = password_repeat
                db.session.commit()
                return redirect(url_for('cms.login'))
            else:
                message = "密码重置失败， 请重试"
                return render_template('cms/cms_reset_secret.html', message=message)
        else:
            return render_template('front/404.html')


bp.add_url_rule('/reset_secret/',view_func=ResetPwdView.as_view('reset_secret'))















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
            new = News(title=title, content=content, author=g.cms_user.username, digest=digest, source="东湖日报", category_id=category_id)
            db.session.add(new)
            db.session.commit()
            message = "<script>alert('新闻提交成功')</script>"
            return render_template("front/news_editor.html", message=message)
        else:
            message = "<script>alert('新闻内容填写不完整，提交失败')</script>"
            return render_template("front/news_editor.html", message=message)


# 查询所有新闻信息(垃圾站)
def search_news(status_code):
    all_news = News.query.filter_by(status=status_code).all()
    return all_news


# 查询所有新闻（分页显示）
def query_news(step, status_code):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * step
    end = start + step
    query_obj = News.query.filter_by(status=status_code).all()
    query_obj = query_obj[::-1]
    new_total = len(query_obj)
    news = query_obj[start:end]
    pagination = Pagination(bs_version=3, page=page, total=new_total, inner_window=2, outer_window=0)
    context = {
        'pagination': pagination,
        'news': news
    }
    return context


# 将数据从数据库查出来，渲染到页面    每次加载新闻页
@bp.route('/load_news/', endpoint="load_news")
def load_news():
    context = query_news(step=config.PER_PAGE, status_code=1)
    return render_template("front/front_index.html", **context)


# 跳转到详情页
@bp.route("/news_detail/<new_id>/", methods=["POST", "GET"])
def news_detail(new_id):
    new_info = News.query.filter_by(id=new_id).first()
    comments = Comment.query.filter_by(new_id=new_id).all()
    # print(comments)
    comment_list = []
    for comment in comments:
        comment_info = {}
        comment_info['comment'] = comment.comment
        comment_info['author'] = comment.author
        comment_info['comment_time'] = comment.comment_time
        comment_list.append(comment_info)
    # print(new_info.content)
    comment_list = comment_list[::-1]
    return render_template("front/front_detail.html", new_info=new_info, comment_list=comment_list)


# 管理所有提交的新闻列表
@bp.route('/control_news/', endpoint="control_news")
@login_required
def control_news():
    # news_list = search_news(status_code=1)[::-1]
    context = query_news(step=50, status_code=1)
    return render_template('front/front_news_list.html', **context)


# 删除新闻列表中的新闻
@bp.route('/delete_new/<int:new_id>/', endpoint="delete_new")
def delete_new(new_id):
    News.query.filter_by(id=new_id).update({"status": 0})
    db.session.commit()
    return redirect(url_for('cms.control_news'))


#  编辑新闻列表中的新闻
@bp.route('/edit_new/<int:new_id>/', endpoint="edit_new", methods=["POST", "GET"])
@login_required
def edit_new(new_id):
    if request.method == "GET":
        new = News.query.filter_by(id=new_id).first()
        return render_template('front/front_edit_new.html', new=new)
    else:
        form = NewsWrite(request.form)
        if form.validate():
            title = form.title.data
            digest = form.digest.data
            content = form.content.data
            category_id = form.category_id.data
            # print(g.cms_user.username)
            author = g.cms_user.username
            News.query.filter_by(id=new_id).update({
                "title": title,
                "digest": digest,
                "content": content,
                "author": author,
                "category_id": category_id
            })
            db.session.commit()
            message = "<script>alert('新闻编辑成功')</script>"
            return render_template("front/news_editor.html", message=message)
        else:
            message = "<script>alert('新闻内容填写不完整，提交失败')</script>"
            return render_template("front/news_editor.html", message=message)


# 垃圾回收站
@bp.route('/garbage/')
def garbage():
    all_news = search_news(status_code=0)
    return render_template('front/front_garbage.html', all_news=all_news)


# 从垃圾回收站还原新闻
@bp.route('/restore_new/<int:new_id>/', endpoint="restore_new")
def restore_new(new_id):
    News.query.filter_by(id=new_id).update({"status": 1})
    db.session.commit()
    return redirect(url_for('cms.garbage'))


# 将前台提交的评论存储到数据库
@bp.route('/comment/', methods=["POST", "GET"], endpoint='comment')
@login_required
def comment():
    if request.method == "POST":
        user_comment = request.form.get('user_comment')
        new_id = request.form.get("new_id")
        print(user_comment)
        comment = Comment(comment=user_comment, author=g.cms_user.username, new_id=new_id)
        db.session.add(comment)
        db.session.commit()
        return jsonify({"data": user_comment})
    else:
        data = {
            "user_comment": "ok"
        }
        print("GET")
        return jsonify(data)
    # return redirect(url_for('cms.load_news', data=data))


# 添加测试数据
@bp.route("/test/")
def test():
    for i in range(100):
        new = News(title='title %s' % i, digest='digest %s' % i, content='content %s' % i)
        db.session.add(new)
        db.session.commit()
    return Response("OK")











# 修改个人信息
class ChangeXinXi(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_change_xinxi.html')
    def post(self):
        form=ChangeXinxi(request.form)
        print("form")
        if form.validate():
            old_username=form.old_username.data
            username_repeat=form.username_repeat.data
            user=CMSUser.query.filter_by(username=old_username).first()
            print("user")
            if user:
                user.username=username_repeat
                db.session.commit()
                flash("用户名修改成功，请重新登录")
                return redirect(url_for('cms.profile'))
            else:
                flash("修改用户名失败,重新输入")
                return redirect(url_for('cms.change_xinxi'))
        else:
            flash("修改用户名失败")
            return redirect(url_for('cms.change_xinxi'))


bp.add_url_rule('/change_xinxi/',view_func=ChangeXinXi.as_view('change_xinxi'))