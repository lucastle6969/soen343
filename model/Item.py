class Item:
    def __init__(self, item_id, title, prefix, quantity):
        self.title = title
        self.prefix = prefix
        self.id = item_id
        self.quantity = quantity


class Book(Item):
    def __init__(self, item_id, title, prefix, author, item_format, pages, publisher, publication_year, language, isbn10, isbn13, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity)
        self.author = author
        self.format = item_format
        self.pages = pages
        self.publisher = publisher
        self.publication_year = publication_year
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.copies = copies


class PhysicalBook:
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        self.id = id
        self.item_fk = item_fk
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk
        self.prefix = "bb"


class Magazine(Item):
    def __init__(self, item_id, title, prefix, publisher, publication_date, language, isbn10, isbn13, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity)
        self.publisher = publisher
        self.publication_date = publication_date
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.copies = copies


class PhysicalMagazine:
    def __init__(self, id, item_fk, status):
        self.id = id
        self.item_fk = item_fk
        self.status = status
        self.prefix = "ma"


class Movie(Item):
    def __init__(self, item_id, title, prefix, director, producers, actors, language, subtitles, dubbed,
                 release_date, runtime, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity)
        self.director = director
        self.producers = producers
        self.actors = actors
        self.language = language
        self.subtitles = subtitles
        self.dubbed = dubbed
        self.release_date = release_date
        self.runtime = runtime
        self.copies = copies


class PhysicalMovie:
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        self.id = id
        self.item_fk = item_fk
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk
        self.prefix = "mo"


class Music(Item):
    def __init__(self, item_id, title, prefix, media_type, artist, label, release_date, asin, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity)
        self.media_type = media_type
        self.artist = artist
        self.label = label
        self.release_date = release_date
        self.asin = asin
        self.copies = copies


class PhysicalMusic:
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        self.id = id
        self.item_fk = item_fk
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk
        self.prefix = "mu"

