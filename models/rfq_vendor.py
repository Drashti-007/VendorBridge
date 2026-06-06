from database import db

rfq_vendors = db.Table(
    "rfq_vendors",

    db.Column(
        "rfq_id",
        db.Integer,
        db.ForeignKey("rfqs.id"),
        primary_key=True
    ),

    db.Column(
        "vendor_id",
        db.Integer,
        db.ForeignKey("vendors.id"),
        primary_key=True
    )
)