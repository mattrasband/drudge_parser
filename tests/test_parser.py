import os

import pytest

import drudge_parser


static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


@pytest.mark.parametrize('filename, top_count, main_count, col1_count, col2_count, col3_count', (
    (os.path.join(static_dir, 'page01.html'), 13, 1, 12, 30, 11),
    (os.path.join(static_dir, 'page_2016_06_01.html'), 6, 1, 13, 19, 14),
))
def test_parse(filename, top_count, main_count, col1_count, col2_count,
               col3_count):
    parser = drudge_parser.DrudgeParser()
    with open(filename) as f:
        parser.feed(f.read())

    counter = {
        drudge_parser.Location.TOP_STORY: 0,
        drudge_parser.Location.MAIN_HEADLINE: 0,
        drudge_parser.Location.COLUMN1: 0,
        drudge_parser.Location.COLUMN2: 0,
        drudge_parser.Location.COLUMN3: 0,
    }

    for a in parser.articles:
        counter[a['location']] += len(a['articles'])

    assert top_count == counter[drudge_parser.Location.TOP_STORY]
    assert main_count == counter[drudge_parser.Location.MAIN_HEADLINE]
    assert col1_count == counter[drudge_parser.Location.COLUMN1]
    assert col2_count == counter[drudge_parser.Location.COLUMN2]
    assert col3_count == counter[drudge_parser.Location.COLUMN3]

