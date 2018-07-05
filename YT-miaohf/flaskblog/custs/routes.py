from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post

custs = Blueprint('custs', __name__)


@custs.route("/custs/<int:custid>")
def customers(custid):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(custid=custid).order_by(Post.date_posted.desc()).paginate(page=page, per_page=27)
    return render_template('custs.html', posts=posts, custid=custid)
