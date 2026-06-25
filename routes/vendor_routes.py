from flask import Blueprint, request, jsonify

from database import db
from models.vendor import Vendor
from auth.decorators import role_required
from flask_jwt_extended import jwt_required

vendor_bp = Blueprint(
    "vendor",
    __name__
)

@vendor_bp.route(
    "/vendors",
    methods=["POST"]
)
@jwt_required()
@role_required("admin")
def create_vendor():

    data = request.json

    if not data.get("company_name"):
        return jsonify({
            "message": "Company name is required"
        }), 400

    vendor = Vendor(
        company_name=data["company_name"],
        category=data.get("category"),
        gst_number=data.get("gst_number"),
        contact_person=data.get("contact_person"),
        email=data.get("email"),
        phone=data.get("phone")
    )

    db.session.add(vendor)
    db.session.commit()

    return jsonify({
        "message": "Vendor created successfully",
        "vendor_id": vendor.id
    }), 201

@vendor_bp.route(
    "/vendors",
    methods=["GET"]
)
@jwt_required()
def get_vendors():

    vendors = Vendor.query.all()

    result = []

    for vendor in vendors:

        result.append({
            "id": vendor.id,
            "company_name": vendor.company_name,
            "category": vendor.category,
            "email": vendor.email,
            "status": vendor.status
        })

    return jsonify(result)

@vendor_bp.route(
    "/vendors/<int:vendor_id>",
    methods=["GET"]
)
def get_vendor(vendor_id):

    vendor = Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }), 404

    return jsonify({
        "id": vendor.id,
        "company_name": vendor.company_name,
        "category": vendor.category,
        "gst_number": vendor.gst_number,
        "contact_person": vendor.contact_person,
        "email": vendor.email,
        "phone": vendor.phone,
        "status": vendor.status
    })

@vendor_bp.route(
    "/vendors/<int:vendor_id>",
    methods=["PUT"]
)
def update_vendor(vendor_id):

    vendor = Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }), 404

    data = request.json

    vendor.company_name = data.get(
        "company_name",
        vendor.company_name
    )

    vendor.category = data.get(
        "category",
        vendor.category
    )

    vendor.contact_person = data.get(
        "contact_person",
        vendor.contact_person
    )

    vendor.email = data.get(
        "email",
        vendor.email
    )

    vendor.phone = data.get(
        "phone",
        vendor.phone
    )

    vendor.status = data.get(
        "status",
        vendor.status
    )

    db.session.commit()

    return jsonify({
        "message": "Vendor updated successfully"
    })

@vendor_bp.route(
    "/vendors/<int:vendor_id>",
    methods=["DELETE"]
)
def delete_vendor(vendor_id):

    vendor = Vendor.query.get(vendor_id)

    if not vendor:
        return jsonify({
            "message": "Vendor not found"
        }), 404

    db.session.delete(vendor)
    db.session.commit()

    return jsonify({
        "message": "Vendor deleted successfully"
    })
