""" Contains functions to scrape news from a website. """

from urllib.request import urlopen
from requests import HTTPError
from bs4 import BeautifulSoup


def get_html(url):
    """ Get HTML from a URL. """
    try:
        with urlopen(url) as urlpage:
            page = urlpage
            html_bytes = page.read()
            html_doc = html_bytes.decode("utf_8")
    except ValueError as err:
        raise HTTPError("Invalid Link. ") from err
    return html_doc

def parse_stories_bs(domain_url, html):
    """ Create a list of story dictionaries containing title and url for input HTML. """
    stories_list = []
    soup = BeautifulSoup(html, "html.parser")
    stories_list = soup.css.select(".e1vyq2e80")
    story_list = []
    for story in stories_list:
        # Skips over BBC Videos and the Country News Pages.
        if story.find('span', class_="visually-hidden ssrcss-1f39n02-VisuallyHidden e16en2lz0"
                      ) is not None or len(str(story.find('p')).split(" ")) < 5:
            continue
        story_dict = {}
        story_dict['title'] = str(story.find(
            'p', class_="ssrcss-1b1mki6-PromoHeadline exn3ah96")).split(">")[2].split("<")[0]
        story_dict['url'] = domain_url + str(story.find("a")['href'])
        story_list.append(story_dict)
    return story_list


if __name__ == "__main__":
    BBC_URL = "http://bbc.co.uk"
    bbc_html_doc = get_html(BBC_URL)
    stories = parse_stories_bs(domain_url=BBC_URL, html=bbc_html_doc)
