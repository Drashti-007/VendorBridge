from database import db

class Approval(db.Model):

    __tablename__ = "approvals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quotation_id = db.Column(
        db.Integer,
        db.ForeignKey("quotations.id")
    )

    manager_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    status = db.Column(
        db.String(30)
    )

    remarks = db.Column(
        db.Text
    )

    approved_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )