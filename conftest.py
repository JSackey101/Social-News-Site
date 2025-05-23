""" Contains Fixtures for the tests. """

from api import app
import pytest


@pytest.fixture(scope='module')
def test_client():
    """ Returns the test client for the app. """
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def test_basic_story():
    """ Returns a basic set of stories. """
    return [
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
            "created_at": "Sat, 09 Apr 2022 09:11:52 GMT",
            "id": 3,
            "score": 0,
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
        }]


@pytest.fixture
def test_empty_story():
    """ Returns an empty list. """
    return []


@pytest.fixture
def test_url():
    """ Returns a URL request body. """
    return {"url": "https://www.bbc.co.uk/news/articles/cp82jvd3g54o"}


@pytest.fixture
def test_title():
    """ Returns a title request body. """
    return {"title": "Shoplifters 'out of control' and becoming more brazen, say retailers"}


@pytest.fixture
def test_title_ascending_stories():
    """ Returns a list of stories ascending by title. """
    return [
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
            "created_at": "Sat, 09 Apr 2022 09:11:52 GMT",
            "id": 3,
            "score": 0,
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
            "created_at": "Sun, 20 Mar 2022 08:43:21 GMT",
            "id": 1,
            "score": 42,
            "title": "Voters Overwhelmingly Back Community Broadband in Chicago and Denver",
            "updated_at": "Tue, 22 Mar 2022 14:58:45 GMT",
            "url": "https://www.vice.com/en/article/xgzxvz/voters-overwhelmingly-back-community-broadband-in-chicago-and-denver",
            "website": "vice.com"
        }
    ]


@pytest.fixture
def test_score_ascending_stories():
    """ Returns a list of stories ascending by score. """
    return [
        {
            "created_at": "Sat, 09 Apr 2022 09:11:52 GMT",
            "id": 3,
            "score": 0,
            "title": "Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake",
            "updated_at": "Mon, 11 Apr 2022 17:13:29 GMT",
            "url": "https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/",
            "website": "empireonline.com"
        },
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
            "created_at": "Tue, 01 Mar 2022 12:31:45 GMT",
            "id": 5,
            "score": 87,
            "title": "Budget: Pensions to get boost as tax-free limit to rise",
            "updated_at": "Thu, 03 Mar 2022 15:29:58 GMT",
            "url": "https://www.bbc.co.uk/news/business-64949083",
            "website": "bbc.co.uk"
        },
        {
            "created_at": "Mon, 07 Feb 2022 06:21:19 GMT",
            "id": 4,
            "score": 101,
            "title": "Pfizers coronavirus vaccine is more than 90 percent effective in first analysis, company reports",
            "updated_at": "Wed, 09 Feb 2022 08:44:22 GMT",
            "url": "https://www.cnbc.com/2020/11/09/covid-vaccine-pfizer-drug-is-more-than-90percent-effective-in-preventing-infection.html",
            "website": "cnbc.com"
        }
    ]


@pytest.fixture
def test_created_at_ascending_stories():
    """ Returns a list of stories ascending by creation date. """
    return [
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
            "created_at": "Sun, 20 Mar 2022 08:43:21 GMT",
            "id": 1,
            "score": 42,
            "title": "Voters Overwhelmingly Back Community Broadband in Chicago and Denver",
            "updated_at": "Tue, 22 Mar 2022 14:58:45 GMT",
            "url": "https://www.vice.com/en/article/xgzxvz/voters-overwhelmingly-back-community-broadband-in-chicago-and-denver",
            "website": "vice.com"
        },
        {
            "created_at": "Sat, 09 Apr 2022 09:11:52 GMT",
            "id": 3,
            "score": 0,
            "title": "Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake",
            "updated_at": "Mon, 11 Apr 2022 17:13:29 GMT",
            "url": "https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/",
            "website": "empireonline.com"
        }
    ]


@pytest.fixture
def test_updated_at_ascending_stories():
    """ Returns a list of stories ascending by modification date. """
    return [
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
            "created_at": "Sun, 20 Mar 2022 08:43:21 GMT",
            "id": 1,
            "score": 42,
            "title": "Voters Overwhelmingly Back Community Broadband in Chicago and Denver",
            "updated_at": "Tue, 22 Mar 2022 14:58:45 GMT",
            "url": "https://www.vice.com/en/article/xgzxvz/voters-overwhelmingly-back-community-broadband-in-chicago-and-denver",
            "website": "vice.com"
        },
        {
            "created_at": "Sat, 09 Apr 2022 09:11:52 GMT",
            "id": 3,
            "score": 0,
            "title": "Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake",
            "updated_at": "Mon, 11 Apr 2022 17:13:29 GMT",
            "url": "https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/",
            "website": "empireonline.com"
        }
    ]

@pytest.fixture
def test_html_bytes():
    """ Returns byte data. """
    return b'Hello World!'

@pytest.fixture
def test_video_html():
    """ Returns HTML representing a video article. """
    return """<div class="e1vyq2e80">
<span class="visually-hidden ssrcss-1f39n02-VisuallyHidden e16en2lz0">Video: How AI is Changing the Future</span>
<a href="/news/technology-10101">Watch the video</a>
</div>"""

@pytest.fixture
def test_normal_story_A():
    """ Returns HTML representing a normal story. """
    return """<div class="e1vyq2e80">
<p class="ssrcss-1b1mki6-PromoHeadline exn3ah96"><span aria-hidden="false">Breaking News: New Developments in the Tech Industry</span></p>
<a href="/news/technology-12345">Read more</a>
</div>"""

@pytest.fixture
def test_language_html():
    """ Returns HTML representing a language page. """
    return """<div class="e1vyq2e80">
<p class="ssrcss-1b1mki6-PromoHeadline exn3ah96"><span aria-hidden="false">Wales</span></p>
<a href="/wales"></a>
</div>"""


@pytest.fixture
def test_normal_story_B():
    """ Returns HTML representing a normal story. """
    return """<div class="e1vyq2e80">
<p class="ssrcss-1b1mki6-PromoHeadline exn3ah96"><span aria-hidden="false">Global Warming: The Impact on Our Oceans</span></p>
<a href="/news/environment-67890">Read more</a>
</div>
"""
