import os

"""Authentication configuration helpers."""

# These variables can be populated manually if you prefer hard-coding your
# credentials.  When the respective environment variable is set, it will take
# precedence over the values defined here.
DEFAULT_API_KEY = ""
DEFAULT_M365_USERNAME = ""
DEFAULT_M365_PASSWORD = ""

# Read configuration from environment variables, falling back to the constants
# above so the script continues to function even when values are manually
# inserted here.
API_KEY = os.getenv("CANIX_API_KEY", DEFAULT_API_KEY)
username = os.getenv("M365_USERNAME", DEFAULT_M365_USERNAME)
password = os.getenv("M365_PASSWORD", DEFAULT_M365_PASSWORD)

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json",
}

