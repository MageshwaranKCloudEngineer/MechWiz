import boto3
import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=AWS_REGION
)
service_centers_table = dynamodb.Table("ServiceCentersTable")
warranty_table = dynamodb.Table("WarrantyTable")
appointment_table = dynamodb.Table("AppointmentTable")


S3_BUCKET = "your-s3-bucket-name"
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=AWS_REGION
)

# Set up SNS client
sns_client = boto3.client(
    "sns",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=AWS_REGION
)


if __name__ == "__main__":

    app.run(debug=True)