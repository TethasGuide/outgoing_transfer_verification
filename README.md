# outgoing_transfer_verification
For verifying outgoing transfers utilizing the Canix API. 

The Outgoing Transfer Verification function is a Python script designed to interact with Canix and Microsoft Office365 for the purpose of fetching, processing, and reporting cannabis transfer data. This utility automates the retrieval of transfer data from Canix, augments it with additional details (e.g., weight and unit for each tag), and then generates a verification report which is uploaded to a specified SharePoint document library.

Installation
To get started with the Outgoing Transfer Verification Tool, clone this repository to your local machine using:


git clone https://github.com/yourusername/outgoing_transfer_verification.git
cd outgoing_transfer_verification
Before running the script, ensure Python 3.x is installed on your system. You can download Python here.(https://www.python.org/downloads/)

Configuration
API Keys and Credentials
You need to obtain an API Key from Canix and credentials for Microsoft Office365 access.

Once you have your Canix API Key and Microsoft credentials you can store them in
`auth_header.py` or, preferably, load them from environment variables. A
`.env.example` file is provided that lists the required variables. Copy this file
to `.env` and fill in your values. Example environment variable names:

```
export CANIX_API_KEY=your_canix_api_key_here
export M365_USERNAME=your_sharepoint_email_login
export M365_PASSWORD=your_login_password
export SP_MAIN_SITE_URL=https://yourcompany.sharepoint.com
export SP_LIBRARY_PATH="/sites/documentcontrol/Shared Documents/..."
```

After updating `.env` with your credentials, the script will load these values
automatically when executed. If the variables are not set, any values entered in
`auth_header.py` will be used instead.


Note: Do not share your API keys or credentials within your code when publishing or sharing your project.

Thread Pool Workers
-------------------
Package weight information is fetched concurrently using threads. The default
number of worker threads is **10**, but this can be tuned by setting the
`WEIGHT_FETCH_WORKERS` environment variable before running the script. Adjust
this value based on your available network capacity and any API rate limits you
need to respect.

Dependencies
All Python dependencies are listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```


Usage
To run the Outgoing Transfer Verification Tool, execute the following command in your terminal:

python verification_function.py

Follow the GUI prompts to enter the verifier name, manifest number, and to scan tags as part of the transfer verification process.

### Settings Window

From the main window you can open **Settings** to update credentials and SharePoint options without restarting.  The following fields can be changed:

* `CANIX_API_KEY`
* `M365_USERNAME`
* `M365_PASSWORD`
* `SP_MAIN_SITE_URL`
* `SP_LIBRARY_PATH`
* `WEIGHT_FETCH_WORKERS`

Any changes are stored in memory and apply to future API calls.

Docker Usage
------------
If you prefer running the verification tool in a container, use the provided
`Dockerfile` to build an image and run it:

```bash
docker build -t outgoing-transfer-verification .
docker run --rm outgoing-transfer-verification
```

Contributing
Contributions to the Outgoing Transfer Verification Tool are welcome! Please feel free to submit pull requests, report bugs, or suggest features via the GitHub issues page.

License
This project is licensed under the GNU Affero General Public License v3.0 - see the LICENSE file for details.
