#python convertNLPdataFilesTokeniseProsody.py
import os

prosodyDelimitedData = True
if(prosodyDelimitedData):
	#FUTURE update prosodyDelimitedData implementation to reserve special tokenizer tokens for prosodyDelimiterToken
	prosodyDelimitedUniqueTokens = False
	prosodyDelimiterToken = '\u6F22' #random chinese character
	#prosodyDelimiterTokenStart = '<'
	#prosodyDelimiterTokenEnd = 'S>'
	prosodyDelimiterTokenStart = prosodyDelimiterToken
	prosodyDelimiterTokenEnd = ''
	debugProsodyDelimitedData = False

def convertNLPdataFilesTokeniseProsody(input_folder_path, output_folder_path, fileExtension, fileExtensionOut, prosodyDelimitedUniqueTokens):
	# List all files in the folder
	files = os.listdir(input_folder_path)
	files = [file for file in files if file.endswith(fileExtension)]
	files = sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0]))	#robust alphabetical sort (indexed file names that are not padded with 0s)
	
	# Filter only .txt files
	txt_files = [file for file in files if file.endswith(fileExtension)]
	
	output_file_suffix = fileExtensionOut
	output_file_index = 0
	lines_accumulated = 0
	lines_buffer = []

	# Process each text file
	for txt_file in txt_files:
		input_file_path = os.path.join(input_folder_path, txt_file)
		
		# Open the input file
		text = []
		with open(input_file_path, 'r') as input_file:
			for line in input_file:
				text.append(line)

		text = replaceProsodySpaceWithTokens(text, prosodyDelimitedUniqueTokens)

		# Write accumulated lines to new file
		output_file_name = os.path.splitext(os.path.basename(txt_file))[0]
		output_file_path = f"{output_folder_path}{output_file_name}{output_file_suffix}"
		with open(output_file_path, 'w') as output_file:
			output_file.writelines(text)

def replaceProsodySpaceWithTokens(text, prosodyDelimitedUniqueTokens):
	for index in range(len(text)):
		line = text[index]
		if(prosodyDelimitedUniqueTokens):
			for i in range(100, 0, -1):  # Replace up to 100 consecutive spaces
				line = line.replace(' ' * i, f'{prosodyDelimiterTokenStart}{i}{prosodyDelimiterTokenEnd}')
		else:
			line = line.replace(' ', f'{prosodyDelimiterToken}')
		if(debugProsodyDelimitedData):
			print("line = ", line)
		text[index] = line
	return text
	
if __name__ == "__main__":
	input_folder_path = "NLPdataFiles/"
	output_folder_path = "NLPdataFilesProsodyTokens/"
	convertNLPdataFilesTokeniseProsody(input_folder_path, output_folder_path, ".txt", ".txtptc", False)	#prosodyDelimitedType="controlTokens"	#replace single space characters with tokens
	convertNLPdataFilesTokeniseProsody(input_folder_path, output_folder_path, ".txtw", ".txtptr", False)	#prosodyDelimitedType="repeatTokens"	#replace repeated space characters with tokens
	convertNLPdataFilesTokeniseProsody(input_folder_path, output_folder_path, ".txtw", ".txtptu", True)	#prosodyDelimitedType="uniqueTokens"	#replace repeated space characters with unique token


