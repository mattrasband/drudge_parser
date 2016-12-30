#!/usr/bin/env python

import contextlib
try:
    from html.parser import HTMLParser
    from urllib.request import urlopen
except ImportError:
    from HTMLParser import HTMLParser  # noqa
    from urllib2 import urlopen  # noqa


class Location:
    """Location constants for locations on the page,
    not using an Enum to maintain backwards compat with
    the stdlib.
    """
    TOP_STORY = 'TOP_STORY'
    MAIN_HEADLINE = 'MAIN_HEADLINE'
    COLUMN1 = 'COLUMN1'
    COLUMN2 = 'COLUMN2'
    COLUMN3 = 'COLUMN3'


class DrudgeParser(HTMLParser):
    """DrudgeParser parses the Drudge Report (http://drudgereport.com)
    parsing out related articles, their multimedia content, and groups
    them according to the location on the page (see the Location enumeration)

    Call feed(str) on an instance and get the results from the `articles`
    property.

    The articles property will be an ordered list of grouped elements on the
    page, beginning with the Top Stories (TOP_STORY), Main Headline
    (MAIN_HEADLINE), and then Columns 1-3 (COLUMN#).

    The grouped element is simply a dictionary:

    {
        "images": [str],  # This often is just empty, never None
        "articles": [
            {
                "title": str,
                "href": str
            }
        ],
        "location": str  # One of the Location 'enumeration'
    }

    Groups are determined by one of the following factors:

        1. The parser moved from one div#id to another (e.g. app_topstories ->
           app_mainheadline or app_mainheadline -> app_col#)
        2. An <hr> element was encountered

    In all cases to date, the articles appear to be related by these groupings.

    Anything that is not a link isn't considered an article (rarely drudge will
    post a quick summary, these are missed). They aren't always super valuable,
    however. If they become so, please provide a copy of the source of the page
    at that moment in time.
    """
    # partial src links that should be ignored for
    # whatever reason.
    SRC_BLACKLIST = [
        'adserver.adtechus',
        'widget.quantcast.com',
        'pixel.quantserve.com',
        'http://www.drudgereport.com/i/logo9.gif',
    ]

    # these are entire href matches that trigger
    # a state of "skipping" the links/data until
    # triggered back out. From a standard 0 index,
    # the evens are the ENTER condition (start skipping)
    # and the odds are the EXIT condition (stop skipping)
    HREF_BLACKLIST_SWITCH = [
        # COL 1
        'http://www.thepaperboy.com/uk/front-pages.cfm',
        'http://www.zerohedge.com/',
        # COL 2
        'http://www.mirror.co.uk/3am/',
        'http://www.suntimes.com/entertainment/zwecker/index.html',
        # COL 3
        'http://www.france24.com/en/timeline/global/',
        'http://www.intermarkets.net/privacypolicy.html',
    ]

    # these are partial matches that are just to be ignored
    # for the one iteration, but otherwise have no longlasting
    # meaning.
    HREF_BLACKLIST = [
        'adserver.adtechus.com',
        'www.quantcast.com',
        'http://www.drudgereport.com/',
    ]

    def __init__(self):
        HTMLParser.__init__(self)
        self.location = None
        self.want = False
        self.skip = False

        self.articles = []
        self.last = {
            'images': [],
            'articles': [],
            'location': None,
        }

        self.column_num = 1

    def handle_starttag(self, tag, attrs):
        if tag in ('img', 'iframe'):
            # This is going to be media content, usually images and
            # sometimes embedded youtube clips.
            src = self._find_attr_value(attrs, 'src')
            if src and not any(x in src for x in self.SRC_BLACKLIST):
                self.last['images'].append(src)
        elif tag == 'a':
            href = self._find_attr_value(attrs, 'href')
            if href:
                if any(x == href for x in self.HREF_BLACKLIST_SWITCH):
                    # The static links in each of the columns triggers us to
                    # move into a state in which we skip everything until we
                    # see the end of the column, resetting us to care.
                    self.skip = not self.skip
                    if self.skip:
                        self.column_num += 1
                        if self.column_num == 2:
                            self.location = Location.COLUMN2
                        else:
                            self.location = Location.COLUMN3
                elif not (self.skip or any(x in href for x in self.HREF_BLACKLIST)):
                    # We found an article and want to grab it.
                    self.want = True
                    self.last['location'] = self.location
                    self.last['articles'].append({
                        'href': href.strip(),
                        'title': '',
                    })
        elif tag == 'div':
            if ('id', 'app_topstories') in attrs:
                self.location = Location.TOP_STORY
                self._reset_last()
            elif ('id', 'app_mainheadline') in attrs:
                self.location = Location.MAIN_HEADLINE
                self._reset_last()
            elif ('id', 'app_col1') in attrs:
                self.location = Location.COLUMN1
                self._reset_last()
        elif tag == 'hr':
            # We have crossed into a new section, snap off the related
            # articles/images
            self._reset_last()

    def handle_endtag(self, tag):
        self.want = False

    def handle_data(self, data):
        if self.want:
            title = self.last['articles'][-1]['title']
            if len(title) > 0:
                title += ' '
            title += data.strip()
            self.last['articles'][-1]['title'] = title

    def _reset_last(self):
        if self.last['images'] or self.last['articles']:
            self.articles.append(self.last)
        self.last = {'images': [], 'articles': [], 'location': None}

    def _find_attr_value(self, attrs, target_attr):
        """Find an attribute value by the name. None will be
        returned if the value was not found.
        :param attrs: The list of (name, value) tuples (usually from
                      handle_starttag
        :param target_attr: The attribute name to find (e.g. 'id' for
                            the html ID)
        """
        for name, value in attrs:
            if name == target_attr and value:
                return value
        return None


def scrape_page():
    with contextlib.closing(urlopen('http://drudgereport.com')) as page:  # py2 compat
        assert page.getcode() == 200, \
            'Bad response from the page, try again later.'
        p = DrudgeParser()
        source = page.read()
        if isinstance(source, bytes):  # py3 compat
            source = source.decode()
        p.feed(source)
        return p.articles


if __name__ == '__main__':
    import json
    print(json.dumps(scrape_page(), indent=4))
