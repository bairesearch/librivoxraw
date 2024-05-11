#conda activate whisperx
#python transcribeLibrivoxAudioBooks.py

import os
import subprocess

def transcribeLibrivoxFiles():
	folder_path = '../transcribeIn'
	files = os.listdir(folder_path)
	files.sort()  # Sort files alphabetically
	for fileMp3 in files:
		print("transcribing: " + fileMp3)
		#fileMp3
		command = "whisperx " + folder_path + "/" + fileMp3
		subprocess.run(command, shell=True)

if __name__ == "__main__":
	transcribeLibrivoxFiles()
