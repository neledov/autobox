import os
import supabase.client as supabase_client
import subprocess
from tqdm import tqdm
import logging

def main():

    logging.basicConfig(level=logging.INFO)

    # Prompt the user for the bucket name
    bucket_name = "prabyss"

    # Set the directories where the files will be downloaded and processed
    download_directory = "D:/Input/"
    model_dir = "D:/au/whisper_models/"
    output_directory = os.path.join("D:/au/", bucket_name)

    # Set the OpenAI Whisper command-line arguments
    openai_args = [
        "whisper",
        "--language", "ru",
        "--model", "medium",
        "--device", "cuda",
        "--model_dir", model_dir,
        "--output_dir", output_directory,
        "--verbose", "False"
    ]

    # Connect to Supabase
    client = supabase_client.create_client(
        supabase_url="https://svfizyfozagyqkkjzqdc.supabase.co",
        supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN2Zml6eWZvemFneXFra2p6cWRjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY1NjM0NzMwNCwiZXhwIjoxOTcxOTIzMzA0fQ.aBQ6SIdy7nprpqox7a6aSjHAzwRR8MMxdV-v9Dxf0Qg"
    )
    
    # Get db object with selected records
    db = client.postgrest.schema("service").from_(bucket_name).select("path").eq("status", "uploaded_test").execute()

    # Get path list from every row in db.data tuple
    path_list = [row["path"] for row in db.data]
    # Defile storage
    storage = client.storage()
    bucket = storage.get_bucket(bucket_name)

    with tqdm(total=len(path_list)) as pbar:
        for obj in path_list:
            try:
                disk_full_file_path = os.path.join(download_directory, obj)
                disk_full_file_path_output = os.path.join(output_directory, os.path.basename(disk_full_file_path) + ".srt")
                file_clean_name = os.path.basename(disk_full_file_path_output)
                bucket_path = os.path.dirname(obj)
                dir_of_file = os.path.dirname(disk_full_file_path)

                # Check if directory with bucket name exists if no - create it
                if not os.path.isdir(dir_of_file):
                    os.makedirs(dir_of_file, exist_ok=True)
                    logging.info("creating directories in the path")
                else:
                    logging.info("folder already exists, skipping")
                file_bytes = bucket.download(obj)
                with open(disk_full_file_path, "wb") as f:
                    f.write(file_bytes)
                    subprocess.run(openai_args + [disk_full_file_path])
            except Exception as e:
                # Catch any exception that occurs during the processing and log it
                logging.error(f"An error occurred while processing {disk_full_file_path}: {e}")
                continue

            # Upload the output .srt file to the storage bucket
            try:
                with open(disk_full_file_path_output, 'r') as f:
                    file_content = f.read()
                bucket.upload(os.path.join(bucket_path, file_clean_name), file_content)
            except Exception as e:
                logging.error(f"An error occurred while uploading {disk_full_file_path_output}: {e}")
                continue
            pbar.update(1)   
    
if __name__ == "__main__":
    main()

