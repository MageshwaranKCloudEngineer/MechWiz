from flask import Flask, request, jsonify, render_template
import uuid
from datetime import datetime
import config
from config import service_centers_table, warranty_table, appointment_table, sns_client
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram
from time import time
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

metrics = PrometheusMetrics(app, path="/metrics")

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"]
)

@app.before_request
def start_timer():
    request.start_time = time()

@app.after_request
def log_request(response):
    if request.endpoint:
        http_requests_total.labels(method=request.method, endpoint=request.path).inc()
        request_latency = time() - request.start_time
        http_request_duration.labels(method=request.method, endpoint=request.path).observe(request_latency)
    return response

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/add-service-center-page", methods=["GET"])
def add_service_center_page():
    return render_template("add_service_center.html")
    
@app.route("/check-warranty", methods=["GET"])
def check_warranty_page():
    return render_template("warranty_check.html")
 
@app.route('/service-centers-page', methods=['GET'])    
def service_centers_page():
    return render_template("service_centers.html")
    
@app.route('/book-appointment')
def book_appointment():
    return render_template("appointment_booking.html")

@app.route("/service-center/<id>", methods=["GET"])
def get_service_center_by_id(id):
    response = service_centers_table.get_item(Key={"id": id})
    item = response.get("Item")
    if not item:
        return jsonify({"error": "Service center not found"}), 404
    return jsonify(item)

@app.route("/app/add-service-center", methods=["POST"])
def add_service_center():
    try:
        data = request.json

        service_centers_table.put_item(Item={
            "id": str(uuid.uuid4()),
            "name": data["name"],
            "address": data["address"],
            "location": data["location"],
            "type": data["type"]
        })
        return jsonify({"status": "Service center added successfully!"})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
