from flask import Flask
from flask import render_template, session, request, redirect
import drafting
import json
import datetime
import pickle
import base64
import calculations
import random

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

kinect_data = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/kinect')
def kinect():
	print kinect_data
	return json.dumps(kinect_data)

@app.route("/JSON/<int:id>")
def return_size(id):
	filename = "static/JSON/" + str(id) + ".JSON"
	JSON = open(filename, "r")
	sizes = JSON.read()
	session["measurements"] = sizes
	return sizes

@app.route("/custom", methods=['POST'])
def save_custom():
	custom_size = {}
	for key in request.form:
		print key
		if key == "size":
			custom_size[key] = request.form.get(key)
		if key == "kinect":
			custom_size = kinect_data[request.form.get(key)]
		else:
			custom_size[key] = int(request.form.get(key))
	custom_size["girth"] = custom_size["hip"]*.77
	session["measurements"] = json.dumps(custom_size)
	print session["measurements"]
	return "200 OK"

@app.route("/patterns/<int:pattern_id>")
def return_pattern(pattern_id):
	print session["measurements"]
	use_me = json.loads(session["measurements"])
	draft = drafting.Drafting(use_me);
	if pattern_id == 1:
		filename = "static/patterns/circle_skirt" + str(random.randint(0,16384)) + ".pdf"
		draft.draft_circle_skirt(filename)
	if pattern_id == 2:
		filename = "static/patterns/skirt" + str(random.randint(0,16384)) + ".pdf"
		draft.draft_skirt(filename)
	if pattern_id == 3:
		filename = "static/patterns/leggings" + str(random.randint(0,16384)) + ".pdf"
		draft.draft_leggings(filename)
	return filename

@app.route("/calculate", methods=['POST'])
def calculate():
	body_parts = pickle.loads(base64.b64decode(request.form.get("body_parts")))
	point_cloud = pickle.loads(base64.b64decode(request.form.get("point_cloud")))
	calc = calculations.CalculationObject(point_cloud, body_parts)
	calc.calc_joint_angles()
	calc.calc_lengths()
	calc.calc_girths()
	calc.convert_measures_to_inches()
	timestamp = datetime.datetime.now().strftime("%x %X")
	kinect_data[timestamp] = calc.measures
	return "200 OK"

if __name__ == '__main__':
	app.run(debug=True)