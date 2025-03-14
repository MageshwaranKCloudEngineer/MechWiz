import json
import boto3

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "ServiceCentersTable"

def lambda_handler(event, context):
    try:

        location = event.get("queryStringParameters", {}).get("location", "")


        table = dynamodb.Table(TABLE_NAME)

        response = table.scan()


        centers = [center for center in response.get("Items", []) if center.get("location") == location]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=UTF-8",
                "Access-Control-Allow-Origin": "*",  
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "X-Content-Type-Options": "nosniff", 
                "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate" 
            },
            "body": json.dumps(centers)
        }

    except Exception as e:
        print("Error:", e)
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  
                "X-Content-Type-Options": "nosniff"
            },
            "body": json.dumps({"error": str(e)})
        }
