import json
import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')

# Replace with your actual DynamoDB table name
TABLE_NAME = "ServiceCentersTable"

def lambda_handler(event, context):
    try:
        # Extract location from query parameters
        location = event.get("queryStringParameters", {}).get("location", "")

        # Get DynamoDB table
        table = dynamodb.Table(TABLE_NAME)

        # Scan all service centers (optimize later with indexing if needed)
        response = table.scan()

        # Filter service centers by location
        centers = [center for center in response.get("Items", []) if center.get("location") == location]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=UTF-8",
                "Access-Control-Allow-Origin": "*",  # Allow all origins
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "X-Content-Type-Options": "nosniff",  # Security header
                "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate"  # Performance optimization
            },
            "body": json.dumps(centers)
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Ensure error response also has CORS headers
                "X-Content-Type-Options": "nosniff"
            },
            "body": json.dumps({"error": str(e)})
        }
