from flask import Blueprint, request, jsonify, session

from database import db
from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from utils.logger import log_activity

invoice_bp = Blueprint("invoice", __name__)

@invoice_bp.route("/invoices", methods=["POST"])
def create_invoice():

    data = request.json

    po = PurchaseOrder.query.get(data["po_id"])

    if not po:
        return jsonify({"message": "Purchase Order not found"}), 404

    # Dummy logic (since we don’t have line-item pricing system)
    subtotal = 50000  # you can later improve this
    tax_percent = data.get("tax_percent", 18)

    tax_amount = (subtotal * tax_percent) / 100
    total_amount = subtotal + tax_amount

    invoice = Invoice(
        po_id=po.id,
        invoice_number=f"INV-{po.id}",
        subtotal=subtotal,
        tax_percent=tax_percent,
        tax_amount=tax_amount,
        total_amount=total_amount
    )

    db.session.add(invoice)
    db.session.commit()

    log_activity(
        action="Invoice Generated",
        entity_type="Invoice",
        entity_id=invoice.id,
        user_id=session.get("user_id")
    )

    return jsonify({
        "message": "Invoice created successfully",
        "invoice_id": invoice.id,
        "total": total_amount
    }), 201

@invoice_bp.route("/invoices", methods=["GET"])
def get_invoices():

    invoices = Invoice.query.all()

    result = []

    for inv in invoices:
        result.append({
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "po_id": inv.po_id,
            "total_amount": inv.total_amount,
            "status": inv.status
        })

    return jsonify(result), 200

@invoice_bp.route("/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):

    inv = Invoice.query.get(invoice_id)

    if not inv:
        return jsonify({"message": "Invoice not found"}), 404

    return jsonify({
        "invoice_number": inv.invoice_number,
        "po_id": inv.po_id,
        "subtotal": inv.subtotal,
        "tax_percent": inv.tax_percent,
        "tax_amount": inv.tax_amount,
        "total_amount": inv.total_amount,
        "status": inv.status
    }), 200