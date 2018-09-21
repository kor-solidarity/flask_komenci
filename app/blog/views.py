from app import app
from flask import render_template, redirect, flash, url_for, session, abort
from blog.form import SetupForm, PostForm
from app import db
from author.models import Author
from blog.models import Blog, Category, Post
from author.decorators import login_required, author_required
import bcrypt
from _global_constant import *
from slugify import slugify


@app.route('/')
@app.route('/index')
def index():
    blogs = Blog.query.count()
    if blogs == 0:
        return redirect(url_for('setup'))
    return 'hi!'


@app.route('/admin')
@author_required
def admin():
    if session.get('is_author'):
        return render_template('blog/admin.html')
    else:
        abort(403)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = SetupForm()
    error = ''
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hash_pass = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)

        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hash_pass,
            True
        )
        db.session.add(author)
        db.session.flush()
        if author.id:
            blog = Blog(
                form.name.data,
                author.id
            )
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = 'ERROR creating user'

        if author.id and blog.id:
            db.session.commit()
            flash('blog created')
            return redirect(url_for('admin'))
        else:
            db.session.rollback()
            error = 'error making blog'

        # flash()

    return render_template('blog/setup.html', form=form, error=error)


@app.route('/post', methods=get_post)
@author_required
def post():
    # return 'blogpost'
    form = PostForm()

    if form.validate_on_submit():
        if form.new_category.data:
            new_cat = Category(form.new_category.data)
            db.session.add(new_cat)
            db.session.flush()
            category = new_cat
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data)
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = None
        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog, author, title, body, category, slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('blog/post.html', form=form)


@app.route('/article')
@login_required
def article():
    return render_template('blog/article.html')
