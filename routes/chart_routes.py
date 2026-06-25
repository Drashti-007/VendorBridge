from flask import Blueprint, jsonify

from models.rfq import RFQ
from models.invoice import Invoice
from models.approval import Approval

chart_bp = Blueprint(
    "chart",
    __name__
)

@chart_bp.route(
    "/charts/rfq-status",
    methods=["GET"]
)
def rfq_chart():

    open_count = RFQ.query.filter_by(
        status="Open"
    ).count()

    closed_count = RFQ.query.filter_by(
        status="Closed"
    ).count()

    return jsonify({
        "Open": open_count,
        "Closed": closed_count
    })

@chart_bp.route(
    "/charts/invoice-status",
    methods=["GET"]
)
def invoice_chart():

    generated = Invoice.query.filter_by(
        status="Generated"
    ).count()

    paid = Invoice.query.filter_by(
        status="Paid"
    ).count()

    return jsonify({
        "Generated": generated,
        "Paid": paid
    })

@chart_bp.route(
    "/charts/approvals",
    methods=["GET"]
)
def approval_chart():
    
    approved = Approval.query.filter_by(
        status="Approved"
    ).count()

    rejected = Approval.query.filter_by(
        status="Rejected"
    ).count()

    return jsonify({
        "Approved": approved,
        "Rejected": rejected
    })