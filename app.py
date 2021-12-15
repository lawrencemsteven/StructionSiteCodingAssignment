from flask import Flask, request, send_file
import urllib.request
import os
import shutil

app = Flask(__name__)

progress = 0
progress_total = 0

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == 'GET':
		return "<h1>Hello World!</h1>"
	else:
		data = request.get_json(force=True)
		if os.path.exists("files/"):
			shutil.rmtree("files/")
		os.mkdir("files/")
		progress = 0
		progress_total = len(data)
		for link in data:
			print(link['url'])
			with urllib.request.urlopen(link['url']) as f:
				file_not_saved = True
				while (file_not_saved):
					try:
						with open("files/"+link['filename'], 'wb') as file:
							file.write(f.read())
							file.close()
							file_not_saved = False
							progress += 1
					except FileNotFoundError:
						file_not_saved = True

		return get_files()
	

@app.route("/get_files")
def get_files():
	shutil.make_archive("files", "zip", "files")
	return send_file("files.zip")