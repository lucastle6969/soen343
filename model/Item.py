class Item:
    def __init__(self, item_id, title, prefix, quantity):
        self.title = title
        self.prefix = prefix
        self.id = item_id
        self.quantity = quantity

    def add_temp_copies(self, amount, prefix):
        for x in range(0, amount):
            if prefix == "bb":
                self.copies.append(PhysicalBook(None, self.id, "Available", None))
                self.quantity = self.quantity + 1

            if prefix == "ma":
                self.copies.append(PhysicalMagazine(None, self.id, None))
                self.quantity = self.quantity + 1

            if prefix == "mo":
                self.copies.append(PhysicalMovie(None, self.id, "Available", None))
                self.quantity = self.quantity + 1

            if prefix == "mu":
                self.copies.append(PhysicalMusic(None, self.id, "Available", None))
                self.quantity = self.quantity + 1

    def remove_physical_item(self, removed_physical_ids):
        for physical_id in removed_physical_ids:
            for copy in self.copies:
                print("===============================================================")
                print(physical_id)
                if physical_id is not None:
                    if int(physical_id) == copy.id:
                        self.copies.remove(copy)
                        self.quantity = self.quantity - 1
                        break
                if physical_id is None:
                    self.copies.remove(copy)
                    self.quantity = self.quantity - 1
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
    def __init__(self, id, item_fk, status, return_date, user_fk=None):
        PhysicalItem.__init__(self, id, "bb", item_fk)
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
    def __init__(self, id, item_fk, status):
        PhysicalItem.__init__(self, id, "ma", item_fk)
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
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "mo", item_fk)
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
    def __init__(self, id, item_fk, status, return_date, user_fk = None):
        PhysicalItem.__init__(self, id, "mu", item_fk)
        self.status = status
        self.return_date = return_date
        self.user_fk = user_fk

