Transfactory:<br />
This script is used for processing video files and creating subtitles for them. It uses the OpenAI Whisper library, Supabase, and dotenv to connect to a storage bucket, download videos, process them, and upload the generated subtitles back to the storage bucket.<br />

Dependencies<br />
os<br />
dotenv<br />
supabase.client<br />
subprocess<br />
tqdm<br />
logging<br />

Usage<br />
Create a .env file in the root of your project and add the following environment variables:
SUPABASE_URL
SUPABASE_KEY
Run the script with python transfactory.py

File Structure<br />
The script prompts the user for the bucket name and sets the directories where the files will be downloaded and processed.<br />
It then connects to Supabase and gets a list of file paths from the selected records in the database.<br />
Then, the script downloads the files from the storage bucket, processes them with OpenAI Whisper, and uploads the generated subtitles to the storage bucket.<br />
Finally, it updates the database with the status of the processed files.<br />

Usage: <br />
<br />
1.Configure upload.ini script: <br /> 
example file contents: <br /> 
[auth] <br /> 
client_id=XXX #client_id provided by Box API <br /> 
client_secret=XXX #client_secret provided by Box API <br /> 
enterprise_id=XXX #enterprise_id provided by Box API <br /> 
 <br />
[folder] <br /> 
folder_id=XXX #folder_id is folder numerical value in last \ section of folder URL when you're in it in Box Web GUI <br /> 
upload_directory=XXX is upload directory where *.srt files are being uploaded by whisper OpenAI batch file <br /> 
<br/>
2.install dependencies:<br/>
pip install boxsdk<br/>
pip install tqdm<br/>
<br />
3.launch the upload_files.py script:<br />
python upload_files.py<br />
enter interval in minutes and press enter<br />
