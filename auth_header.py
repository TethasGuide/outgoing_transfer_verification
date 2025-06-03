import os

# Read configuration from environment variables. If the variables are not set,
# fall back to empty strings so that the application can handle the missing
# credentials gracefully.
API_KEY = os.environ.get("CANIX_API_KEY", "")
headers = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

username = os.environ.get("SHAREPOINT_USERNAME", "")
password = os.environ.get("SHAREPOINT_PASSWORD", "")

