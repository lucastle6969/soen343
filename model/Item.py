class Item:
    def __init__(self, item_id, title, prefix, quantity, copies):
        self.title = title
        self.prefix = prefix
        self.id = item_id
        self.quantity = quantity
        self.copies = copies

    def add_temp_copies(self, amount):
        while amount < 0:
            self.copies.append(PhysicalItem(None, self.prefix, self.id))
            amount = amount - 1
            quantity = quantity + 1

    def remove_physical_item(self, removed_physical_ids):
        for physical_id in removed_physical_ids:
            for copy in copies:
                if physical_id == copy.id:
                    copies.remove(copy)
                    quantity = quantity - 1
                    break


class PhysicalItem:
    def __init__(self, id, prefix, item_fk):
        self.id = id
        self.prefix = prefix
        self.item_fk = item_fk

    def __eq__(self, other):
        return self.id == other.id and self.prefix == other.prefix

    def __hash__(self):
        return hash(('id', self.id, "prefix", self.prefix))


class Book(Item):
    def __init__(self, item_id, title, prefix, author, item_format, pages, publisher, publication_year, language, isbn10, isbn13, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity, copies)
        self.author = author
        self.format = item_format
        self.pages = pages
        self.publisher = publisher
        self.publication_year = publication_year
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13


class PhysicalBook(PhysicalItem):
    def __init__(self, id, item_fk, status, return_date, user_fk=None):
        PhysicalItem.__init__(self, id, "bb", item_fk)
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk


class Magazine(Item):
    def __init__(self, item_id, title, prefix, publisher, publication_date, language, isbn10, isbn13, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity, copies)
        self.publisher = publisher
        self.publication_date = publication_date
        self.language = language
        self.isbn10 = isbn10
        self.isbn13 = isbn13


class PhysicalMagazine(PhysicalItem):
    def __init__(self, id, item_fk, status):
        PhysicalItem.__init__(self, id, "ma", item_fk)
        self.status = status


class Movie(Item):
    def __init__(self, item_id, title, prefix, director, producers, actors, language, subtitles, dubbed,
                 release_date, runtime, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity, copies)
        self.director = director
        self.producers = producers
        self.actors = actors
        self.language = language
        self.subtitles = subtitles
        self.dubbed = dubbed
        self.release_date = release_date
        self.runtime = runtime


class PhysicalMovie(PhysicalItem):
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "mo", item_fk)
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk


class Music(Item):
    def __init__(self, item_id, title, prefix, media_type, artist, label, release_date, asin, quantity, copies):
        Item.__init__(self, item_id, title, prefix, quantity, copies)
        self.media_type = media_type
        self.artist = artist
        self.label = label
        self.release_date = release_date
        self.asin = asin


class PhysicalMusic(PhysicalItem):
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "mu", item_fk)
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk

