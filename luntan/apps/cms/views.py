from flask import Blueprint, render_template, views, request, session, redirect, url_for, g, flash, Response, jsonify
from .forms import LoginForm, ChangeSecret, NewsWrite, Register
from .models import CMSUser
from ..front.models import News, Comment
import config
from .decorators import login_required
from exts import db
import json


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
            new = News(title=title, content=content, author=g.cms_user.username, digest=digest, source="东湖日报")
            db.session.add(new)
            db.session.commit()
            message = "<script>alert('新闻提交成功')</script>"
            return render_template("front/news_editor.html", message=message)
        else:
            message = "<script>alert('新闻内容填写不完整，提交失败')</script>"
            return render_template("front/news_editor.html", message=message)


# 查询所有新闻信息
def search_news():
    all_news = News.query.order_by(News.id.desc()).all()
    news_list = []
    for new in all_news:
        news_info = {}
        news_info["id"] = new.id
        news_info["title"] = new.title
        news_info["content"] = new.content
        news_info["author"] = new.author
        news_info["source"] = new.source
        news_info["send_time"] = new.send_time
        news_info["digest"] = new.digest
        news_list.append(news_info)
    return news_list


# 将数据从数据库查出来，渲染到页面    每次加载新闻页
@bp.route('/load_news/', endpoint="load_news")
def load_news():
    news_list = search_news()
    return render_template("front/front_index.html", news_list=news_list)


# 跳转到详情页
@bp.route("/news_detail/<new_id>/")
def news_detail(new_id):
    new_info = News.query.filter_by(id=new_id).first()
    # print(new_info.content)
    return render_template("front/front_detail.html", new_info=new_info)



# 管理所有提交的新闻列表
@bp.route('/control_news/', endpoint="control_news")
def control_news():
    news_list = search_news()[::-1]
    return render_template('front/front_news_list.html', news_list=news_list)


# 删除新闻列表中的新闻
@bp.route('/delete_new/<int:new_id>/', endpoint="delete_new")
def delete_new(new_id):
    new = News.query.filter_by(id=new_id).first()
    db.session.delete(new)
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
            print(g.cms_user.username)
            author = g.cms_user.username
            News.query.filter_by(id=new_id).update({
                "title": title,
                "digest": digest,
                "content": content,
                "author": author
            })
            db.session.commit()
            message = "<script>alert('新闻编辑成功')</script>"
            return render_template("front/news_editor.html", message=message)
        else:
            message = "<script>alert('新闻内容填写不完整，提交失败')</script>"
            return render_template("front/news_editor.html", message=message)


# # 将前台提交的数据存储到数据库
# # @bp.route('/comment/', methods=["POST", "GET"], endpoint='comment')
# # def comment():
# #     if request.method == "POST":
# #         form = CommentList(request.form)
# #         if form.validate():
# #             comment_input = form.comment_input.data
# #             new_id = form.new_id.data
# #             comment = Comment(comment=comment_input, author=g.cms_user.username)
# #             db.session.add(comment)
# #             db.session.commit()
# #             # return redirect(url_for('cms.news_detail', id=new_id))
# #             return "ok"
# #         else:
# #             return render_template('front/404.html')
# #     else:
# #         return "shibai"


# 将前台提交的数据存储到数据库
@bp.route('/comment/', methods=["POST", "GET"], endpoint='comment')
def comment():

    # user_comment = request.form.get('user_comment')
    # comment = Comment(comment=user_comment, author=g.cms_user.username)
    # db.session.add(comment)
    # db.session.commit()
    data = {
        "user_comment": "haode"
    }
    return json.dumps(data)
    # return redirect(url_for('cms.load_news', data=data))

