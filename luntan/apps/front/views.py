from flask import Blueprint, render_template, redirect, url_for
from .models import News
import config
from ..cms.decorators import login_required


bp = Blueprint('front', __name__, url_prefix="/front")


# 新闻首页
# 将数据从数据库查出来，渲染到页面    每次加载新闻页
@bp.route('/')
def index():
    return redirect(url_for("cms.load_news") )


# # 新闻详情页
# @bp.route('/detail/<int:page>/')
# def detail(page):
#     news = News.query.filter_by(id=page).first()
#     if news:
#         return render_template('front/front_detail.html', news=news)
#     else:
#         return render_template('front/404.html')




