from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSUser(db.Model):
    __tablename__ = "cms_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #
    # # 对外字段   password
    # # 对内字段   _password
    # @property
    # def password(self):
    #     return self._password
    #
    # @password.setter
    # def password(self, raw_password):
    #     self._password = generate_password_hash(raw_password)
    #
    # # 第一个参数  加密后的代码
    # # 第二个参数  新的密码
    # # 先将密码进行加密，然后跟数据库中的密码进行比对，如果相同，正确，否则错误
    # def check_password(self, raw_password):
    #     result = check_password_hash(self.password, raw_password)
    #     return result
