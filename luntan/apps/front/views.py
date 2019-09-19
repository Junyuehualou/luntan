from flask import Blueprint, render_template
from .models import News
import config
from ..cms.decorators import login_required


bp = Blueprint('front', __name__, url_prefix="/front")


# 新闻首页
@bp.route('/')
def index():
    return render_template('front/front_index.html')


# 新闻详情页
@bp.route('/detail/<int:page>/')
def detail(page):
    news = News.query.filter_by(id=page).first()
    if news:
        return render_template('front/front_detail.html', news=news)
    else:
        return render_template('front/404.html')




