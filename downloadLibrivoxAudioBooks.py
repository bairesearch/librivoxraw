#python downloadLibrivoxAudioBooks.py

import requests
import xml.etree.ElementTree as ET
import zipfile
import os
import io
from urllib.parse import urlparse

numberOfIndices = 20000	#CHECKTHIS	#librivox api number of index

def getLibrivoxXmlFiles(output_folder_path):
	for i in range(0, numberOfIndices):	#0
		print("i = ", i)
		
		url = "https://librivox.org/api/feed/audiobooks/?id=" + str(i)

		# Send a GET request to the URL
		response = requests.get(url)

		# Check if the request was successful (status code 200)
		if response.status_code == 200:
			# Check the Content-Type header to see if it's XML
			content_type = response.headers.get("Content-Type")
			if content_type and "xml" in content_type:
				print("Content is XML.")
				xml_content = response.content
				# Now you can work with the XML content
				parseLibrivoxXmlFile(output_folder_path, xml_content)
				
			else:
				print("Content is not XML. Content-Type:", content_type)
		else:
			print("Failed to retrieve XML content. Status code:", response.status_code)

def parseLibrivoxXmlFile(output_folder_path, xml_content):
	#print(xml_content)
	
	# Parse the XML file
	root = ET.fromstring(xml_content)	#parse

	# Check if the <error> tag exists and its content is "Audiobooks could not be found"
	error_tag = root.find('.//error')

	if error_tag is not None and error_tag.text.strip() == "Audiobooks could not be found":
		print("Error: Audiobooks could not be found")
	elif error_tag is not None:
		print("Error tag exists but content is different:", error_tag.text.strip())
	else:
		url_zip_file = root.find('.//url_zip_file').text
		print("url_zip_file = ", url_zip_file)
		if(url_zip_file is not None):
			downloadLibrivoxFile(output_folder_path, url_zip_file)
		

def downloadLibrivoxFile(output_folder_path, url_zip_file):
	extract_folder = 'extract/'
	extract_path = output_folder_path + extract_folder
	parsed_url = urlparse(url_zip_file)
	filename = os.path.basename(parsed_url.path)
	filepath = output_folder_path + filename
	
	if(not os.path.exists(filepath)):
		response = requests.get(url_zip_file)
		if response.status_code != 200:
			print("Failed to download the zip file")
			return

		# Save the zip file
		with open(filepath, 'wb') as f:
			f.write(response.content)

		# Unzip the content
		with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
			zip_ref.extractall(extract_path)


if __name__ == "__main__":
	output_folder_path = "audiobooks/"
	getLibrivoxXmlFiles(output_folder_path)

