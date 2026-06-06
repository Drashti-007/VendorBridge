from flask import Blueprint, request, jsonify

from database import db
from models.quotation import Quotation
from models.rfq import RFQ
from models.vendor import Vendor
from utils.logger import log_activity


quotation_bp = Blueprint(
    "quotation",
    __name__
)

@quotation_bp.route(
    "/quotations",
    methods=["POST"]
)
def create_quotation():

    data = request.json

    rfq = RFQ.query.get(
        data["rfq_id"]
    )

    if not rfq:
        return jsonify({
            "message": "RFQ not found"
        }), 404

    vendor = Vendor.query.get(
        data["vendor_id"]
    )

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }), 404

    quotation = Quotation(
        rfq_id=data["rfq_id"],
        vendor_id=data["vendor_id"],
        price=data["price"],
        delivery_days=data["delivery_days"],
        notes=data.get("notes")
    )

    db.session.add(quotation)
    db.session.commit()

    log_activity(
        action="Quotation Submitted",
        entity_type="Quotation",
        entity_id=quotation.id,
        user_id=quotation.vendor_id
    )

    return jsonify({
        "message": "Quotation submitted successfully",
        "quotation_id": quotation.id
    }), 201

@quotation_bp.route(
    "/rfqs/<int:rfq_id>/quotations",
    methods=["GET"]
)
def get_quotations(rfq_id):

    quotations = Quotation.query.filter_by(
        rfq_id=rfq_id
    ).all()

    result = []

    for quotation in quotations:

        vendor = Vendor.query.get(
            quotation.vendor_id
        )

        result.append({
            "quotation_id": quotation.id,
            "vendor_name": vendor.company_name,
            "price": quotation.price,
            "delivery_days": quotation.delivery_days,
            "status": quotation.status
        })

    return jsonify(result), 200
@quotation_bp.route(
    "/rfqs/<int:rfq_id>/compare",
    methods=["GET"]
)
def compare_quotations(rfq_id):

    quotations = Quotation.query.filter_by(
        rfq_id=rfq_id
    ).order_by(
        Quotation.price.asc()
    ).all()

    result = []

    for quotation in quotations:

        vendor = Vendor.query.get(
            quotation.vendor_id
        )

        result.append({
            "vendor": vendor.company_name,
            "price": quotation.price,
            "delivery_days": quotation.delivery_days
        })

    return jsonify(result), 200