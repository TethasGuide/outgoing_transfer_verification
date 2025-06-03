# outgoing_transfer_verification
For verifying outgoing transfers utilizing the Canix API. 

The Outgoing Transfer Verification function is a Python script designed to interact with Canix and Microsoft Office365 for the purpose of fetching, processing, and reporting cannabis transfer data. This utility automates the retrieval of transfer data from Canix, augments it with additional details (e.g., weight and unit for each tag), and then generates a verification report which is uploaded to a specified SharePoint document library.

Installation
To get started with the Transfer Manifest Scanner, clone this repository to your local machine using:


git clone https://github.com/yourusername/transfer-manifest-scanner.git
cd transfer-manifest-scanner
Before running the script, ensure Python 3.x is installed on your system. You can download Python here.(https://www.python.org/downloads/)

Configuration
API Keys and Credentials
You need to obtain an API Key from Canix and credentials for Microsoft Office365 access.
Once you have your Canix API Key, open auth_header.py and fill in the API_KEY variable:

API_KEY = 'your_canix_api_key_here'

Similarly, for Microsoft Office365 login details, specify your username and password in the same file:

username = "your_microsoft_email_login_here"
password = "your_login_password_here"


Note: Do not share your API keys or credentials within your code when publishing or sharing your project.

Dependencies
Install the required Python packages using the requirements file:

pip install -r requirements.txt


Usage
To run the Transfer Manifest Scanner, execute the following command in your terminal:

python transfer_manifest_scanner.py

Follow the GUI prompts to enter the verifier name, manifest number, and to scan tags as part of the transfer verification process.

Contributing
Contributions to the Transfer Manifest Scanner are welcome! Please feel free to submit pull requests, report bugs, or suggest features via the GitHub issues page.

License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
