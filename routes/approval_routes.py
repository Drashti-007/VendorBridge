from flask import Blueprint, request, jsonify

from database import db
from models.approval import Approval
from models.quotation import Quotation
from utils.logger import log_activity

approval_bp = Blueprint(
    "approval",
    __name__
)

@approval_bp.route(
    "/approvals",
    methods=["POST"]
)
def approve_quotation():

    data = request.json

    quotation = Quotation.query.get(
        data["quotation_id"]
    )

    if not quotation:
        return jsonify({
            "message": "Quotation not found"
        }), 404

    approval = Approval(
        quotation_id=data["quotation_id"],
        manager_id=data["manager_id"],
        status=data["status"],
        remarks=data.get("remarks")
    )

    db.session.add(approval)
    db.session.commit()

    log_activity(
        action="Quotation Approved",
        entity_type="Approval",
        entity_id=approval.id,
        user_id=approval.manager_id
    )

    return jsonify({
        "message": "Approval recorded successfully",
        "approval_id": approval.id
    }), 201
@approval_bp.route(
    "/approvals",
    methods=["GET"]
)
def get_approvals():

    approvals = Approval.query.all()

    result = []

    for approval in approvals:

        result.append({
            "id": approval.id,
            "quotation_id": approval.quotation_id,
            "manager_id": approval.manager_id,
            "status": approval.status,
            "remarks": approval.remarks,
            "approved_at": str(
                approval.approved_at
            )
        })

    return jsonify(result), 200