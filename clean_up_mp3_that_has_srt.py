import os

files = os.listdir()

for file in files:
  if file.endswith('.srt'):
    mp3_file = file[:-4] + '.mp3'
    if os.path.exists(mp3_file):
      os.remove(file)
      os.remove(mp3_file)
      print("removing {0}".format(file))