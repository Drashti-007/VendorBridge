from flask import Blueprint, send_file
from reportlab.platypus import (
    SimpleDocTemplate, 
    Paragraph, 
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from models.invoice import Invoice
import os
from datetime import datetime

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

    elements.append(
        Paragraph(
            "PROCUREMENT INVOICE",
            styles["Heading2"]
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

    elements.append(
        Paragraph(
            f"Date: {datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    data = [
        ["Description", "Amount"],
        ["Subtotal", f"Rs.{invoice.subtotal}"],
        ["Tax", f"Rs.{invoice.tax_amount}"],
        ["TOTAL", f"Rs.{invoice.total_amount}"]
    ]

    table = Table(data, colWidths=[250, 150])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12)   
        ])
    )

    elements.append(table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Thank you for using VendorBridge.",
            styles["Italic"]
        )
    )

    elements.append(
        Paragraph(
            "This is a system-generated invoice.",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return send_file(
        filename,
        as_attachment=True
    )
