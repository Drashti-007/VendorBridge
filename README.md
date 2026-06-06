# VendorBridge – Procurement Management System

VendorBridge is a full-stack procurement workflow management system built using Flask (Backend) and designed to streamline the end-to-end procurement lifecycle including RFQ creation, vendor management, quotations, approvals, purchase orders, invoices, and activity tracking.

# Features

## Authentication & Authorization
- User registration and login
- Role-based access control:
  - Admin
  - Procurement Officer
  - Manager
  - Vendor
- Session-based authentication

## Vendor Management
- Add and manage vendors
- Store company details (GST, contact info, category)
- Link vendors to RFQs

## RFQ (Request for Quotation)
- Create RFQs with item requirements
- Assign multiple vendors to RFQs
- Track RFQ status and lifecycle

## Quotation System
- Vendors submit quotations against RFQs
- Store price, delivery time, and notes
- Compare multiple quotations for decision making

## Approval Workflow
- Manager approval/rejection system
- Approval tracking with remarks
- Ensures controlled procurement decisions

## Purchase Order System
- Generate Purchase Orders from approved quotations
- Track PO status (Generated / Accepted / Delivered)
- Unique PO numbering system

## Invoice System
- Generate invoices from Purchase Orders
- Automatic tax calculation
- Stores subtotal, tax, and total amount

## Activity Logging System
- Tracks all system events:
- RFQ creation
- Vendor assignment
- Quotation submission
- Approval actions
- PO generation
- Invoice creation
- Provides full audit trail for transparency

# Tech Stack

## Backend
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flask Sessions
## Database
- SQLite (development)
- Easily migratable to PostgreSQL/MySQL
## Tools
Postman (API testing)

## API Endpoints

Auth
- POST /register
- POST /login

Vendors
- POST /vendors
- GET /vendors
- RFQs
- POST /rfqs
- GET /rfqs
- POST /rfqs/<id>/vendors

Quotations
- POST /quotations
- GET /rfqs/<id>/quotations
- GET /rfqs/<id>/compare

Approvals
- POST /approvals
- GET /approvals

Purchase Orders
- POST /purchase-orders
- GET /purchase-orders
- PUT /purchase-orders/<id>

Invoices
- POST /invoices
- GET /invoices
- GET /invoices/<id>

Activity Logs
- GET /activities

#  Key Highlights
- Full ERP-style procurement workflow
- Role-based access system
- End-to-end traceability using activity logs
- Modular Flask architecture using Blueprints
- Easy to extend to PostgreSQL + frontend integration
# Setup Instructions
## Clone repo
git clone <repo-url>

## Install dependencies
pip install -r requirements.txt

## Run server
python app.py

## Testing

Use Postman:

- Start with /register
- Login via /login
- Follow workflow:
- RFQ → Quotation → Approval → PO → Invoice

## Future Improvements
- JWT Authentication instead of sessions
- PostgreSQL integration
- Frontend dashboard (React/Angular)
- PDF invoice generation
- Email notifications
- Analytics dashboard

# Final Note

VendorBridge simulates a real-world procurement system used in enterprises to manage vendor workflows, approvals, and financial tracking in a structured and auditable way.
