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


def error_return(message: str) -> dict:
    """ Returns an error dict with the given message. """
    return {"error": True, "message": message}


def vote_story(story: dict, direction: str) -> None:
    """ Updates the story based on whether it was up or downvoted. """
    if direction == 'up':
        story['score'] += 1
    else:
        story['score'] -= 1
    story['updated_at'] = datetime.now().strftime(
        "%a, %d %b %Y %H:%M:%S GMT")


def search_stories(stories_list: list[dict], search_term: str) -> list[dict]:
    """ Searches for stories that have the search term in their title. """
    queried_stories = [story for story in stories_list
                       if search_term.lower() in story['title'].lower()]
    return queried_stories


def sort_stories(stories_list: list[dict], sort_param: str, order_param: str = None) -> list[dict]:
    """ Sorts stories depending on given sort property and order. 
        Defaults to ascending order. """
    reverse_order = False
    if order_param == 'descending':
        reverse_order = True
    if sort_param == 'title':
        return sorted(stories_list, key=lambda val: val['title'].upper(), reverse=reverse_order)
    if sort_param == 'score':
        return sorted(
            stories_list, key=lambda val: val['score'], reverse=reverse_order)
    if sort_param == 'created':
        return sorted(stories_list,
                      key=lambda val: datetime.strptime(val['created_at'],
                                                        "%a, %d %b %Y %H:%M:%S GMT"),
                      reverse=reverse_order)
    if sort_param == 'modified':
        return sorted(stories_list,
                     key=lambda val: datetime.strptime(val['updated_at'],
                                                       "%a, %d %b %Y %H:%M:%S GMT"),
                     reverse=reverse_order)
    return None


def search_sort(search: str, sort: str, order: str) -> tuple:
    """ Returns a tuple based on the values of search and sort. """
    if search and sort:
        found_stories = search_stories(stories, search)
        if len(found_stories) == 0:
            return found_stories, 404
        return sort_stories(found_stories, sort, order), 200
    if sort:
        return sort_stories(stories, sort, order), 200
    if search:
        return search_stories(stories, search), 200
    return stories, 200


def validate_sort_order(sort: str, order: str):
    """ Validates that the sort and order values are valid"""
    if sort and sort not in ['title', 'score', 'created', 'modified']:
        return error_return("Invalid sort property"), 400
    if order and order not in ['ascending', 'descending']:
        return error_return("Invalid order property"), 400
    return None


@app.route("/", methods=["GET"])
def index():
    """ Returns the base HTML for the site. """
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    return current_app.send_static_file("./scrape/index.html")

def create_story(url: str, title: str) -> dict:
    """ Creates a new story using the input url and title. """
    new_story = {
        "created_at": datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT"),
        "updated_at": datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT"),
        "id": sorted(stories, key=lambda val: val['id'], reverse=True)[0]['id'] + 1,
        "score": 0,
        "website": url.split("/")[2],
        "url": url,
        "title": title
    }
    return new_story

@app.route("/stories", methods=["GET", "POST"])
def get_stories():
    """ Returns all of the stories. """
    if request.method == "GET":
        args = request.args.to_dict()
        search = args.get('search')
        sort = args.get('sort')
        order = args.get('order')
        val_result = validate_sort_order(sort, order)
        if val_result:
            return val_result
        if stories:
            return search_sort(search, sort, order)
        return error_return("No stories were found"), 404
    if request.method == "POST":
        data = request.get_json(silent=True)
        if "url" in data and "title" in data:
            stories.append(create_story(data['url'], data['title']))
            return {"message": "Added Successfully"}, 201
        return error_return("New story must have a url and a title."), 400
    return error_return("Invalid Request Method."), 400


@app.route("/stories/<int:id>/votes", methods=["POST"])
def add_vote(id: int):
    """ Add vote to story. """
    if request.method == "POST":
        data = request.get_json()
        print(data.get('direction'))
        if data.get("direction") in ['up', 'down']:
            for story in stories:
                if story['id'] == id:
                    if story['score'] == 0 and data.get("direction") == 'down':
                        return error_return("Can't downvote for a story with a score of 0"), 400
                    vote_story(story, data.get('direction'))
                    return {"message": "Updated Successfully"}, 201
            return error_return("ID not found"), 404
        return error_return("Direction must be up or down"), 400
    return error_return("Invalid Request Method."), 400

def update_story(story: dict, url: str, title: str) -> None:
    """ Updates an existing story using the input url/title. """
    if title:
        story['title'] = title
    if url:
        story['updated_at'] = datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        story['url'] = url
        story["website"] = url.split("/")[2]

@app.route("/stories/<int:id>", methods=(["PATCH", "DELETE"]))
def add_new_story_info(id: int):
    """ Updates existing story of input ID with new info. """
    if request.method == "PATCH":
        data = request.get_json(silent=True)
        if "url" in data or "title" in data:
            for story in stories:
                if story['id'] == id:
                    update_story(story, data.get('url'), data.get('title'))
                    return {"message": "Updated Successfully"}, 201
            return error_return("ID not found"), 404
        return error_return("Updated story data must contain url or title"), 400
    if request.method == "DELETE":
        for i, story in enumerate(stories.copy()):
            if story['id'] == id:
                stories.remove(stories[i])
                return {"message": "Deleted Successfully"}, 201
        return error_return("ID not found"), 404
    return error_return("Invalid Request Method."), 400




if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5002)
