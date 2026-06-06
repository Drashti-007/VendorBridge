from flask import Blueprint, jsonify
from models.activity_log import ActivityLog
from models.user import User

activity_bp = Blueprint("activity", __name__)

@activity_bp.route("/activities", methods=["GET"])
def get_activities():

    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()

    result = []

    for log in logs:

        user = User.query.get(log.user_id)

        result.append({
            "id": log.id,
            "title": log.action,
            "description": log.action,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,

            "performed_by": {
                "user_id": log.user_id,
                "role": user.role if user else "unknown"
            },

            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(result), 200