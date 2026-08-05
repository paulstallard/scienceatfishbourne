import sys


class Author:
    def __init__(self, name, affiliation=None):
        self.name = name
        self.affiliation = affiliation


class Talk:
    def __init__(
        self,
        date,
        author,
        *,
        title,
        subtitle=None,
        overview=None,
        categories="",
        headline="",
        attachments=None,
        review=True,
        review_text=None,
    ):
        if len(date) != 10:
            sys.exit("Talk date must be of form 'YYYY-MM-DD'")
        self.date = date
        self.shortdate = date[:-3]
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.overview = overview
        self.categories = categories
        self.headline = headline
        self.attachments = attachments
        self.review = review
        self.review_text = review_text
