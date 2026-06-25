from flask import Blueprint, request, jsonify, session
from datetime import datetime

from database import db
from models.rfq import RFQ
from models.vendor import Vendor
from utils.logger import log_activity
from flask_jwt_extended import jwt_required

rfq_bp = Blueprint(
    "rfq",
    __name__
)

@rfq_bp.route(
    "/rfqs",
    methods=["POST"]
)
@jwt_required()
def create_rfq():

    data = request.json

    rfq = RFQ(
        title=data["title"],
        category=data["category"],
        description=data["description"],
        quantity=data["quantity"],
        deadline=datetime.strptime(
            data["deadline"],
            "%Y-%m-%d"
        ).date(),
        created_by=session["user_id"]
    )

    

    db.session.add(rfq)
    db.session.commit()
    log_activity(
        action="RFQ Created",
        entity_type="RFQ",
        entity_id=rfq.id,
        user_id=rfq.created_by
    )

    return jsonify({
        "message": "RFQ created successfully",
        "rfq_id": rfq.id
    }), 201

@rfq_bp.route(
    "/rfqs",
    methods=["GET"]
)
@jwt_required()
def get_rfqs():

    rfqs = RFQ.query.all()

    result = []

    for rfq in rfqs:

        result.append({
            "id": rfq.id,
            "title": rfq.title,
            "category": rfq.category,
            "description": rfq.description,
            "quantity": rfq.quantity,
            "deadline": str(rfq.deadline),
            "status": rfq.status,
            "created_by": rfq.created_by
        })

    return jsonify(result), 200

@rfq_bp.route(
    "/rfqs/<int:rfq_id>",
    methods=["GET"]
)
def get_rfq(rfq_id):

    rfq = RFQ.query.get(rfq_id)

    if not rfq:
        return jsonify({
            "message": "RFQ not found"
        }), 404

    return jsonify({
        "id": rfq.id,
        "title": rfq.title,
        "category": rfq.category,
        "description": rfq.description,
        "quantity": rfq.quantity,
        "deadline": str(rfq.deadline),
        "status": rfq.status,
        "created_by": rfq.created_by
    }), 200

@rfq_bp.route(
    "/rfqs/<int:rfq_id>/vendors",
    methods=["POST"]
)
def assign_vendors(rfq_id):

    rfq = RFQ.query.get(rfq_id)

    if not rfq:
        return jsonify({
            "message": "RFQ not found"
        }), 404

    data = request.json

    vendor_ids = data.get("vendor_ids", [])

    for vendor_id in vendor_ids:

        vendor = Vendor.query.get(vendor_id)

        if vendor:
            rfq.vendors.append(vendor)
    
    db.session.commit()
    log_activity(
        action="Vendor Assigned to RFQ",
        entity_type="RFQ",
        entity_id=rfq.id,
        user_id=session.get("user_id")
    )


    return jsonify({
        "message": "Vendors assigned successfully"
    }), 200

@rfq_bp.route(
    "/rfqs/<int:rfq_id>/vendors",
    methods=["GET"]
)
def get_rfq_vendors(rfq_id):

    rfq = RFQ.query.get(rfq_id)

    if not rfq:
        return jsonify({
            "message": "RFQ not found"
        }), 404

    result = []

    for vendor in rfq.vendors:
        result.append({
            "id": vendor.id,
            "company_name": vendor.company_name
        })

    return jsonify(result)

