import json
import uuid
import boto3
import os

# Initialize AWS services
dynamodb = boto3.resource("dynamodb")
sns_client = boto3.client("sns")

# Load environment variables
APPOINTMENT_TABLE = os.environ["APPOINTMENT_TABLE"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

appointment_table = dynamodb.Table(APPOINTMENT_TABLE)

def lambda_handler(event, context):
    try:
        data = json.loads(event["body"])

        # Validate required fields
        required_fields = ["service_center_id", "user_name", "user_contact", "appointment_date"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"statusCode": 400, "body": json.dumps({"error": f"Missing fields: {', '.join(missing_fields)}"})}

        # Generate appointment ID
        appointment_id = str(uuid.uuid4())

        # Save appointment details to DynamoDB
        appointment = {
            "appointment_id": appointment_id,
            "service_center_id": data["service_center_id"],
            "user_name": data["user_name"],
            "user_contact": data["user_contact"],
            "appointment_date": data["appointment_date"]
        }

        appointment_table.put_item(Item=appointment)

        # Send SNS notification
        message = (
            f"Hello Car Company,\n\n"
            f"An appointment has been confirmed!\n"
            f"Customer Name: {data['user_name']}\n"
            f"Contact Email: {data['user_contact']}\n"
            f"Appointment Date: {data['appointment_date']}\n\n"
            f"Thank you!"
        )

        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Appointment Confirmation"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "Appointment booked successfully!",
                "appointment_id": appointment_id
            })
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

