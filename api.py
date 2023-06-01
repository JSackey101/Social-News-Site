from flask import Flask, current_app, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")


@app.route("/stories", methods=["GET"])
def stories():
    data = {}
    return jsonify(data)
