import os
import configparser
import requests
from boxsdk import DevelopmentClient
from boxsdk import OAuth2
import time
from tqdm import tqdm

# Get the number of minutes between each run from the user
interval_minutes = int(input("Enter the number of minutes between each run: "))

# Calculate the number of seconds in the interval
interval_seconds = interval_minutes * 60

CONFIG_FILE_PATH = ".\\upload.ini"

# Read the authorization and folder ID variables from the file
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
client_id = config["auth"]["client_id"]
client_secret = config["auth"]["client_secret"]
enterprise_id = config["auth"]["enterprise_id"]
folder_id = config["folder"]["folder_id"]
upload_directory = config["folder"]["upload_directory"]

# Loop every N seconds (taken from interval_seconds)
while True:

    AUTH_URL = "https://api.box.com/oauth2/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "box_subject_type":"enterprise",
        "box_subject_id": enterprise_id,
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "enterprise_id": enterprise_id,
    }

    response = requests.post(AUTH_URL, headers=headers, data=data)

    response_data = response.json()
    access_token = response_data["access_token"]
    print(f"access token fetched: {access_token}")


    # Create an OAuth2 object with creds from the variables read above
    oauth2 = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
    )

    # Create a Box client using the OAuth2 object
    box_client = DevelopmentClient(oauth2)

    # Get a reference to the folder where you want to upload the files
    folder = box_client.folder(folder_id).get()

    # Loop through the files in the upload directory
    for filename in os.listdir(upload_directory):
        # Check if the file has the .srt extension
        if filename.endswith(".srt"):
            # Build the full path to the file
            file_path = os.path.join(upload_directory, filename)

            # Check if a file with the same name exists in the folder on Box
            file_exists = False
            for item in folder.get_items():
                if item.name == filename:
                    file_exists = True
                    break

            # Upload the file to the folder if it doesn't already exist
            if not file_exists:
                box_file = folder.upload(file_path, file_name=filename)
                print(f"Uploaded file: {filename}")
            else:
                print(f"File {filename} already exists on Box. Skipping.")
    print("WAITING {0} mins till the next run".format(interval_minutes))
    #fancy progress bar so you could watch it stoned
    for i in tqdm(range(interval_seconds)):
        time.sleep(1)
