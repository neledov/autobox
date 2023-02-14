import logging
import os
import subprocess
import time
import datetime

import dotenv
import supabase.client as supabase_client

def get_formatted_date_time():
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time as a string
    date_time_str = now.strftime("%b %d %Y %H:%M:%S")

    # Return the date and time string
    return date_time_str

# Call the function and print the result
print(get_formatted_date_time())

def main():
    dotenv.load_dotenv()

    logging.basicConfig(level=logging.INFO)

    logging.info("Oh here we go again...")

    # Set bucket name
    bucket_name = os.getenv('BUCKET_NAME')

    # Set the directories where the files will be downloaded and processed
    dir_download = os.getenv('DIR_DOWNLOAD')
    dir_ai_model_loc = os.getenv('DIR_AI_MODEL_LOC')
    dir_srt_out_base = os.getenv('DIR_SRT_OUT_BASE')
    dir_srt_out = os.path.join(dir_srt_out_base, bucket_name)

    logging.info("Assembiling client creds...")
    # Connect to Supabase
    client = supabase_client.create_client(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_KEY')
    )
    logging.info("Supabase client set...")
    # Get query_select object with selected records
    query_select = client.postgrest.schema("service").from_(bucket_name).select("*").eq("status", "uploaded").limit(1).execute()
    logging.info("Queried table for availiable work")
    job_queue_size = len(query_select.data)
    if job_queue_size>0:
    # Define storage
        logging.info("I have stuff to do!")
        storage = client.storage()
        bucket = storage.get_bucket(bucket_name)

        for obj in query_select.data:
            try:
                # Set the OpenAI Whisper command-line arguments
                logging.info("Preparing OpenAI Whisper arguments for {0}".format(obj["title"]))
                openai_args = [
                    "whisper",
                    "--language", obj["lang"],
                    "--model", obj["model"],
                    "--device", "cuda",
                    "--model_dir", dir_ai_model_loc,
                    "--output_dir", dir_srt_out,
                    "--verbose", "False"
                ]
                file_disk_full_path = '/'.join([dir_download, obj["path"]])
                file_disk_full_path_srt = '/'.join([dir_srt_out, os.path.basename(file_disk_full_path) + ".srt"])
                file_name_srt = os.path.basename(file_disk_full_path_srt)
                dir_bucket_path = os.path.dirname(obj["path"])
                dir_path = os.path.dirname(file_disk_full_path)
                # Check if directory with bucket name exists if no - create it
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    logging.info("No directories exist: creating directories in the path...")
                else:
                    logging.info("Directory already exists, skipping...")
                logging.info("Downloading file from the Supabase path: {0}".format(obj["path"]))
                file_bytes = bucket.download(obj["path"])
                with open(file_disk_full_path, "wb") as f:
                    f.write(file_bytes)
                logging.info("Invoking OpenAI Whisper on downloaded file: {0}".format(file_disk_full_path))
                logging.info("Updating table record for {0} as IN PROGRESS to avoid duplicate tasking".format(obj["title"]))
                client.postgrest.schema('service').table('prabyss').update({"status": "in progress"}).eq("id", obj["id"]).execute()
                client.postgrest.schema('service').table('prabyss').update({"started_at": get_formatted_date_time()}).eq("id", obj["id"]).execute()
                subprocess.run(openai_args + [file_disk_full_path])
            except Exception as e:
                # Catch any exception that occurs during the processing and log it
                logging.error(f"Oh noes! An error occurred while downloading file: {e}")
                logging.warning("Setting back file status from IN PROGRESS to UPLOADED...")
                client.postgrest.schema('service').table('prabyss').update({"status": "uploaded"}).eq("id", obj["id"]).execute()
                continue

            # Upload the output .srt file to the storage bucket
            try:
                logging.info("Attempting to upload *.srt file to the bucket {0}...".format(bucket_name))
                bucket.upload('/'.join([dir_bucket_path, file_name_srt]), file_disk_full_path_srt)
                logging.info("Updating table record for {0} as PROCESSED".format(obj["title"]))
                client.postgrest.schema('service').table('prabyss').update({"status": "processed"}).eq("id", obj["id"]).execute()
                client.postgrest.schema('service').table('prabyss').update({"completed_at": get_formatted_date_time()}).eq("id", obj["id"]).execute()
            except Exception as e:
                logging.error(
                    f"Oh noes! An error occurred while uploading file: {e}")
                logging.warning("Setting back file status from IN PROGRESS to UPLOADED...")
                client.postgrest.schema('service').table('prabyss').update({"status": "uploaded"}).eq("id", obj["id"]).execute()
                continue
        
    else:
        logging.info("Nothing to do, idling...")
        time.sleep(30)


while True:
    if __name__ == "__main__":
        main()
