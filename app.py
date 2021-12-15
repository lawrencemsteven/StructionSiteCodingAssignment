from flask import Flask, request, send_file
import urllib.request
import os
import shutil

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	# Display Basic Get Request
	if request.method == 'GET':
		return "<h1>Hello World!</h1>"
	
	# Post Request Reads JSON Data
	else:
		data = request.get_json(force=True)

		# Clear files/ directory
		if os.path.exists("files/"):
			shutil.rmtree("files/")
		os.mkdir("files/")

		# Fetch data from each link and write it to file in files
		for link in data:
			with urllib.request.urlopen(link['url']) as f:
				file_not_saved = True
				while (file_not_saved):
					try:
						with open("files/"+link['filename'], 'wb') as file:
							file.write(f.read())
							file.close()
							file_not_saved = False
					except FileNotFoundError:
						# Repeat step if files are currently being zipped
						file_not_saved = True

		return get_files()
	

@app.route("/get_files")
def get_files():
	# Zip files and send to user
	shutil.make_archive("files", "zip", "files")
	return send_file("files.zip")