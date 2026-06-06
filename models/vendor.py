from database import db

class Vendor(db.Model):

    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    gst_number = db.Column(
        db.String(50),
        unique=True
    )

    contact_person = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    phone = db.Column(
        db.String(20)
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )