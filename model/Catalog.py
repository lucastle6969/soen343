from model.Item import Book, Magazine, Movie, Music


class Catalog:

    def __init__(self):
        self.item_catalog = []

    def get_item_by_id(self, item_id):
        int_id = item_id
        if item_id is not int:
            int_id = int(item_id)

        for item in self.item_catalog:
            if item.id == int_id:
                return item
        return None

    def get_all_items(self):
        pass

    # [Testing] This function is required for testing add/remove/edit
    def insert_item(self, item):
        if item is None:
            return False

        self.item_catalog.append(item)
        return True

    def add_item(self, item_type, form):
        if item_type == "Book":
            title = form.title.data
            prefix = "bb"
            status = "avail"
            author = form.author.data
            book_format = form.format.data
            pages = form.pages.data
            publisher = form.publisher.data
            language = form.language.data
            isbn10 = form.isbn10.data
            isbn13 = form.isbn13.data
            book = Book(title, prefix, 5, status, author, book_format, pages, publisher, language, isbn10, isbn13)
            self.insert_item(book)
            return True
        elif item_type == "Magazine":
            title = form.title.data
            publisher = form.publisher.data
            prefix = "ma"
            status = "avail"
            language = form.language.data
            isbn10 = form.isbn10.data
            isbn13 = form.isbn13.data
            magazine = Magazine(title, prefix, 6, status, publisher, language, isbn10, isbn13)
            self.insert_item(magazine)
            return True
        elif item_type == "Movie":
            title = form.title.data
            prefix = "mo"
            status = "avail"
            director = form.director.data
            producers = form.producers.data
            actors = form.actors.data
            language = form.language.data
            subtitles = form.subtitles.data
            dubbed = form.dubbed.data
            release_date = form.releaseDate.data
            run_time = form.runtime.data
            movie = Movie(title, prefix, 7, status, director, producers, actors, language, subtitles, dubbed,
                          release_date, run_time)
            self.insert_item(movie)
            return True
        elif item_type == "Music":
            media_type = form.media_type.data
            title = form.title.data
            prefix = "mu"
            status = "avail"
            artist = form.artist.data
            label = form.label.data
            release_date = form.releaseDate.data
            asin = form.asin.data
            music = Music(title, prefix, 8, status, media_type, artist, label, release_date, asin)
            self.insert_item(music)
            return True
        return False

    def edit_item(self, item_id, form):
        item = self.get_item_by_id(item_id)
        if item is None:
            return None

        selected_item_prefix = item.prefix

        if selected_item_prefix == "bb":
            item.title = form.title.data
            item.author = form.author.data
            item.format = form.format.data
            item.pages = form.pages.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data
        elif selected_item_prefix == "ma":
            item.title = form.title.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data
        elif selected_item_prefix == "mo":
            item.title = form.title.data
            item.director = form.director.data
            item.producers = form.producers.data
            item.actors = form.actors.data
            item.language = form.language.data
            item.subs = form.subtitles.data
            item.dubbed = form.dubbed.data
            item.release_date = form.releaseDate.data
            item.runtime = form.runtime.data
        elif selected_item_prefix == "mu":
            item.title = form.title.data
            item.media_type = form.media_type.data
            item.artist = form.artist.data
            item.label = form.label.data
            item.release_date = form.releaseDate.data
            item.asin = form.asin.data

    def delete_item(self, item_id):
        item = self.get_item_by_id(item_id)
        if item is not None:
            self.item_catalog.remove(item)
            return True
        else:
            return False

    # [Testing] Used to remove objects added to catalog while testing
    def delete_last_item(self):
        if len(self.item_catalog) == 0:
            return None
        self.item_catalog = self.item_catalog[:-1]