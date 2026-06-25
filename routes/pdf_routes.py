from flask import Blueprint, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from models.invoice import Invoice
import os

pdf_bp = Blueprint(
    "pdf",
    __name__
)

@pdf_bp.route(
    "/invoice/<int:invoice_id>/pdf",
    methods=["GET"]
)
def generate_invoice_pdf(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {
            "message": "Invoice not found"
        }, 404
    
    os.makedirs("pdfs", exist_ok=True)
    
    filename = f"invoice_{invoice_id}.pdf"

    doc = SimpleDocTemplate(filename)

    styles =  getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "VendorBridge Invoice",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Invoice Number: {invoice.invoice_number}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Purchase Order ID: {invoice.po_id}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Subtotal: Rs.{invoice.subtotal}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Tax Percentage: {invoice.tax_percent}%",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Tax Amount: Rs.{invoice.tax_amount}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Amount: Rs.{invoice.total_amount}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Status: {invoice.status}",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return send_file(
        filename,
        as_attachment=True
    )
