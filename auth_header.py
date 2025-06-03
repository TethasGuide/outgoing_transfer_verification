import os

"""Authentication configuration helpers."""

# These variables can be populated manually if you prefer hard-coding your
# credentials.  When the respective environment variable is set, it will take
# precedence over the values defined here.
DEFAULT_API_KEY = ""
DEFAULT_M365_USERNAME = ""
DEFAULT_M365_PASSWORD = ""
DEFAULT_SP_MAIN_SITE_URL = "https://totalhealthcollective.sharepoint.com"
DEFAULT_SP_LIBRARY_PATH = "/sites/documentcontrol/Shared Documents/Controlled Tracking Excels/Shipping/Verification CSVs"

# Read configuration from environment variables, falling back to the constants
# above so the script continues to function even when values are manually
# inserted here.
API_KEY = os.getenv("CANIX_API_KEY", DEFAULT_API_KEY)
username = os.getenv("M365_USERNAME", DEFAULT_M365_USERNAME)
password = os.getenv("M365_PASSWORD", DEFAULT_M365_PASSWORD)
SP_MAIN_SITE_URL = os.getenv("SP_MAIN_SITE_URL", DEFAULT_SP_MAIN_SITE_URL)
SP_LIBRARY_PATH = os.getenv("SP_LIBRARY_PATH", DEFAULT_SP_LIBRARY_PATH)

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json",
}

