class Item:
    def __init__(self, item_id, title, prefix, status):
        self.title = title
        self.prefix = prefix
        self.id = item_id
        self.status = status


class Book(Item):
    def __init__(self, item_id, title, prefix, status, author, item_format, pages, publisher, language, isbn10, isbn13):
        Item.__init__(self, item_id, title, prefix, status)
        self.author = author
        self.format = item_format
        self.pages = pages
        self.publisher = publisher
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13


class Magazine(Item):
    def __init__(self, item_id, title, prefix, status, publisher, language, isbn10, isbn13):
        Item.__init__(self, item_id, title, prefix, status)
        self.publisher = publisher
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13


class Movie(Item):
    def __init__(self, item_id, title, prefix, status, director, producers, actors, language, subtitles, dubbed,
                 release_date, runtime):
        Item.__init__(self, item_id, title, prefix, status)
        self.director = director
        self.producers = producers
        self.actors = actors
        self.language = language
        self.subtitles = subtitles
        self.dubbed = dubbed
        self.release_date = release_date
        self.runtime = runtime


class Music(Item):
    def __init__(self, item_id, title, prefix, status, media_type, artist, label, release_date, asin):
        Item.__init__(self, item_id, title, prefix, status)
        self.media_type = media_type
        self.artist = artist
        self.label = label
        self.release_date = release_date
        self.asin = asin
