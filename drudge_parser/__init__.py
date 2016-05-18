from collections import namedtuple
from enum import Enum
from itertools import chain
from urllib.request import urlopen
from types import coroutine

from bs4 import BeautifulSoup


class Location(Enum):
    TOP_STORY = 'TOP_STORY'
    MAIN_HEADLINE = 'MAIN_HEADLINE'
    COLUMN = 'COLUMN'


Article = namedtuple('Article', 'title href location')
Image = namedtuple('Image', 'src')


@coroutine
def scrape_site(timeout=5):
    """Scrape the live web site, an exception will be thrown
    if the site is not accessible within the timeout
    :param timeout: timeout in seconds
    :return: yields a tuple of (Article, Image) on each iteration. Note that
             the Image can (and often is) None - meaning no image is associated
             with the article.
    """
    with urlopen('http://drudgereport.com/', timeout=timeout) as page:
        yield from scrape_stream(page)


@coroutine
def scrape_stream(stream):
    """Parse the articles/images from an input stream,
    :param stream: file like object
    :return: yields an article and an image on each iteration
    """
    soup = BeautifulSoup(stream, 'html5lib')
    yield from chain(parse_top_stories(soup),
                     parse_main_headlines(soup),
                     parse_columns(soup))


@coroutine
def process_tags(tags, location):
    img = None
    for tag in tags:
        # We have crossed into another section.
        if tag.name == 'div' and tag.attrs.get('id', '') == 'app_mainheadline':
            break

        # Reset, new sub-section of related articles/images
        if tag.name == 'hr':
            img = None
            continue

        if tag.name == 'img':
            src = tag.attrs.get('src', '').rstrip()
            img = Image(src)
        elif tag.name == 'a':
            title = tag.text.rstrip().replace('\n', ' ')
            href = tag.attrs.get('href', '').rstrip()
            yield Article(title, href, location.value), img


@coroutine
def parse_main_headlines(soup):
    mainheadline = soup.find('div', {'id': 'app_mainheadline'})
    tags = mainheadline.find_all(['img', 'a'])
    yield from process_tags(tags, Location.MAIN_HEADLINE)


@coroutine
def parse_top_stories(soup):
    topstories = soup.find('div', {'id': 'app_topstories'})
    children = topstories.find_all(['a', 'img', 'div'])
    yield from process_tags(children, Location.TOP_STORY)


@coroutine
def parse_columns(soup):
    article_columns = soup \
        .find('div', {'id': 'app_col1'}) \
        .find('table') \
        .find_all('td', {'width': '33%'})
    assert len(article_columns) == 3

    @coroutine
    def parse_column(column):
        tags = column.find_all(['a', 'img', 'hr'])
        for article, image in process_tags(tags, Location.COLUMN):
            if article.title in ('AP TOP', 'WABC RADIO...', 'AGENCE FRANCE-PRESSE'):
                break
            yield article, image

    for col in article_columns:
        yield from parse_column(col)


if __name__ == '__main__':
    for article, image in scrape_site():
        print(article, image, end='\n\n\n')

