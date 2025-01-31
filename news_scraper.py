from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup


def get_html(url):
    """ Get HTML from a URL. """
    page = urlopen(url)
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
    bbc_html_doc = get_html(bbc_url)
    parse_stories_bs(domain_url=bbc_url, html=bbc_html_doc)
    
