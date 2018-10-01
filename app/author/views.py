from app import app
from flask import render_template, redirect, url_for, session, request
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

get = 'GET'
post = 'POST'


@app.route('/login', methods=[get, post])
def login():
    form = LoginForm()
    error = None

    if request.method == get and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(
            username=form.username.data,
        ).first()
        if author:
            print(bcrypt.hashpw(form.password.data.encode('utf8'), author.password.encode('utf8')))
            if bcrypt.hashpw(form.password.data.encode('utf8'), author.password.encode('utf8')) == author.password.encode('utf8'):
                session['username'] = form.username.data.encode('utf8')
                session['is_author'] = author.is_author
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                return redirect(url_for('index'))
            else:
                error = '틀린암호/계정임?????'
        else:
            error = '틀린암호/계정임.'

    return render_template('author/login.html', form=form, error=error)


@app.route('/register', methods=['POST', "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)


@app.route('/success')
def success():
    return '완료'


@app.route('/login_success')
@login_required
def login_success():
    return '로긴성공'


@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    return redirect(url_for('index'))


