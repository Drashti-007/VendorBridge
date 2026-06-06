from database import db

class Quotation(db.Model):

    __tablename__ = "quotations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    rfq_id = db.Column(
        db.Integer,
        db.ForeignKey("rfqs.id")
    )

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendors.id")
    )

    price = db.Column(
        db.Float
    )

    delivery_days = db.Column(
        db.Integer
    )

    notes = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default="Submitted"
    )

    submitted_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )