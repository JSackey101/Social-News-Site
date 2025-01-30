""" An API for displaying news stories. """

import json
import os
from datetime import datetime
from flask import Flask, current_app, request



app = Flask(__name__)


class HelpApp():
    """ A class containing helper methods for the API. """

    ABS_PATH = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def load_stories() -> list[dict]:
        """From the JSON file, load all the stories into a python list."""
        with open(os.path.join(HelpApp.ABS_PATH, "stories.json"), encoding="UTF-8") as file:
            data = json.load(file)
            return data

    @staticmethod
    def write_to_file(stories: list[dict]) -> None:
        """Given a list of stories, rewrite them to the JSON file."""
        with open(os.path.join(HelpApp.ABS_PATH, "stories.json"), mode="w", encoding="UTF-8") as f:
            json.dump(stories, f, indent=3)

    @staticmethod
    def error_return(message: str) -> dict:
        """ Returns an error dict with the given message. """
        return {"error": True, "message": message}

    @staticmethod
    def vote_story(story: dict, direction: str) -> None:
        """ Updates the story based on whether it was up or downvoted. """
        if direction == 'up':
            story['score'] += 1
        else:
            story['score'] -= 1
        story['updated_at'] = datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def search_stories(stories_list: list[dict], search_term: str) -> list[dict]:
        """ Searches for stories that have the search term in their title. """
        queried_stories = [story for story in stories_list
                        if search_term.lower() in story['title'].lower()]
        return queried_stories

    @staticmethod
    def sort_stories(stories_list: list[dict], 
                     sort_param: str, order_param: str = None) -> list[dict]:
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

    @staticmethod
    def search_sort(stories: list[dict], search: str, sort: str, order: str) -> tuple:
        """ Returns a tuple based on the values of search and sort. """
        if search and sort:
            found_stories = HelpApp.search_stories(stories, search)
            if len(found_stories) == 0:
                return found_stories, 404
            return HelpApp.sort_stories(found_stories, sort, order), 200
        if sort:
            return HelpApp.sort_stories(stories, sort, order), 200
        if search:
            return HelpApp.search_stories(stories, search), 200
        return stories, 200

    @staticmethod
    def validate_sort_order(sort: str, order: str) -> tuple:
        """ Validates that the sort and order values are valid"""
        if sort and sort not in ['title', 'score', 'created', 'modified']:
            return HelpApp.error_return("Invalid sort property"), 400
        if order and order not in ['ascending', 'descending']:
            return HelpApp.error_return("Invalid order property"), 400
        return None

    @staticmethod
    def update_story(story: dict, url: str, title: str) -> None:
        """ Updates an existing story using the input url/title. """
        if title:
            story['title'] = title
        if url:
            story['updated_at'] = datetime.now().strftime(
                "%a, %d %b %Y %H:%M:%S GMT")
            story['url'] = url
            story["website"] = url.split("/")[2]

    @staticmethod
    def create_story(stories: list[dict], url: str, title: str) -> dict:
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

@app.route("/", methods=["GET"])
def index():
    """ Returns the base HTML for the site. """
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    """ Returns the HTML for adding a story. """
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    """ Returns the HTML for scraping stories. """
    return current_app.send_static_file("./scrape/index.html")

@app.route("/stories", methods=["GET", "POST"])
def get_stories():
    """ Returns all of the stories or adds a new story to the list. """
    stories = HelpApp.load_stories()
    if request.method == "GET":
        args = request.args.to_dict()
        search = args.get('search')
        sort = args.get('sort')
        order = args.get('order')
        val_result = HelpApp.validate_sort_order(sort, order)
        if val_result:
            return val_result
        if stories:
            return HelpApp.search_sort(stories, search, sort, order)
        return HelpApp.error_return("No stories were found"), 404
    if request.method == "POST":
        data = request.get_json(silent=True)
        if "url" in data and "title" in data:
            stories.append(HelpApp.create_story(stories, data['url'], data['title']))
            HelpApp.write_to_file(stories)
            return {"message": "Added Successfully"}, 201
        return HelpApp.error_return("New story must have a url and a title."), 400
    return HelpApp.error_return("Invalid Request Method."), 405


@app.route("/stories/<int:s_id>/votes", methods=["POST"])
def add_vote(s_id: int):
    """ Add vote to story. """
    stories = HelpApp.load_stories()
    if request.method == "POST":
        data = request.get_json()
        if data.get("direction") in ['up', 'down']:
            for story in stories:
                if story['id'] == s_id:
                    if story['score'] == 0 and data.get("direction") == 'down':
                        return HelpApp.error_return("Can't downvote for a story with 0 votes"), 400
                    HelpApp.vote_story(story, data.get('direction'))
                    HelpApp.write_to_file(stories)
                    return {"message": "Updated Successfully"}, 201
            return HelpApp.error_return("ID not found"), 404
        return HelpApp.error_return("Direction must be up or down"), 400
    return HelpApp.error_return("Invalid Request Method."), 405

@app.route("/stories/<int:s_id>", methods=(["PATCH", "DELETE"]))
def update_story_info(s_id: int):
    """ Updates existing story of input ID with new info or deletes existing story by ID. """
    stories = HelpApp.load_stories()
    if request.method == "PATCH":
        data = request.get_json(silent=True)
        if "url" in data or "title" in data:
            for story in stories:
                if story['id'] == s_id:
                    HelpApp.update_story(
                        story, data.get('url'), data.get('title'))
                    HelpApp.write_to_file(stories)
                    return {"message": "Updated Successfully"}, 201
            return HelpApp.error_return("ID not found"), 404
        return HelpApp.error_return("Updated story data must contain url or title"), 400
    if request.method == "DELETE":
        for i, story in enumerate(stories.copy()):
            if story['id'] == s_id:
                stories.remove(stories[i])
                HelpApp.write_to_file(stories)
                return {"message": "Deleted Successfully"}, 201
        return HelpApp.error_return("ID not found"), 404
    return HelpApp.error_return("Invalid Request Method."), 405




if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=8000)
