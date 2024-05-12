#python generateNLPdataFiles.py
import os

def generate_txt_files(input_folder_path, output_folder_path, fileExtension, lines_per_file, output_file_prefix):
	# List all files in the folder
	files = os.listdir(input_folder_path)
	files.sort()  # Sort files alphabetically
	
	# Filter only .txtx files
	txt_files = [file for file in files if file.endswith(fileExtension)]
	
	output_file_suffix = fileExtension
	output_file_index = 0
	lines_accumulated = 0
	lines_buffer = []

	# Process each text file
	for txt_file in txt_files:
		input_file_path = os.path.join(input_folder_path, txt_file)
		
		# Open the input file
		with open(input_file_path, 'r') as input_file:
			for line in input_file:
				lines_buffer.append(line.lstrip())
				lines_accumulated += 1
				
				# Check if it's time to create a new output file
				if lines_accumulated >= lines_per_file:
					output_file_path = f"{output_folder_path}{output_file_prefix}{output_file_index}{output_file_suffix}"
					
					# Write accumulated lines to new file
					with open(output_file_path, 'w') as output_file:
						output_file.writelines(lines_buffer)
					
					# Reset variables for next output file
					lines_buffer = []
					lines_accumulated = 0
					output_file_index += 1
				
				# If we've reached the end of input files, create the final output file
				if not line and lines_buffer:
					output_file_path = f"{output_folder_path}{output_file_prefix}{output_file_index}{output_file_suffix}"
					
					# Write accumulated lines to new file
					with open(output_file_path, 'w') as output_file:
						output_file.writelines(lines_buffer)
					
					# Reset variables for next output file
					lines_buffer = []
					lines_accumulated = 0
					output_file_index += 1
					
if __name__ == "__main__":
	lines_per_file = 10000
	input_folder_path = "TXTWsequenceLength/"
	output_folder_path = "NLPdataFiles/"
	generate_txt_files(input_folder_path, output_folder_path, ".txt", lines_per_file, "text_")
	generate_txt_files(input_folder_path, output_folder_path, ".txtw", lines_per_file, "text_")


