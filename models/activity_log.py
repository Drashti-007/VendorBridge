from database import db


class ActivityLog(db.Model):

    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(
        db.String(200),
        nullable=False
    )

    entity_type = db.Column(
        db.String(50)
    )  # RFQ / Vendor / PO / Invoice

    entity_id = db.Column(
        db.Integer
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )