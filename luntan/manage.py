from flask_script import Manager
from luntan import create_app
from apps.cms import models as cms_models
from flask_migrate import Migrate, MigrateCommand
from exts import db
from apps.front import models as front_models


CMSUser = cms_models.CMSUser
News = front_models.News
app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.option("-u", "--username", dest="username")
@manager.option("-p", "--password", dest="password")
@manager.option("-e", "--email", dest="email")
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")


@manager.option("-u", "--usernmae", dest="username")
@manager.option("-nu", "--new_username", dest="new_username")
def change(username, new_username):
    user = CMSUser.query.filter_by(username=username).first()
    user.username = new_username
    db.session.commit()
    print("更改用户名成功")


@manager.option("-p", "--password", dest="password")
@manager.option("-np", "--new_password", dest="new_password")
def change_secret(password, new_password):
    user = CMSUser.query.filter_by(password=password).first()
    user.password = new_password
    db.session.commit()
    print("密码修改成功")

@manager.option("-e", "--email", dest="email")
@manager.option("-ne", "--new_email", dest="new_email")
def change_secret(email, new_email):
    user = CMSUser.query.filter_by(email=email).first()
    user.password = new_email
    db.session.commit()
    print("邮箱修改成功")


@manager.option("-t", "--title", dest="title")
@manager.option("-c", "--content", dest="content")
@manager.option("-a", "--author", dest="author")
def create_news(title, content, author):
    news = News(title=title, content=content, author=author)
    db.session.add(news)
    db.session.commit()
    print("新闻添加成功")



if __name__ == "__main__":
    manager.run()