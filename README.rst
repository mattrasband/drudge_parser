.. image:: https://travis-ci.org/mrasband/drudge_parser.svg?branch=master

A pretty simple parser for `Drudge Report <http://drudgereport.com>`_. I find the site impossible to look at and wanted a way to more easily digest the information, as I like to keep tabs on lots of differing news outlets.

This library has no external dependencies and supports Python 2.7+ (targeted for Python 3+)

Installation
============

PyPI

    pip install drudge_parser


Usage
=====

Example::

    import drudge_parser

    # You can use and feed the parser directly if you would like:
    parser = drudge_parser.DrudgeParser()
    parser.feed('<html string>')
    print(parser.articles)

    # Or just use the helper to scrape the current site:
    articles = drudge_parser.scrape_page()
    print(articles)

Articles is a list of article groupings. These are ordered down the page, so they will always be ``TOP_STORY``, ``MAIN_HEADLINE``, followed by ``COLUMN{1,3}``.

An article grouping looks like::

    {
        "images": [str],  # This often is just empty, never None
        "articles": [
            #  These will be ordered by appearance, in some cases drudge
            #  builds related titles on each other to make one link across
            #  multiple lines.
            {
                "title": str,
                "href": str
            }
        ],  # Never None
        "location": str  # One of the drudge_parser.Location 'enumeration'
    }

Additional Contributors
=======================

* [jamesjackson69](https://github.com/jamesjackson69)
