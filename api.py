import psycopg2
import psycopg2.extras  # We'll need this to convert SQL responses into Dictionaries
from flask import Flask, current_app, jsonify

app = Flask(__name__)
conn = get_db_connection()

@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")


@app.route("/stories", methods=["GET"])
def stories():
    data = {}
    return jsonify(data)

def get_db_connection():
  try:
    conn = psycopg2.connect("dbname=social_news user=postgres host=localhost")
    return conn
  except:
    print("Error connecting to database.")
