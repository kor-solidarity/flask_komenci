from app import app
from flask import render_template, redirect, flash, url_for, session, abort
from blog.form import SetupForm
from app import db
from author.models import Author
from blog.models import Blog
from author.decorators import login_required, author_required
import bcrypt
from _global_constant import *


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
    return 'blogpost'


@app.route('/article')
@login_required
def article():
    return render_template('blog/article.html')
