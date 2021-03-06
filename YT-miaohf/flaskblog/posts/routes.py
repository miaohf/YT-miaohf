from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Postdtl
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    postdtls = Postdtl.query.filter(Postdtl.ytid==post.ytid)
    return render_template('post.html', title=post.title, post=post, postdtls=postdtls)


@posts.route("/post/cust/<int:custid>")
@login_required
def postcust(custid):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(custid=custid).order_by(Post.date_posted.desc()).paginate(page=page, per_page=25)
    return render_template('tuozhan.html', posts=posts, custid=custid)

@posts.route("/post/cust/<int:custid>/dtl")
@login_required
def postcustdtl(custid):

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(custid=custid).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2500)
    #return render_template('tuozhan.html', posts=posts)

    #posts = Post.query.filter_by(custid=custid).order_by(Post.date_posted.desc())
    postdtls = Postdtl.query.join(Post,Postdtl.ytid==Post.ytid).filter(Post.custid==custid). \
    with_entities(Post.customer, \
        Post.date_posted, \
        Postdtl.ytid, \
        Postdtl.businame, \
        Postdtl.busisubname, \
        Postdtl.busisubunit, \
        Postdtl.receiveprice, \
        Postdtl.renderimg, \
        Postdtl.create_time, \
        Postdtl.copys, \
        Postdtl.numexp, \
        Postdtl.remark
        ).order_by(Postdtl.ytid)
    return render_template('postbycust.html',  posts=posts, postdtls=postdtls)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data1
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
