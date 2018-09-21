from functools import wraps
from flask import session, request, redirect, url_for, abort


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_func


def author_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get('is_author') is None:
            abort(403)
        return f(*args, **kwargs)
    return decorated_func


