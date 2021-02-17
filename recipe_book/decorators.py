from functools import wraps

from flask import current_app, request, redirect, url_for
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS


__all__ = ('anonymous_required', )


def anonymous_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif current_user.is_authenticated:
            # TODO: redirect to "already authorized"
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return decorated_view
