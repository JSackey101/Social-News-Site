""" Contains functions to scrape news from a website. """

from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_html(url):
    """ Get HTML from a URL. """
    with urlopen(url) as urlpage:
        page = urlpage
    html_bytes = page.read()
    html_doc = html_bytes.decode("utf_8")
    return html_doc


def parse_stories_bs(domain_url, html):
    """ Create a list of story dictionaries containing title and url for input HTML. """
    stories = []
    soup = BeautifulSoup(html, "html.parser")
    stories = soup.css.select(".e1vyq2e80")
    story_list = []
    for story in stories:
        story_dict = {}
        story_dict['title'] = str(story.find('p'))[
            75:].split('<', maxsplit=1)[0]
        story_dict['url'] = domain_url + str(story.find("a")['href'])
        story_list.append(story_dict)
    return story_list


if __name__ == "__main__":
    BBC_URL = "http://bbc.co.uk"
    bbc_html_doc = get_html(BBC_URL)
    parse_stories_bs(domain_url=BBC_URL, html=bbc_html_doc)
