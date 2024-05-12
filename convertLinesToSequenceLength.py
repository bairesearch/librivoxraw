#python convertLinesToSequenceLength.py

import os
import re

def setSequenceLength(input_folder_path, output_folder_path, fileExtension, sequenceLength, output_file_prefix):
	# List all files in the folder
	files = os.listdir(input_folder_path)
	files.sort()  # Sort files alphabetically
	
	# Filter only .txtx files
	txt_files = [file for file in files if file.endswith(fileExtension)]
	
	output_file_suffix = fileExtension

	# Process each text file
	for txt_file in txt_files:
		input_file_path = os.path.join(input_folder_path, txt_file)
		
		# Open the input file
		fileTokensNew = []
		with open(input_file_path, 'r') as input_file:
			lineTokensNew = []
			for line in input_file:
				lineTokens = getTokens(line, fileExtension)
				#print("lineTokens = ", lineTokens)
				proposedSequenceLength = len(lineTokensNew) + len(lineTokens)
				if(proposedSequenceLength < sequenceLength):
					lineTokensNew = lineTokensNew + lineTokens
					#print("lineTokensNew = ", lineTokensNew)
				else:
					lineTokensNew.append('\n')
					lineTokensNewString = "".join(lineTokensNew)
					fileTokensNew.append(lineTokensNewString)
					lineTokensNew = lineTokens
			
		output_file_name = os.path.splitext(os.path.basename(txt_file))[0]
		output_file_path = f"{output_folder_path}{output_file_name}{output_file_suffix}"
		with open(output_file_path, 'w') as output_file:
			output_file.writelines(fileTokensNew)
					
def getTokens(line, fileExtension):
	tokens = re.findall(r'\S+|\s+|\n', line)
	if(tokens and tokens[-1] == '\n'):
		if(fileExtension == ".txt"):
			tokens[-1] = ' '	#replace new line character with a space
		elif(fileExtension == ".txtw"):
			tokens.pop()  # Remove the newline character if it exists at the end
	return tokens
	
if __name__ == "__main__":
	sequenceLengthTokens = 512
	sequenceLengthWordsApprox = sequenceLengthTokens//2		#approximate max number words per line (take into account subword tokenisation)
	#sequenceLengthWordsSpacesApprox = sequenceLengthWordsApprox//2		#approximate max number words+spaces per line 

	input_folder_path = "transcribeOut/"	#transcribeOutArchive	#transcribeOut
	output_folder_path = "TXTWsequenceLength/"
	setSequenceLength(input_folder_path, output_folder_path, ".txt", sequenceLengthWordsApprox, "text_")
	setSequenceLength(input_folder_path, output_folder_path, ".txtw", sequenceLengthWordsApprox, "text_")


