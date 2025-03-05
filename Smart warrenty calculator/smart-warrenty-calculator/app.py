from flask import Flask, request, jsonify, render_template
import uuid
from datetime import datetime
import config

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/check-warranty", methods=["POST"])
def check_warranty():
    try:
        data = request.json
        print("Received request:", data)

        response = warranty_table.get_item(Key={"product_id": data["product_id"]})
        print("DynamoDB Response:", response)

        item = response.get("Item")

        if not item:
            return jsonify({"status": "Expired"}), 404
        
        return jsonify({"status": "Active", "warranty_period": item["warranty_period"]})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/check-warranty", methods=["GET"])
def check_warranty_page():
    return render_template("warranty_check.html")



@app.route("/service-centers", methods=["GET"])
def get_service_centers():
    location = request.args.get("location")
    response = service_centers_table.scan()
    centers = [center for center in response.get("Items", []) if center.get("location") == location]
    return jsonify(centers)
    
@app.route('/service-centers-page', methods=['GET'])
def service_centers_page():
    return render_template("service_centers.html")

@app.route("/service-center/<id>", methods=["GET"])
def get_service_center_by_id(id):
    response = service_centers_table.get_item(Key={"id": id})
    item = response.get("Item")
    if not item:
        return jsonify({"error": "Service center not found"}), 404
    return jsonify(item)

@app.route("/request-appointment", methods=["POST"])
def request_appointment():
    try:
        data = request.json
        appointment_id = str(uuid.uuid4())
        appointment = {
            "appointment_id": appointment_id,
            "service_center_id": data["service_center_id"],
            "user_name": data["user_name"],
            "user_contact": data["user_contact"],
            "appointment_date": data["appointment_date"]
        }
        appointment_table = dynamodb.Table("AppointmentTable")
        appointment_table.put_item(Item=appointment)

        user_email = data["user_contact"] 
        subject = "Appointment Confirmation"
        message = f"Hello Car Company,\n\nAn appointment has been confirmed booked!\nCustomername: {data['user_name']}\nContact email : {data['user_contact']}\nAppointment Date: {data['appointment_date']}\n\nThank you!"

        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:053158170613:Smart_warrenty_calculator_email', 
            Message=message,
            Subject=subject,
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': user_email
                }
            }
        )

        return jsonify({
            "status": "Appointment booked successfully!",
            "appointment_id": appointment_id,
            "sns_response": response
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/book-appointment')
def book_appointment():
    return render_template("appointment_booking.html")


@app.route("/add-service-center", methods=["POST"])
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

@app.route("/add-warranty", methods=["POST"])
def add_warranty():
    try:
        data = request.json
        warranty_table.put_item(Item={
            "product_id": data["product_id"],
            "purchase_date": data["purchase_date"],
            "warranty_period": data["warranty_period"]
        })
        return jsonify({"status": "Warranty details added successfully!"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/upload-warranty-doc", methods=["POST"])
def upload_warranty_doc():
    file = request.files["file"]
    file_name = f"{uuid.uuid4()}_{file.filename}"
    s3_client.upload_fileobj(file, S3_BUCKET, file_name)
    return jsonify({"status": "Uploaded", "file_url": f"https://{S3_BUCKET}.s3.amazonaws.com/{file_name}"})

if __name__ == "__main__":

    app.run(debug=True)
