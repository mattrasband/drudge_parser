import os

from bs4 import BeautifulSoup
import pytest

import drudge_parser


static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


def image_count(stories):
    return sum([1 for _, i in stories if i])


@pytest.mark.parametrize('filename, article_ct, image_ct, parser_fn', (
    (os.path.join(static_dir, 'page01.html'), 13, 0, drudge_parser.parse_top_stories),
    (os.path.join(static_dir, 'page01.html'), 1, 0, drudge_parser.parse_main_headlines),
    (os.path.join(static_dir, 'page01.html'), 53, 8, drudge_parser.parse_columns),
))
def test_parsing(filename, article_ct, image_ct, parser_fn):
    """Quick and dirty test to at least check the quantity
    of expected articles/images in a given static page.
    """
    with open(filename) as f:
        soup = BeautifulSoup(f, 'html5lib')
        articles = list(parser_fn(soup))
        assert len(articles) == article_ct
        assert image_count(articles) == image_ct

