from database import db
from models.activity_log import ActivityLog


def log_activity(action, entity_type, entity_id, user_id):

    log = ActivityLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id
    )

    db.session.add(log)
    db.session.commit()