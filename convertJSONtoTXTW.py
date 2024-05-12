#python convertJSONtoTXTW.py
import os
import json
import statistics
import math
from typing import TextIO

def convertJSONtoTXTW(input_folder_path, output_folder_path, output_file_suffix):

	# List all files in the folder
	files = os.listdir(input_folder_path)
	files.sort()  # Sort files alphabetically
	
	# Filter only .json files
	json_files = [file for file in files if file.endswith(".json")]
	
	# Process each text file
	for json_file in json_files:
		input_file_path = os.path.join(input_folder_path, json_file)
		
		# Open the input file
		with open(input_file_path, 'r') as file:
			xmlParseTree = json.load(file)

		output_file_suffix = output_file_suffix
		output_file_name = os.path.splitext(os.path.basename(json_file))[0]
		output_file_path = f"{output_folder_path}{output_file_name}{output_file_suffix}"
		with open(output_file_path, "w", encoding="utf-8") as f:
			WriteTXTW(xmlParseTree, file=f)

#code extracted from https://github.com/bairesearch/whisperX/tree/branch-addWriteTSVWandTXTW whisperx/utils.py:

def WriteTXTW(result: dict, file: TextIO):
    '''
    - take the median (not average) interval length between spoken words = I
    - for each interval length i between words calculate prosody = i/I
    - calculate number prosody tokens (or type of prosody token) = int((i*3)/I)
    - generate text with repeated prosody tokens between words
    '''

    averageInterval = calculateMedianInterval(result)

    previousWordEnd = 0
    for segment in result["segments"]:
        #print("\nsegment:")
        if "words" in segment:
            for word in segment["words"]:
                if "start" in word:
                    if(previousWordEnd > 0):
                        i = 1000*word["start"] - previousWordEnd
                        #print("i = ", i)
                        prosodyString = generateProsodyTokens(i, averageInterval)
                        print(prosodyString, file=file, end="")
                    print(word["word"], file=file, end="")
                    previousWordEnd = 1000*word["end"]
        print("", file=file, flush=True)

def generateProsodyTokens(i, averageInterval):
    averageNumberProsodyTokens = 3
    prosodyToken = ' '    #CHECKTHIS

    numberProsodyTokens = math.ceil((i*averageNumberProsodyTokens)/averageInterval)
    prosodyString = prosodyToken * numberProsodyTokens
    return prosodyString

def calculateMedianInterval(result):
    previousWordEnd = 0
    #averageInterval = 0
    #wordCount = 0
    intervalList = []
    for segment in result["segments"]:
        if "words" in segment:
            for word in segment["words"]:
                if "start" in word:
                    if(previousWordEnd > 0):
                        i = 1000*word["start"] - previousWordEnd
                        intervalList.append(i)
                        #averageInterval += i
                        #wordCount += 1
                    previousWordEnd = 1000*word["end"]
    #averageInterval /= wordCount
    averageInterval = statistics.median(intervalList)
    return averageInterval
            
			
if __name__ == "__main__":
	input_folder_path = "transcribeOutArchive/"
	output_folder_path = "TXTWregeneratedFromJson/"
	convertJSONtoTXTW(input_folder_path, output_folder_path, ".txtw")


