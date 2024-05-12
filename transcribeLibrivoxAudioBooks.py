#conda activate whisperx
#python transcribeLibrivoxAudioBooks.py

import os
import subprocess

def transcribeLibrivoxFiles(input_folder_path, output_folder_path):
	files = os.listdir(input_folder_path)
	files.sort()  # Sort files alphabetically
	for fileNameMp3 in files:
		print("transcribing: " + fileNameMp3)
		command = "whisperx" + " -o " + output_folder_path + " " + input_folder_path + fileNameMp3
		subprocess.run(command, shell=True)

if __name__ == "__main__":
	input_folder_path = 'transcribeIn/'
	output_folder_path = 'transcribeOut/'
	transcribeLibrivoxFiles(input_folder_path, output_folder_path)
