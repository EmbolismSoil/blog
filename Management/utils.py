from functools import wraps
from flask_login import current_user
from flask import redirect, url_for
import platform


def admin_required(func):
    @wraps(func)
    def wrap_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('management.management_login'))

        if current_user.is_administrator():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('management.management_login'))

    return wrap_view


def get_sys_info():
    sys_info = {'platform': platform.platform()}
    return sys_info