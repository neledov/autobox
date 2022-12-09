# autobox
Simple upload script for *.srt files processed from *.mp3 files by OpenAI whisper <br /> 

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
