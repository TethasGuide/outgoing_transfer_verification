import logging
import os
import csv

import concurrent.futures
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

import requests
from auth_header import headers, username, password
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

# Number of workers used when fetching package weights concurrently. Can be
# overridden with the WEIGHT_FETCH_WORKERS environment variable.
WEIGHT_FETCH_WORKERS = int(os.getenv("WEIGHT_FETCH_WORKERS", "10"))

def get_transfers(api_endpoint, headers, logger):
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code != 200:
            print("Error status code:", response.status_code)
            logger.error(f"Error: {response.status_code} {response.text}")
            print("Error response:", response.text)
            
            return None
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        return None
    
def fetch_weight_for_tag(tag, logger):
    api_endpoint = f"https://api.canix.com/api/v1/packages?where=tag=%27{tag}%27"
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:
                logger.warning(f"No data returned for tag {tag}")
                return 0, None
            weight = data[0].get('weight', 0)
            weight_unit = data[0].get('weight_unit', "")
            return weight, weight_unit
        else:
            logger.error(f"Error fetching weight for tag {tag}: {response.status_code} {response.text}")
            return 0, None
    except requests.RequestException as e:
        logger.error(f"Error fetching weight for tag {tag}: {e}")
        return 0, None







class TransferApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tag_item_dict = {}
        self.scanned_items = {}

        self.title("Transfer Manifest Scanner")
        self.geometry("800x500")
        self.init_logger()

        self.create_widgets()
        
    def init_logger(self):
        
        self.logger = logging.getLogger("ship_verification")
        self.logger.setLevel(logging.DEBUG)

        
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        
        if not os.path.exists("ship_verification.log"):
            open("ship_verification.log", "w").close()  
        file_handler = logging.FileHandler("ship_verification.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def create_widgets(self):
        
        # Name Entry 
        self.name_label = tk.Label(self, text="Verifier Name")
        self.name_label.pack(pady=(10, 0))
        self.name_entry = tk.Entry(self, width=20)
        self.name_entry.pack(pady=5)
        
        # Manifest Number Entry
        self.manifest_label = tk.Label(self, text="Enter Manifest Number:")
        self.manifest_label.pack(pady=(10, 0))
        self.manifest_entry = tk.Entry(self, width=20)
        self.manifest_entry.pack(pady=5)

        # Fetch Data Button
        self.fetch_button = tk.Button(self, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack(pady=5)

        # Tag Entry
        self.tag_entry = tk.Entry(self, width=50)
        self.tag_entry.pack(pady=10)
        self.tag_entry.bind("<Return>", self.scan_tag) 
        self.tag_entry.config(state='disabled')        
        
        # Scan Button
        self.scan_button = tk.Button(self, text="Scan", command=self.scan_tag)
        self.scan_button.pack(pady=10)
        self.scan_button.config(state='disabled')  

        # Scanned Items List
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_list = tk.Listbox(self, width=125, yscrollcommand=self.scrollbar.set)
        self.items_list.pack(pady=10)
        self.scrollbar.config(command=self.items_list.yview)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)
        self.submit_button.config(state='disabled')

    def process_transfers(self, transfer):
        self.logger.info("Starting to process transfers.")
        tag_item_dict = {}
        tags = []

        # First, collect basic details about each tag
        for destination in transfer.get("destinations", []):
            for content in destination.get("contents", []):
                package = content.get("package", {})
                tag = package.get("tag")
                if tag:
                    item = package.get("item", {})
                    item_name = item.get("name")
                    sub_type = item.get("sub_type", {})
                    sub_type_name = sub_type.get("name") if sub_type else None
                    tag_item_dict[tag] = {
                        'item_name': item_name,
                        'sub_type_name': sub_type_name
                    }
                    tags.append(tag)
                    self.logger.debug(f"Tag found: {tag}")

        if not tags:
            self.logger.warning("No tags found in transfer data.")

        # Concurrently fetch weights and weight units for each tag
        with concurrent.futures.ThreadPoolExecutor(max_workers=WEIGHT_FETCH_WORKERS) as executor:
            tag_details = {tag: executor.submit(fetch_weight_for_tag, tag, self.logger) for tag in tags}

        for tag, future in tag_details.items():
            try:
                weight, weight_unit = future.result()
                if tag in tag_item_dict:
                    tag_item_dict[tag].update({'weight': weight, 'weight_unit': weight_unit})
                    self.logger.info(f"Updated tag {tag} with weight and unit.")
                else:
                    self.logger.warning(f"Tag {tag} not found in initial data collection.")
            except Exception as e:
                self.logger.error(f"Error processing tag {tag}: {e}")

        self.logger.info("Finished processing transfers.")
        return tag_item_dict
    def fetch_data(self):
        manifest_number = self.manifest_entry.get()
        response = None
        if manifest_number:
            api_endpoint = f"https://api.canix.com/api/v1/transfers?where=manifest_number=%27{manifest_number}%27"
            response = get_transfers(api_endpoint, headers, self.logger)
        else:
            messagebox.showwarning("Missing Manifest Number", "Please enter a manifest number before fetching data.")
            self.logger.warning("Manifest number was not provided when attempting to fetch data.")

        if response is not None and isinstance(response, list) and len(response) > 0:
            transfer = response[0]
            self.tag_item_dict = self.process_transfers(transfer)
            self.tag_entry.config(state='normal')
            self.scan_button.config(state='normal')
            self.submit_button.config(state='normal')
            print ("Fetched tag-item dictionary:", self.tag_item_dict)
            self.logger.info(f"Fetched tag-item dictionary:{self.tag_item_dict}")
                        
        else:
            messagebox.showerror("Error", "Failed to fetch data for the given manifest number.")
    def scan_tag(self, event=None): 
        tag = self.tag_entry.get()
        print("Scanned tag:", tag)
        self.logger.info(f"Scanned tag:{tag}")
        if tag in self.scanned_items:
            messagebox.showinfo("Duplicate Tag", "This tag has already been verified")
        elif tag in self.tag_item_dict:
            data = self.tag_item_dict[tag]
            display_info = f"{tag}: {data['item_name']}, {data['weight']} {data['weight_unit']}"
            self.items_list.insert(tk.END, display_info)
            self.scanned_items[tag] = data
        else:
            self.handle_unrecognized_tag(tag)

        self.tag_entry.delete(0, tk.END)
        self.tag_entry.focus_set()


    def handle_unrecognized_tag(self, tag):
        response = messagebox.showinfo("Unrecognized Tag", f"The tag '{tag}' is not present on this manifest.")
        if response:            
            self.tag_entry.delete(0, tk.END)

    def submit(self):
        if self.check_missed_items():
            manifest_number = self.manifest_entry.get()
            local_file_path, file_name = self.generate_csv(manifest_number)
            self.upload_to_sharepoint(local_file_path, file_name)
            messagebox.showinfo("Success", f"{manifest_number} verification.csv generated successfully!")
            self.destroy()

    def check_missed_items(self):
        missed_items = [tag for tag in self.tag_item_dict if tag not in self.scanned_items]
        if missed_items:
            missed_items_str = "\n".join([f"{tag}: {self.tag_item_dict[tag]}" for tag in missed_items])
            messagebox.showwarning("Missed Items", f"The following items were not scanned:\n{missed_items_str}")
            return False
        return True

    def upload_to_sharepoint(self, local_filepath, file_name):
        # Main SharePoint Site URL
        main_site_url = "https://totalhealthcollective.sharepoint.com"

        # Subsite URL for 'documentcontrol'
        document_control_site_url = f"{main_site_url}/sites/documentcontrol"

        # Create a client context with the subsite URL
        ctx = ClientContext(document_control_site_url).with_credentials(UserCredential(username, password))

        # Server-relative URL for the specific folder in the library
        server_relative_url = "/sites/documentcontrol/Shared Documents/Controlled Tracking Excels/Shipping/Verification CSVs"

        sp_library = ctx.web.get_folder_by_server_relative_url(server_relative_url)

        with open(local_filepath, 'rb') as file_input:
            file_content = file_input.read()

        try:
            # Upload the file
            sp_library.upload_file(file_name, file_content)
            ctx.execute_query()
            self.logger.info(f"Uploaded CSV as {file_name}")
        except Exception as e:
            self.logger.error(f"Error uploading file to SharePoint: {e}")


    
    def generate_csv(self, manifest_number):
        user = self.name_entry.get()
        filename = f"{user} {manifest_number} verification.csv"        
        # Get the current working directory
        current_directory = os.getcwd()
    
        # Construct the full file path
        local_filepath = os.path.join(current_directory, filename)
        self.logger.info(f"Saving CSV locally as {local_filepath}")

        with open(local_filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Tag", "Name", "Weight", "Weight Unit", "Sub Type", "Timestamp"])
            for tag, data in self.scanned_items.items():
                timestamp = datetime.now().isoformat()
                writer.writerow([tag, data['item_name'], data['weight'], data['weight_unit'], data['sub_type_name'], timestamp])

        # Return the full path of the saved file
        return local_filepath, filename
    



if __name__ == "__main__":
    app = TransferApp()
    app.mainloop()
