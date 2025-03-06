#!/bin/bash
# Use the HOME environment variable explicitly
mkdir -p "$HOME/.aws"

# Fetch new temporary credentials for 4 hours (14400 seconds)
CREDS_JSON=$(aws sts get-session-token --duration-seconds 14400)

# Parse the credentials (ensure jq is installed)
ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
SECRET_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretAccessKey')
SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')

# Write the credentials to the default AWS credentials file using $HOME
cat > "$HOME/.aws/credentials" <<EOF
[default]
aws_access_key_id = ${ACCESS_KEY}
aws_secret_access_key = ${SECRET_KEY}
aws_session_token = ${SESSION_TOKEN}
EOF

echo "$ACCESS_KEY"
echo "$SECRET_KEY"
echo "$SESSION_TOKEN"

echo "AWS credentials updated at $(date)"
