from flask import Flask
from flask import render_template, session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/kinect')
def open_kinect():
	return "Open kinect window!"

if __name__ == '__main__':
    app.run(debug=True)