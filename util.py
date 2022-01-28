from functools import wraps
from flask import g, request, redirect, url_for, session, flash

# Login Required Decorator SAMPLE
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function


def requires_login(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login!', 'danger')
            return redirect(url_for('login'))
    return decorated_func



