import os
import whisper

# Set the directory containing the MP3 files
mp3_dir = "D:/au/youtube/"

# Set the directory for the output files
output_dir = "D:/au/youtube/"

# Set the language and model parameters
language = "ru"
model = "medium"
device = "cuda"
model_dir = "D:/au/whisper_models/"
verbose = False

# Get a list of all the MP3 files in the directory
mp3_files = os.listdir(mp3_dir)

# Loop through the MP3 files
for mp3_file in mp3_files:
  # Generate some text using whisper
  text = whisper.generate_text(
    file=mp3_file,
    language=language,
    model=model,
    device=device,
    model_dir=model_dir,
    output_dir=output_dir,
    verbose=verbose
  )

  # Print the generated text
  print(text)