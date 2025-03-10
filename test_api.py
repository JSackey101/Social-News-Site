""" Contains tests for the Social News Site. """

import copy
from datetime import datetime
from unittest.mock import patch, MagicMock
from api import HelpApp
from news_scraper import get_html, parse_stories_bs
from requests import HTTPError

class TestNewsScraper():
    """ Class for Testing the functions in news_scraper.py; """

    @staticmethod
    @patch("news_scraper.urlopen")
    def test_get_html(mock_open,test_html_bytes):
        """ Tests whether the urlopen is called, .read() is called and the html is decoded. """
        mock_response = MagicMock()
        mock_response.read.return_value = test_html_bytes

        mock_open.return_value.__enter__.return_value = mock_response

        html_bytes =  get_html("https://www.newssite.com")

        mock_open.assert_called_once_with("https://www.newssite.com")
        mock_response.read.assert_called_once()
        assert html_bytes == "Hello World!"

    @staticmethod
    def test_parse_stories_video(test_video_html, test_normal_story_A):
        """ Tests whether Video stories are skipped over. """
        stories = parse_stories_bs("https://www.newssite.com", 
                                   test_video_html + test_normal_story_A)

        assert len(stories) == 1

    @staticmethod
    def test_parse_stories_language(test_language_html, test_normal_story_A):
        """ Tests whether Language web pages are skipped over. """
        stories = parse_stories_bs(
            "https://www.newssite.com", test_language_html + test_normal_story_A)

        assert len(stories) == 1

    @staticmethod
    def test_parse_stories_one(test_normal_story_A):
        """ Tests whether a story is created correctly for 1 HTML story given. """
        stories = parse_stories_bs(
            "https://www.newssite.com", test_normal_story_A)
        assert len(stories) == 1
        assert stories[0]['title'] == 'Breaking News: New Developments in the Tech Industry'
        assert stories[0]['url'] == 'https://www.newssite.com/news/technology-12345'

    @staticmethod
    def test_parse_stories_two(test_normal_story_A, test_normal_story_B):
        """ Tests whether stories are created correctly for more than 1 HTML story given. """
        stories = parse_stories_bs(
            "https://www.newssite.com", test_normal_story_A + test_normal_story_B)
        assert len(stories) == 2
        assert stories[0]['title'] == 'Breaking News: New Developments in the Tech Industry'
        assert stories[0]['url'] == 'https://www.newssite.com/news/technology-12345'
        assert stories[1]['title'] == 'Global Warming: The Impact on Our Oceans'
        assert stories[1]['url'] == 'https://www.newssite.com/news/environment-67890'

class TestScrapeStories():
    """ Class for testing the /scrape route. """

    @staticmethod
    @patch('api.get_html')
    @patch('api.save_to_file')
    @patch('api.load_from_file')
    def test_scrape(mock_load_stories, mock_save_to_file, mock_get_html, test_client, test_normal_story_A, test_basic_story):
        """ Tests whether stories are scraped correctly. """
        mock_get_html.return_value = test_normal_story_A
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.post(
            "/scrape", json={'url': 'https://www.newssite.com'})
        assert response.status_code == 201
        assert mock_load_stories.called is True
        assert mock_save_to_file.called is True

    @staticmethod
    @patch('api.get_html')
    @patch('api.save_to_file')
    @patch('api.load_from_file')

    def test_invalid_url(mock_load_stories, _, mock_get_html, test_client, test_basic_story):
        """ Tests whether a bad request error is returned for an invalid URL. 
            (which raises a HTTPError) """
        mock_get_html.side_effect = HTTPError("Invalid Url. ")
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/scrape", json={'url': 'https://www.newssite.com'})
        assert response.status_code == 400

    @staticmethod
    @patch('api.load_from_file')

    def test_no_url_header(_, test_client):
        """ Tests whether a bad request error is returned when the head is not 'url'. """
        response = test_client.post(
            "/scrape", json={'link': 'https://www.newssite.com'})
        assert response.status_code == 400

    @staticmethod
    @patch('api.get_html')
    @patch('api.load_from_file')
    def test_no_scraped_stories(mock_load_stories, mock_get_html, test_client, test_basic_story):
        """ Tests whether a not found error is returned when no stories are scraped. """
        mock_get_html.return_value = ""
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/scrape", json={'url': 'https://www.newssite.com'})
        assert response.status_code == 404


class TestStories():
    """ Class for Testing the /stories route. """

    @staticmethod
    @patch('api.load_from_file')
    def test_stories_get(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route loads the stories for a get request. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.get("/stories")
        assert response.status_code == 200
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_stories_search(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route loads only matching stories 
            for a get request with a search query. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.get("/stories?search=boost")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert "boost" in response.json[0]['title']

    @staticmethod
    @patch('api.load_from_file')
    def test_stories_get_error(mock_load_stories, test_client, test_empty_story):
        """ Tests whether the route sends a not found error 
            for a get request when no stories are found. """
        mock_load_stories.return_value = test_empty_story

        response = test_client.get("/stories")

        assert response.status_code == 404
        assert 'message' in response.json
        assert 'error' in response.json
        assert 'No stories were found' in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    @patch('api.save_to_file')
    def test_post_stories(mock_write_to_file, mock_load_stories, test_client, test_basic_story, test_url, test_title):
        """ Tests whether the route adds a story for a post request. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post("/stories", json=test_url | test_title)

        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Added Successfully' in response.json['message']
        assert mock_write_to_file.called is True

    @staticmethod
    @patch('api.load_from_file')
    @patch('api.save_to_file')
    def test_post_stories_error(_, mock_load_stories, test_client, test_basic_story, test_title):
        """ Tests whether the route sends a bad request error 
            for a post request that is missing data. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post("/stories", json=test_title)

        assert response.status_code == 400
        assert 'error' in response.json
        assert 'message' in response.json
        assert 'New story must have a url and a title' in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    def test_stories_invalid_method(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route sends a method not allowed error 
            when the request method is not one allowed by the route. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.delete("/stories")
        assert response.status_code == 405


class TestStoryVote():
    """ Class for Testing the /stories/<int:s_id>/votes route. """

    @staticmethod
    @patch('api.load_from_file')
    def test_story_upvote(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route updates a given story by +1 vote when direction is up. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/1/votes", json={"direction": "up"})
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_downvote(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route updates a given story by -1 vote when direction is down. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/1/votes", json={"direction": "down"})
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_downvote_zero_score(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route returns a bad request error 
            when trying to downvote a stories with 0 votes. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/3/votes", json={"direction": "down"})
        assert response.status_code == 400
        assert 'error' in response.json
        assert 'message' in response.json
        assert "Can't downvote for a story with 0 votes" in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_votes_id_not_found(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the not found error is returned when 
            trying to change the votes of a story that does not exist. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/6/votes", json={"direction": "down"})
        assert mock_load_stories.called is True
        assert response.status_code == 404

        assert 'error' in response.json
        assert 'message' in response.json
        assert 'ID not found' in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_votes_wrong_direction(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the bad request error is returned 
            when the direction given is not up or down. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/1/votes", json={"direction": "unknown"})
        assert response.status_code == 400
        assert 'error' in response.json
        assert 'message' in response.json
        assert 'Direction must be up or down' in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    def test_stories_invalid_method(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route sends a method not allowed error 
            when the request method is not one allowed by the route. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.delete("/stories")
        assert response.status_code == 405


class TestStoriesID():

    """ Class for Testing the /stories/<int:s_id> route. """

    @staticmethod
    @patch('api.load_from_file')
    def test_story_update_title_url(mock_load_stories, test_client, 
                                    test_basic_story, test_title, test_url):
        """ Tests whether the route updates the title and url of a story when both are given. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/1", json=test_title | test_url)
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_update_title(mock_load_stories, test_client, test_basic_story, test_title):
        """ Tests whether the route updates the title of a story when given. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/1", json=test_title)
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_update_url(mock_load_stories, test_client, test_basic_story, test_url):
        """ Tests whether the route updates the url of a story when given. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/1", json=test_url)
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_update_id_not_found(mock_load_stories, test_client, test_basic_story, test_url):
        """ Tests whether the not found error is returned when trying to update a story that does not exist. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/6", json=test_url)
        assert mock_load_stories.called is True
        assert response.status_code == 404

        assert 'error' in response.json
        assert 'message' in response.json
        assert 'ID not found' in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_delete(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the story is deleted from the list. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.delete(
            "/stories/1")
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Deleted Successfully' in response.json['message']
        assert mock_load_stories.called is True

    @staticmethod
    @patch('api.load_from_file')
    def test_story_delete_not_found(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the not found error is returned when trying to delete a story that does not exist. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.delete(
            "/stories/6")
        assert mock_load_stories.called is True
        assert response.status_code == 404

        assert 'error' in response.json
        assert 'message' in response.json
        assert 'ID not found' in response.json['message']
        assert response.json['error'] is True

    @staticmethod
    @patch('api.load_from_file')
    def test_stories_invalid_method(mock_load_stories, test_client, test_basic_story):
        """ Tests whether the route sends a method not allowed error when the request method is not one allowed by the route. """
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.delete("/stories")
        assert response.status_code == 405


class TestHelpApp():

    """ Class for Testing the HelpApp class. """

    @staticmethod
    def test_vote_story_up(test_basic_story):
        """ Tests whether the story's score is increased by 1 and 
            the story shows that is has just been updated. """
        story = test_basic_story[0].copy()
        HelpApp.vote_story(story, "up")
        assert story['score'] == 43
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def test_vote_story_down(test_basic_story):
        """ Tests whether the story's score is decreased by 1 
            and the story shows that is has just been updated. """
        story = test_basic_story[0].copy()
        HelpApp.vote_story(story, "down")
        assert story['score'] == 41
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def test_search_story(test_basic_story):
        """ Tests whether the stories are filtered correctly by search terms. """
        queried_stories = HelpApp.search_stories(
            copy.deepcopy(test_basic_story), "coronavirus")
        assert len(queried_stories) == 1
        assert "coronavirus" in queried_stories[0]['title']

    @staticmethod
    def test_sort_title_descending(test_basic_story, test_title_ascending_stories):
        """ Tests whether the stories are sorted by title in descending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "title", "descending")
        assert sorted_stories == test_title_ascending_stories[::-1]

    @staticmethod
    def test_sort_title_ascending(test_basic_story, test_title_ascending_stories):
        """ Tests whether the stories are sorted by title in ascending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "title", "ascending")
        assert sorted_stories == test_title_ascending_stories

    @staticmethod
    def test_sort_score_descending(test_basic_story, test_score_ascending_stories):
        """ Tests whether the stories are sorted by score in descending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "score", "descending")
        assert sorted_stories == test_score_ascending_stories[::-1]

    @staticmethod
    def test_sort_score_ascending(test_basic_story, test_score_ascending_stories):
        """ Tests whether the stories are sorted by score in ascending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "score", "ascending")
        assert sorted_stories == test_score_ascending_stories

    @staticmethod
    def test_sort_created_at_descending(test_basic_story, test_created_at_ascending_stories):
        """ Tests whether the stories are sorted by created date in descending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "created", "descending")
        assert sorted_stories == test_created_at_ascending_stories[::-1]

    @staticmethod
    def test_sort_created_at_ascending(test_basic_story, test_created_at_ascending_stories):
        """ Tests whether the stories are sorted by created date in ascending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "created", "ascending")
        assert sorted_stories == test_created_at_ascending_stories

    @staticmethod
    def test_sort_updated_at_descending(test_basic_story, test_updated_at_ascending_stories):
        """ Tests whether the stories are sorted by updated date in descending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "modified", "descending")
        assert sorted_stories == test_updated_at_ascending_stories[::-1]

    @staticmethod
    def test_sort_updated_at_ascending(test_basic_story, test_updated_at_ascending_stories):
        """ Tests whether the stories are sorted by updated date in ascending order. """
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "modified", "ascending")
        assert sorted_stories == test_updated_at_ascending_stories


    @staticmethod
    def test_update_story_url(test_basic_story, test_url):
        """ Tests whether the story's url is updated alongside the 
            website and the story shows that is has just been updated. """
        story = copy.deepcopy(test_basic_story)[0]
        HelpApp.update_story(story, test_url['url'], None)
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['url'] == test_url['url']
        assert story['website'] == "www.bbc.co.uk"

    @staticmethod
    def test_update_story_title(test_basic_story, test_title):
        """ Tests whether the story's title is updated and 
            the story shows that is has just been updated. """
        story = copy.deepcopy(test_basic_story)[0]
        HelpApp.update_story(story, None, test_title['title'])
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['title'] == test_title['title']

    @staticmethod
    def test_update_story_url_title(test_basic_story, test_url, test_title):
        """ Tests whether the story's url and title are updated and 
            the story shows that is has just been updated. """
        story = copy.deepcopy(test_basic_story)[0]
        HelpApp.update_story(story, test_url['url'], test_title['title'])
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['url'] == test_url['url']
        assert story['website'] == "www.bbc.co.uk"
        assert story['title'] == test_title['title']

    @staticmethod
    def test_create_story(test_basic_story, test_url, test_title):
        """ Tests whether a new story is created properly. """
        story = HelpApp.create_story(test_basic_story, test_url['url'], test_title['title'])
        assert story['created_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['id'] == 6
        assert story['website'] == "www.bbc.co.uk"
        assert story['url'] == test_url['url']
        assert story['title'] == test_title['title']
        assert story['score'] == 0
