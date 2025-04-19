from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/process", methods=['POST'])
def home():
	print("Processing...")
	data = request.get_json()

	url = data["url"]
	dataType = data["type"]

	print(url)
	print(dataType)

	res = {
		"status": "OK",
		"knuckles": "cracked",
		"intellij": "open",
		"chicken": "bbq"
	}

	return res