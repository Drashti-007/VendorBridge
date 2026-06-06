from functools import wraps
from flask import session, jsonify

def role_required(role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if session.get("role") != role:
                return jsonify({
                    "message": "Unauthorized"
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator