from database import db


class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    po_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.id"),
        nullable=False
    )

    invoice_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    subtotal = db.Column(
        db.Float,
        nullable=False
    )

    tax_percent = db.Column(
        db.Float,
        default=18
    )

    tax_amount = db.Column(
        db.Float,
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Generated"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )