from flask import Blueprint, jsonify

from models.user import User
from models.vendor import Vendor
from models.rfq import RFQ
from models.quotation import Quotation
from models.approval import Approval
from models.purchase_order import PurchaseOrder
from models.invoice import Invoice
from flask_jwt_extended import jwt_required

analytics_bp = Blueprint(
    "analytics",
    __name__
)

@analytics_bp.route(
    "/analytics",
    methods=["GET"]
)
@jwt_required()
def get_analytics():

    approved_quotations = Approval.query.filter_by(
        status="Approved"
    ).count()

    open_rfqs = RFQ.query.filter_by(
        status="Open"
    ).count()

    paid_invoices = Invoice.query.filter_by(
        status="Paid"
    ).count()

    data = {
        "total_users": User.query.count(),
        "total_vendors": Vendor.query.count(),
        "total_rfqs": RFQ.query.count(),
        "total_quotations": Quotation.query.count(),
        "total_approvals": Approval.query.count(),
        "total_purchase_orders": PurchaseOrder.query.count(),
        "total_invoices": Invoice.query.count(),
        "approved_quotations": approved_quotations,
        "open_rfqs": open_rfqs,
        "paid_invoices": paid_invoices
    }

    return jsonify(data), 200

