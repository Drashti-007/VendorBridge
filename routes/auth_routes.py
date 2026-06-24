from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models.user import User
from database import db
from models.activity_log import ActivityLog

auth_bp = Blueprint(
    "auth",
    __name__
)

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    data = request.json

    # Check if email already exists
    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400

    hashed_password = generate_password_hash(
        data["password"]
    )

    new_user = User(   
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        password=hashed_password,
        role=data["role"],
        country=data.get("country"),
        additional_info=data.get("additional_info")
    )

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "password",
        "role"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    db.session.add(new_user)
    db.session.commit()

    activity = ActivityLog(
        user_id=new_user.id,
        action="Registered a new account"
    )

    db.session.add(activity)
    db.session.commit()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    return jsonify({
        "message": "User registered successfully"
    }), 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.json

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if not check_password_hash(
        user.password,
        data["password"]
    ):
        return jsonify({
            "message": "Invalid password"
        }), 401

    # Password is correct
    session["user_id"] = user.id
    session["role"] = user.role

    activity = ActivityLog(
        user_id = user.id,
        action = "Logged into the system"
    )

    db.session.add(activity)
    db.session.commit()

    if "email" not in data or "password" not in data:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    return jsonify({
        "message": "Login Success",
        "user_id": user.id,
        "role": user.role
    }), 200

@auth_bp.route(
    "/forgot-password",
    methods=["POST"]
)
def forgot_password():

    data = request.json

    email = data.get("email")
    new_password = data.get("new_password")

    if not email or not new_password:
        return jsonify({
            "message": "Email and new password are required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.password = generate_password_hash(
        new_password
    )

    db.session.commit()

    activity = ActivityLog(
        user_id=user.id,
        action="Reset account password"
    )

    db.session.add(activity)
    db.session.commit()

    return jsonify({
        "message": "Password updated successfully"
    }), 200