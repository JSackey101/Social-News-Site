# pylint: skip-file

import copy
from unittest.mock import patch
from api import HelpApp
from datetime import datetime


class TestStories():

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_stories_get(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.get("/stories")
        assert response.status_code == 200
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_stories_search(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.get("/stories?search=boost")
        assert response.status_code == 200
        assert len(response.json) == 1
        assert "boost" in response.json[0]['title']

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_stories_get_error(mock_load_stories, test_client, test_empty_story):
        mock_load_stories.return_value = test_empty_story

        response = test_client.get("/stories")

        assert response.status_code == 404
        assert 'message' in response.json
        assert 'error' in response.json
        assert 'No stories were found' in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    @patch('api.HelpApp.write_to_file')
    def test_post_stories(mock_write_to_file, mock_load_stories, test_client, test_basic_story, test_url, test_title):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post("/stories", json=test_url | test_title)

        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Added Successfully' in response.json['message']
        assert mock_write_to_file.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    @patch('api.HelpApp.write_to_file')
    def test_post_stories_error(mock_write_to_file, mock_load_stories, test_client, test_basic_story, test_title):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post("/stories", json=test_title)

        assert response.status_code == 400
        assert 'error' in response.json
        assert 'message' in response.json
        assert 'New story must have a url and a title' in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_stories_invalid_method(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.delete("/stories")
        assert response.status_code == 405


class TestStoryVote():

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_upvote(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/1/votes", json={"direction": "up"})
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_downvote(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/1/votes", json={"direction": "down"})
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_downvote_zero_score(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/3/votes", json={"direction": "down"})
        assert 'error' in response.json
        assert 'message' in response.json
        assert "Can't downvote for a story with 0 votes" in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_votes_id_not_found(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/6/votes", json={"direction": "down"})
        assert mock_load_stories.called == True
        assert response.status_code == 404

        assert 'error' in response.json
        assert 'message' in response.json
        assert 'ID not found' in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_votes_wrong_direction(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.post(
            "/stories/1/votes", json={"direction": "unknown"})
        assert response.status_code == 400
        assert 'error' in response.json
        assert 'message' in response.json
        assert 'Direction must be up or down' in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_stories_invalid_method(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.delete("/stories")
        assert response.status_code == 405


class TestStoriesID():

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_update_title_url(mock_load_stories, test_client, test_basic_story, test_title, test_url):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/1", json=test_title | test_url)
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_update_title(mock_load_stories, test_client, test_basic_story, test_title):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/1", json=test_title)
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_update_url(mock_load_stories, test_client, test_basic_story, test_url):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/1", json=test_url)
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Updated Successfully' in response.json['message']
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_update_id_not_found(mock_load_stories, test_client, test_basic_story, test_url):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.patch(
            "/stories/6", json=test_url)
        assert mock_load_stories.called == True
        assert response.status_code == 404

        assert 'error' in response.json
        assert 'message' in response.json
        assert 'ID not found' in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_delete(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.delete(
            "/stories/1")
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'Deleted Successfully' in response.json['message']
        assert mock_load_stories.called == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_story_delete(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)

        response = test_client.delete(
            "/stories/6")
        assert mock_load_stories.called == True
        assert response.status_code == 404

        assert 'error' in response.json
        assert 'message' in response.json
        assert 'ID not found' in response.json['message']
        assert response.json['error'] == True

    @staticmethod
    @patch('api.HelpApp.load_stories')
    def test_stories_invalid_method(mock_load_stories, test_client, test_basic_story):
        mock_load_stories.return_value = copy.deepcopy(test_basic_story)
        response = test_client.delete("/stories")
        assert response.status_code == 405


class TestHelpApp():

    @staticmethod
    def test_vote_story_up(test_basic_story):
        story = test_basic_story[0].copy()
        HelpApp.vote_story(story, "up")
        assert story['score'] == 43
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def test_vote_story_down(test_basic_story):
        story = test_basic_story[0].copy()
        HelpApp.vote_story(story, "down")
        assert story['score'] == 41
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def test_search_story(test_basic_story):
        queried_stories = HelpApp.search_stories(
            copy.deepcopy(test_basic_story), "coronavirus")
        assert len(queried_stories) == 1
        assert "coronavirus" in queried_stories[0]['title']

    @staticmethod
    def test_sort_title_descending(test_basic_story, test_title_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "title", "descending")
        assert sorted_stories == test_title_ascending_stories[::-1]

    @staticmethod
    def test_sort_title_ascending(test_basic_story, test_title_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "title", "ascending")
        assert sorted_stories == test_title_ascending_stories

    @staticmethod
    def test_sort_score_descending(test_basic_story, test_score_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "score", "descending")
        assert sorted_stories == test_score_ascending_stories[::-1]

    @staticmethod
    def test_sort_score_ascending(test_basic_story, test_score_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "score", "ascending")
        assert sorted_stories == test_score_ascending_stories

    @staticmethod
    def test_sort_created_at_descending(test_basic_story, test_created_at_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "created", "descending")
        assert sorted_stories == test_created_at_ascending_stories[::-1]

    @staticmethod
    def test_sort_created_at_ascending(test_basic_story, test_created_at_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "created", "ascending")
        assert sorted_stories == test_created_at_ascending_stories

    @staticmethod
    def test_sort_updated_at_descending(test_basic_story, test_updated_at_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "modified", "descending")
        assert sorted_stories == test_updated_at_ascending_stories[::-1]

    @staticmethod
    def test_sort_updated_at_ascending(test_basic_story, test_updated_at_ascending_stories):
        sorted_stories = HelpApp.sort_stories(copy.deepcopy(test_basic_story),
                                              "modified", "ascending")
        assert sorted_stories == test_updated_at_ascending_stories


    @staticmethod
    def test_update_story_url(test_basic_story, test_url):
        story = copy.deepcopy(test_basic_story)[0]
        HelpApp.update_story(story, test_url['url'], None)
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['url'] == test_url['url']
        assert story['website'] == "www.bbc.co.uk"

    @staticmethod
    def test_update_story_title(test_basic_story, test_title):
        story = copy.deepcopy(test_basic_story)[0]
        HelpApp.update_story(story, None, test_title['title'])
        assert story['title'] == test_title['title']

    @staticmethod
    def test_update_story_url(test_basic_story, test_url, test_title):
        story = copy.deepcopy(test_basic_story)[0]
        HelpApp.update_story(story, test_url['url'], test_title['title'])
        assert story['updated_at'] == datetime.now().strftime(
            "%a, %d %b %Y %H:%M:%S GMT")
        assert story['url'] == test_url['url']
        assert story['website'] == "www.bbc.co.uk"
        HelpApp.update_story(story, None, test_title['title'])
        assert story['title'] == test_title['title']

    @staticmethod
    def test_add_story(test_basic_story, test_url, test_title):
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
