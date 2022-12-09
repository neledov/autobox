# autobox
Simple upload script for *.srt files processed from *.mp3 files by OpenAI whisper

usage:
1.Configure upload.ini script:
example file contents:
[auth]
client_id=XXX #client_id provided by Box API
client_secret=XXX #client_secret provided by Box API
enterprise_id=XXX #enterprise_id provided by Box API

[folder]
folder_id=XXX #folder_id is folder numerical value in last \ section of folder URL when you're in it in Box Web GUI
upload_directory=XXX is upload directory where *.srt files are being kept
