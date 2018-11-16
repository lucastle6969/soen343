class Item:
    def __init__(self, item_id, title, prefix, quantity):
        self.title = title
        self.prefix = prefix
        self.id = item_id
        self.quantity = quantity


class PhysicalItem:
    def __init__(self, id, prefix):
        self.id = id
        self.prefix = prefix

    def __eq__(self, other):
        return self.id == other.id and self.prefix == other.prefix

    def __hash__(self):
        return hash(('id', self.id, "prefix", self.prefix))


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


class PhysicalBook(PhysicalItem):
    def __init__(self, id, book_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "bb")
        self.book_fk = book_fk
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk


class Magazine(Item):
    def __init__(self, item_id, title, prefix, publisher, publication_date, language, isbn10, isbn13, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity)
        self.publisher = publisher
        self.publication_date = publication_date
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.copies = copies


class PhysicalMagazine(PhysicalItem):
    def __init__(self, id, magazine_fk, status):
        PhysicalItem.__init__(self, id, "ma")
        self.magazine_fk = magazine_fk
        self.status = status


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


class PhysicalMovie(PhysicalItem):
    def __init__(self, id, movie_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "mo")
        self.movie_fk = movie_fk
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk


class Music(Item):
    def __init__(self, item_id, title, prefix, media_type, artist, label, release_date, asin, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity)
        self.media_type = media_type
        self.artist = artist
        self.label = label
        self.release_date = release_date
        self.asin = asin
        self.copies = copies


class PhysicalMusic(PhysicalItem):
    def __init__(self, id, music_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "mu")
        self.music_fk = music_fk
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk

