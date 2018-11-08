from model.Item import Book, Magazine, Movie, Music


class Catalog:

    def __init__(self):
        self.item_catalog = []

    def get_item_by_id(self, item_prefix, item_id):
        int_id = int(item_id)

        for item in self.item_catalog:
            if item.id == int_id and item.prefix == item_prefix:
                return item
        return None

    def populate(self, books, magazines, movies, music):

        if books is not None:
            for book in books:
                self.item_catalog.append(Book(book[0], book[1], "bb", book[2], book[3], book[4], book[5], book[6], book[7], book[8], book[9], book[10]))
        if magazines is not None:
            for magazine in magazines:
                self.item_catalog.append(Magazine(magazine[0], magazine[1], "ma", magazine[2], magazine[3], magazine[4], magazine[5], magazine[6], magazine[7]))

        if movies is not None:
            for movie in movies:
                self.item_catalog.append(Movie(movie[0], movie[1], "mo", movie[2], movie[3], movie[4], movie[5], movie[6], movie[7], movie[8], movie[9], movie[10]))

        if music is not None:
            for item in music:
                self.item_catalog.append(Music(item[0], item[1], "mu", item[2], item[3], item[4], item[5], item[6], item[7]))

    # [Testing] Used to remove objects added to catalog while testing
    def delete_last_item(self):
        if len(self.item_catalog) == 0:
            return None
        self.item_catalog = self.item_catalog[:-1]

    def add_item(self, item):
        if item is not None:
            self.item_catalog.append(item)

    def edit_items(self, items):
        for mod_item in items:
            item = self.get_item_by_id(mod_item.prefix, mod_item.id)
            if item is None:
                pass

            if mod_item.prefix == "bb":
                item.title = mod_item.title
                item.author = mod_item.author
                item.format = mod_item.format
                item.pages = mod_item.pages
                item.publisher = mod_item.publisher
                item.publication_year = mod_item.publication_year
                item.language = mod_item.language
                item.isbn10 = mod_item.isbn10
                item.isbn13 = mod_item.isbn13

            elif mod_item.prefix == "ma":
                item.title = mod_item.title
                item.publisher = mod_item.publisher
                item.publication_date = mod_item.publication_date
                item.language = mod_item.language
                item.isbn10 = mod_item.isbn10
                item.isbn13 = mod_item.isbn13

            elif mod_item.prefix == "mo":
                item.title = mod_item.title
                item.director = mod_item.director
                item.producers = mod_item.producers
                item.actors = mod_item.actors
                item.language = mod_item.language
                item.subtitles = mod_item.subtitles
                item.dubbed = mod_item.dubbed
                item.release_date = mod_item.release_date
                item.runtime = mod_item.runtime

            elif mod_item.prefix == "mu":
                item.title = mod_item.title
                item.media_type = mod_item.media_type
                item.artist = mod_item.artist
                item.label = mod_item.label
                item.release_date = mod_item.release_date
                item.asin = mod_item.asin
        return True

    def delete_items(self, items):
        for del_item in items:
            item = self.get_item_by_id(del_item.prefix, del_item.id)
            if item is not None:
                self.item_catalog.remove(item)
        return True
