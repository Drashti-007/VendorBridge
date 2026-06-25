from flask import Blueprint, jsonify

from models.activity_log import ActivityLog
activity_bp = Blueprint(
    "activity",
    __name__
)

@activity_bp.route(
    "/activities",
    methods=["GET"]
)
def get_activities():

    activities = ActivityLog.query.all()

    result = []

    for activity in activities:

        result.append({
            "id": activity.id,
            "user_id": activity.user_id,
            "action": activity.action,
            "entity_type": activity.entity_type,
            "entity_id": activity.entity_id,
            "timestamp": str(
                activity.timestamp
            )
        })

    return jsonify(result), 200