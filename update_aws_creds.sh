#!/bin/bash

mkdir -p ~/.aws
# Fetch new temporary credentials for 4 hours (14400 seconds)
CREDS_JSON=$(aws sts get-session-token --duration-seconds 14400)

echo "$(CREDS_JSON)"

# Parse the credentials (ensure jq is installed: sudo apt-get install jq)
ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
SECRET_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretAccessKey')
SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')

# Write the credentials to the default AWS credentials file
cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = ${ACCESS_KEY}
aws_secret_access_key = ${SECRET_KEY}
aws_session_token = ${SESSION_TOKEN}
EOF

echo "AWS credentials updated at $(date)"

