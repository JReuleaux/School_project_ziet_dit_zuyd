from flask import session, redirect
from functools import wraps


def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect('/')
            if session.get('role') == -1:  
                session.clear()
                return redirect('/')
            if role is not None and session.get('role') < role:
                return "Geen toegang!", 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

