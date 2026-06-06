from database import db

class PurchaseOrder(db.Model):

    __tablename__ = "purchase_orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quotation_id = db.Column(
        db.Integer,
        db.ForeignKey("quotations.id")
    )

    po_number = db.Column(
        db.String(50),
        unique=True
    )

    status = db.Column(
        db.String(30),
        default="Generated"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )