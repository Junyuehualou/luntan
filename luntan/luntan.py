from flask import Flask
from exts import db
import config
from flask_wtf import CSRFProtect   # 表单提交防止跨站请求伪造
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)

    app.config.from_object(config)  # 导入配置文件 生效
    db.init_app(app)
    CSRFProtect(app)
    return app


app = create_app()




if __name__ == '__main__':
    app = create_app()
    app.run()
