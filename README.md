Transfactory:<br />
This script is used for processing video files and creating subtitles for them. It uses the OpenAI Whisper library, Supabase, and dotenv to connect to a storage bucket, download videos, process them, and upload the generated subtitles back to the storage bucket.<br />

Dependencies<br />
os<br />
dotenv<br />
supabase.client<br />
subprocess<br />
logging<br />

Usage<br />
Create a .env file in the root of your project and add the following environment variables:
SUPABASE_URL
SUPABASE_KEY
BUCKET_NAME
DIR_DOWNLOAD
DIR_AI_MODEL_LOC
DIR_SRT_OUT_BASE

Run the script with python transfactory.py

File Structure<br />
The script checks .env file for the bucket name and sets the directories where the files will be downloaded and processed.<br />
It then connects to Supabase and gets a list of file paths from the selected records in the database.<br />
Then, the script downloads the files from the storage bucket, processes them with OpenAI Whisper, and uploads the generated subtitles to the storage bucket.<br />
Finally, it updates the database with the status of the processed files.<br />
