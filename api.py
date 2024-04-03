import psycopg2
from flask import Flask, current_app, jsonify, request
from storage import save_to_file, load_from_file
from datetime import datetime

stories = [
    {
        "created_at": "Sun, 20 Mar 2022 08:43:21 GMT",
        "id": 1,
        "score": 42,
        "title": "Voters Overwhelmingly Back Community Broadband in Chicago and Denver",
        "updated_at": "Tue, 22 Mar 2022 14:58:45 GMT",
        "url": "https://www.vice.com/en/article/xgzxvz/voters-overwhelmingly-back-community-broadband-in-chicago-and-denver",
        "website": "vice.com"
    },
    {
        "created_at": "Wed, 16 Mar 2022 11:05:33 GMT",
        "id": 2,
        "score": 23,
        "title": "eBird: A crowdsourced bird sighting database",
        "updated_at": "Fri, 18 Mar 2022 13:20:47 GMT",
        "url": "https://ebird.org/home",
        "website": "ebird.org"
    },
    {
        "created_at": "Sat, 09 Apr 2022 09:11:52 GMT",
        "id": 3,
        "score": 471,
        "title": "Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake",
        "updated_at": "Mon, 11 Apr 2022 17:13:29 GMT",
        "url": "https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/",
        "website": "empireonline.com"
    },
    {
        "created_at": "Mon, 07 Feb 2022 06:21:19 GMT",
        "id": 4,
        "score": 101,
        "title": "Pfizers coronavirus vaccine is more than 90 percent effective in first analysis, company reports",
        "updated_at": "Wed, 09 Feb 2022 08:44:22 GMT",
        "url": "https://www.cnbc.com/2020/11/09/covid-vaccine-pfizer-drug-is-more-than-90percent-effective-in-preventing-infection.html",
        "website": "cnbc.com"
    },
    {
        "created_at": "Tue, 01 Mar 2022 12:31:45 GMT",
        "id": 5,
        "score": 87,
        "title": "Budget: Pensions to get boost as tax-free limit to rise",
        "updated_at": "Thu, 03 Mar 2022 15:29:58 GMT",
        "url": "https://www.bbc.co.uk/news/business-64949083",
        "website": "bbc.co.uk"
    },
    {
        "created_at": "Fri, 25 Mar 2022 10:22:36 GMT",
        "id": 6,
        "score": 22,
        "title": "Ukraine war: Zelensky honours unarmed soldier filmed being shot",
        "updated_at": "Sun, 27 Mar 2022 12:55:19 GMT",
        "url": "https://www.bbc.co.uk/news/world-europe-64938934",
        "website": "bbc.co.uk"
    },
    {
        "created_at": "Thu, 17 Mar 2022 09:28:42 GMT",
        "id": 7,
        "score": 313,
        "title": "Willow Project: US government approves Alaska oil and gas development",
        "updated_at": "Sat, 19 Mar 2022 11:34:53 GMT",
        "url": "https://www.bbc.co.uk/news/world-us-canada-64943603",
        "website": "bbc.co.uk"
    },
    {
        "created_at": "Wed, 23 Feb 2022 07:15:59 GMT",
        "id": 8,
        "score": 2,
        "title": "SVB and Signature Bank: How bad is US banking crisis and what does it mean?",
        "updated_at": "Fri, 25 Feb 2022 09:41:22 GMT",
        "url": "https://www.bbc.co.uk/news/business-64951630",
        "website": "bbc.co.uk"
    },
    {
        "created_at": "Sat, 26 Feb 2022 14:38:11 GMT",
        "id": 9,
        "score": 131,
        "title": "Aukus deal: Summit was projection of power and collaborative intent",
        "updated_at": "Mon, 28 Feb 2022 16:02:45 GMT",
        "url": "https://www.bbc.co.uk/news/uk-politics-64948535",
        "website": "bbc.co.uk"
    },
    {
        "created_at": "Thu, 24 Mar 2022 13:49:27 GMT",
        "id": 10,
        "score": 41,
        "title": "Dancer whose barefoot video went viral meets Camilla",
        "updated_at": "Sat, 26 Mar 2022 15:51:34 GMT",
        "url": "https://www.bbc.co.uk/news/uk-england-birmingham-64953863",
        "website": "bbc.co.uk"
    }
]

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    return current_app.send_static_file("./scrape/index.html")


@app.route("/stories", methods=["GET", "POST"])
def get_stories():
    pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
