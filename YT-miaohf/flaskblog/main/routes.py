from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='home')

@main.route("/about")
def about():
    return render_template('about.html', title='About')



