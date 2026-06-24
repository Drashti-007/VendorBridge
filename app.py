from flask import Flask, jsonify
from flask_cors import CORS

from database import db
from routes.auth_routes import auth_bp
from routes.vendor_routes import vendor_bp
from routes.rfq_routes import rfq_bp
from routes.quoation_routes import quotation_bp
from routes.approval_routes import approval_bp
from routes.purchase_order_routes import purchase_order_bp
from routes.invoice_routes import invoice_bp
from routes.activity_routes import activity_bp
from routes.analytics_routes import analytics_bp

app = Flask(__name__)

app.secret_key = "vendorbridge_secret_key"

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendorbridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(vendor_bp)
app.register_blueprint(rfq_bp)
app.register_blueprint(quotation_bp)
app.register_blueprint(approval_bp)
app.register_blueprint(purchase_order_bp)
app.register_blueprint(invoice_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(analytics_bp)

from models.user import User
from models.vendor import Vendor
from models.rfq import RFQ
from models.quotation import Quotation
from models.approval import Approval
from models.purchase_order import PurchaseOrder
from models.invoice import Invoice
from models.rfq_vendor import rfq_vendors
from models.activity_log import ActivityLog

@app.route('/')
def home():
    return jsonify({
        "message": "VendorBridge Backend Running"
    })

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)