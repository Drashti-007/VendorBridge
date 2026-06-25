from flask import Blueprint, request, jsonify, session
import uuid

from database import db
from models.purchase_order import PurchaseOrder
from models.approval import Approval
from models.quotation import Quotation
from utils.logger import log_activity
from flask_jwt_extended import jwt_required

purchase_order_bp = Blueprint(
    "purchase_order",
    __name__
)

@purchase_order_bp.route(
    "/purchase-orders",
    methods=["POST"]
)
@jwt_required()
def create_purchase_order():

    data = request.json

    quotation = Quotation.query.get(
        data["quotation_id"]
    )

    if not quotation:
        return jsonify({
            "message": "Quotation not found"
        }), 404

    po = PurchaseOrder(
        quotation_id=quotation.id,

        po_number = f"PO-{uuid.uuid4().hex[:6].upper()}",
        status="Generated"
    )

    db.session.add(po)
    db.session.commit()

    log_activity(
        action="Purchase Order Generated",
        entity_type="PO",
        entity_id=po.id,
        user_id=session.get("user_id")
    )
    return jsonify({
        "message": "Purchase Order created successfully",
        "po_id": po.id,
        "po_number": po.po_number
    }), 201

@purchase_order_bp.route(
    "/purchase-orders",
    methods=["GET"]
)
def get_purchase_orders():

    purchase_orders = PurchaseOrder.query.all()

    result = []

    for po in purchase_orders:

        result.append({
            "id": po.id,
            "quotation_id": po.quotation_id,
            "po_number": po.po_number,
            "status": po.status,
            "created_at": str(po.created_at)
        })

    return jsonify(result), 200

@purchase_order_bp.route(
    "/purchase-orders/<int:po_id>",
    methods=["PUT"]
)
def update_po_status(po_id):

    po = PurchaseOrder.query.get(po_id)

    if not po:
        return jsonify({
            "message": "Purchase Order not found"
        }), 404

    data = request.json

    po.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "Status updated successfully"
    }), 200


