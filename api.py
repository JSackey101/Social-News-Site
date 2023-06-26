from flask import Flask, current_app, jsonify

data = [
    {
        "id": 0,
        "title": "Abdul Sharifu Was Buying Milk For A Neighbor's Baby. A Snowstorm Killed Him. ",
        "url": "https://www.buzzfeednews.com/article/albertsamaha/abdul-sharifu-buffalo-blizzard-2022"
    },
    {
        "id": 1,
        "title": "Amazon Warehouse Worker Daniel Olayiwola Decided To Make A Podcast About Amazon's Working Conditions",
        "url": "https://www.buzzfeednews.com/article/albertsamaha/daniel-olayiwola-amazon-scamazon-podcast"
    },
    {
        "id": 2,
        "title": "Eight People Share What It's Like To Live On $100,000 A Year",
        "url": "https://www.buzzfeednews.com/article/venessawong/six-figure-salary-100k-a-year"
    },
    {
        "id": 3,
        "title": "Biden's Student Loan Forgiveness Plan Is Now On Hold. If You Applied, Tell Us What Your Plans Are.",
        "url": "https://www.buzzfeednews.com/article/venessawong/bidens-student-loan-forgiveness-plan-is-now-on-hold-if-you"
    },
    {
        "id": 4,
        "title": "How A Group Of Dancers Sparked A Unionization Effort At A Los Angeles Strip Club",
        "url": "https://www.buzzfeednews.com/article/otilliasteadman/strippers-unionizing-star-garden"
    }
]

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")


@app.route("/stories", methods=["GET"])
def stories():
    return jsonify(data)
