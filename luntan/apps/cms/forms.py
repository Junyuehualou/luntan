from ..forms import BaseForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱类型"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的密码")])
    remember = IntegerField()


class ChangeSecret(BaseForm):
    old_password = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的密码")])
    new_password = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的密码")])
    password_repeat = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的密码"),
                                              EqualTo("new_password", message="两次输入的密码不一致")])

    submit = SubmitField()


class NewsWrite(BaseForm):
    title = StringField(validators=[InputRequired(message="新闻标题不能为空")])
    category_id = IntegerField()
    digest = TextAreaField(validators=[InputRequired(message="新闻摘要不能为空")])
    content = TextAreaField(validators=[InputRequired(message="新闻内容不能为空")])
    submit = SubmitField()


class Register(BaseForm):
    username = StringField(validators=[InputRequired(message="用户名是必填字段")])
    email = StringField(validators=[Email(message="请输入正确的邮箱类型"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的密码")])


class CommentList(BaseForm):
    comment_input = TextAreaField(validators=[InputRequired(message="评论不能为空")])
    submit = SubmitField()
    new_id = IntegerField()


class ChangeXinxi(BaseForm):
    old_username = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的用户名")])
    new_username = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的用户名")])
    username_repeat = StringField(validators=[Length(min=6, max=20, message="请输入正确格式的用户名"),
                                              EqualTo("new_username", message="两次输入的用户名不一致")])
    submit = SubmitField()