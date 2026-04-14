from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user, logout_user

def usuario_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login_usuario.login'))
        
        if not current_user.is_usuario:
            pass