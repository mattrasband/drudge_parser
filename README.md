A pretty simple parser for [Drudge Report](http://drudgereport.com). I find the site impossible to look at and wanted a way to more easily digest the information, as I like to keep tabs on lots of differing news outlets.


## Installation

PyPI

    pip install drudge_parser


## Usage

    import drudge_parser

    # scrape_site is a generator of (Article, Image)
    articles = drudge_parser.scrape_site()

    for article, image in articles:
        # image may be None, if none was found that is considered as
        # related to the article. In many cases, the same image will
        # be yielded for multiple articles.
        print(article, image)
