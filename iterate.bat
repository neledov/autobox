 for /R %%f in (*.mp3) do (
 whisper "%%f" --language ru --model medium --device cuda --model_dir "D:/au/whisper_models/" --output_dir "D:/au/youtube/" --verbose False
 )