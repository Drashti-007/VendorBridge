from database import db
from models.rfq_vendor import rfq_vendors

class RFQ(db.Model):

    __tablename__ = "rfqs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )
    
    category = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    deadline = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Open"
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    vendors = db.relationship(
    "Vendor",
    secondary=rfq_vendors,
    backref="rfqs"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

class RFQItem(db.Model):

    __tablename__ = "rfq_items"

    id = db.Column(db.Integer, primary_key=True)

    rfq_id = db.Column(
        db.Integer,
        db.ForeignKey("rfqs.id")
    )

    item_name = db.Column(
        db.String(100),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    unit = db.Column(
        db.String(20)
    )