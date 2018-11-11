from model.Item import Book, PhysicalBook, Magazine, PhysicalMagazine, Movie, PhysicalMovie, Music, PhysicalMusic
from model.Uow import Uow
from model.Catalog import Catalog
from model.Tdg import Tdg
from copy import deepcopy


class ItemMapper:
    def __init__(self, app):
        self.uow = None
        self.catalog = Catalog()
        self.tdg = Tdg(app)
        self.catalog.populate(self.get_all_books(), self.get_all_magazines(),
                              self.get_all_movies(), self.get_all_music())

    def get_catalog(self):
        return self.catalog

    def get_all_items(self, item_prefix):
        return self.catalog.get_all_items(item_prefix)

    def get_all_books(self):
        all_copies = []
        for copy in self.tdg.get_books_physical():
            all_copies.append(PhysicalBook(copy[0], copy[1], copy[2], copy[3]))
        book_list = []
        for book in self.tdg.get_books():
            copies = []
            for single_copy in all_copies:
                if single_copy.book_fk == book[0]:
                    copies.append(single_copy)
            book_list.append(Book(book[0], book[1], "bb", book[2], book[3], book[4], book[5], book[6], book[7], book[8], book[9], book[10], copies))
        return book_list

    def get_all_magazines(self):
        all_copies = []
        for copy in self.tdg.get_magazines_physical():
            all_copies.append(PhysicalMagazine(copy[0], copy[1], copy[2], copy[3]))
        magazine_list = []
        for magazine in self.tdg.get_magazines():
            copies = []
            for single_copy in all_copies:
                if single_copy.magazine_fk == magazine[0]:
                    copies.append(single_copy)
            magazine_list.append(Magazine(magazine[0], magazine[1], "ma", magazine[2], magazine[3], magazine[4], magazine[5], magazine[6], magazine[7], copies))
        return magazine_list

    def get_all_music(self):
        all_copies = []
        for copy in self.tdg.get_music_physical():
            all_copies.append(PhysicalMusic(copy[0], copy[1], copy[2], copy[3]))
        music_list = []
        for music in self.tdg.get_music():
            copies = []
            for single_copy in all_copies:
                if single_copy.music_fk == music[0]:
                    copies.append(single_copy)
            music_list.append(Music(music[0], music[1], "mu", music[2], music[3], music[4], music[5], music[6], music[7], copies))
        return music_list

    def get_all_movies(self):
        all_copies = []
        for copy in self.tdg.get_movies_physical():
            all_copies.append(PhysicalMovie(copy[0], copy[1], copy[2], copy[3]))
        movie_list = []
        for movie in self.tdg.get_movies():
            copies = []
            for single_copy in all_copies:
                if single_copy.movie_fk == movie[0]:
                    copies.append(single_copy)
            movie_list.append(Movie(movie[0], movie[1], "mo", movie[2], movie[3], movie[4], movie[5], movie[6], movie[7], movie[8], movie[9], movie[10], copies))
        return movie_list

    def get_all_isbn_items(self):
        all_isbn_items = self.get_all_books()
        all_magazines = self.get_all_magazines()
        for magazine in all_magazines:
            all_isbn_items.append(magazine)
        return all_isbn_items

    def get_saved_changes(self):
        if self.uow is None:
            return None
        else:
            return self.uow.get_saved_changes()

    def find(self, item_prefix, item_id):
        if self.uow is None:
            self.uow = Uow()
        item = self.uow.get(item_prefix, item_id)
        if item is not None:
            clone = deepcopy(item)
            return clone
        else:
            item = self.catalog.get_item_by_id(item_prefix, item_id)
            clone = deepcopy(item)
            self.uow.add(clone)
            return clone

    def delete_item(self, item_prefix, item_id):
        if self.uow is None:
            self.uow = Uow()
        item = self.uow.get(item_prefix, item_id)
        if item is None:
            item = self.catalog.get_item_by_id(item_prefix, item_id)
            clone = deepcopy(item)
            self.uow.add(clone)

        self.uow.register_deleted(item)
        return True

    def cancel_deletion(self, item_prefix, item_id):
        item_to_cancel = self.uow.get(item_prefix, item_id)
        self.uow.cancel_deletion(item_to_cancel)
        return True

    def set_item(self, item_prefix, item_id, form):
        item = self.uow.get(item_prefix, item_id)

        if item_prefix == "bb":
            item.title = form.title.data
            item.author = form.author.data
            item.format = form.format.data
            item.pages = form.pages.data
            item.publisher = form.publisher.data
            item.publication_year = form.publication_year.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data

        elif item_prefix == "ma":
            item.title = form.title.data
            item.publisher = form.publisher.data
            item.publication_date = form.publication_date.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data

        elif item_prefix == "mo":
            item.title = form.title.data
            item.director = form.director.data
            item.producers = form.producers.data
            item.actors = form.actors.data
            item.language = form.language.data
            item.subtitles = form.subtitles.data
            item.dubbed = form.dubbed.data
            item.release_date = form.release_date.data
            item.runtime = form.runtime.data

        elif item_prefix == "mu":
            item.title = form.title.data
            item.media_type = form.media_type.data
            item.artist = form.artist.data
            item.label = form.label.data
            item.release_date = form.release_date.data
            item.asin = form.asin.data

        self.uow.register_dirty(item)

    def add_book(self, form):
        title = form.title.data
        prefix = "bb"
        author = form.author.data
        book_format = form.format.data
        pages = form.pages.data
        publisher = form.publisher.data
        publication_year = form.publication_year.data
        language = form.language.data
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        quantity = int(form.quantity.data)
        book = Book(None, title, prefix, author, book_format, pages, publisher, publication_year, language, isbn10, isbn13, quantity, None)

        if self.uow is None:
            self.uow = Uow()
        self.uow.add(book)
        self.uow.register_new(book)
        return True

    def add_magazine(self, form):
        title = form.title.data
        prefix = "ma"
        publisher = form.publisher.data
        publication_date = form.publication_date.data
        language = form.language.data
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        quantity = int(form.quantity.data)
        magazine = Magazine(None, title, prefix, publisher, publication_date, language, isbn10, isbn13, quantity, None)

        if self.uow is None:
            self.uow = Uow()
        self.uow.add(magazine)
        self.uow.register_new(magazine)
        return True

    def add_movie(self, form):
        title = form.title.data
        prefix = "mo"
        director = form.director.data
        producers = form.producers.data
        actors = form.actors.data
        language = form.language.data
        subtitles = form.subtitles.data
        dubbed = form.dubbed.data
        release_date = form.release_date.data
        run_time = form.runtime.data
        quantity = int(form.quantity.data)
        movie = Movie(None, title, prefix, director, producers, actors,
                      language, subtitles, dubbed, release_date, run_time, quantity, None)
        if self.uow is None:
            self.uow = Uow()
        self.uow.add(movie)
        self.uow.register_new(movie)
        return True

    def add_music(self, form):
        media_type = form.media_type.data
        title = form.title.data
        prefix = "mu"
        artist = form.artist.data
        label = form.label.data
        release_date = form.release_date.data
        asin = form.asin.data
        quantity = int(form.quantity.data)
        music = Music(None, title, prefix, media_type, artist, label,
                      release_date, asin, quantity, None)
        if self.uow is None:
            self.uow = Uow()
        self.uow.add(music)
        self.uow.register_new(music)
        return True

    def end(self):
        items_to_commit = self.uow.get_saved_changes()
        self.uow = None

        modified_books = []
        modified_magazines = []
        modified_movies = []
        modified_music = []

        deleted_books = []
        deleted_magazines = []
        deleted_movies = []
        deleted_music = []

        # Add
        if items_to_commit[0] is not None:
            for item in items_to_commit[0]:
                if item.prefix == "bb":
                    item.id = self.tdg.add_book(item)
                    keys = self.tdg.get_physical_keys(item.id, item.prefix)
                    physical_copies = []
                    for key in keys:
                        physical_copies.append(PhysicalBook(key, item.id, "Available", None))
                    item.copies = physical_copies[:]
                    self.catalog.add_item(item)
                elif item.prefix == "ma":
                    item.id = self.tdg.add_magazine(item)
                    keys = self.tdg.get_physical_keys(item.id, item.prefix)
                    physical_copies = []
                    for key in keys:
                        physical_copies.append(PhysicalMagazine(key, item.id, "Available", None))
                    item.copies = physical_copies[:]
                    self.catalog.add_item(item)
                elif item.prefix == "mo":
                    item.id = self.tdg.add_movie(item)
                    keys = self.tdg.get_physical_keys(item.id, item.prefix)
                    physical_copies = []
                    for key in keys:
                        physical_copies.append(PhysicalMovie(key, item.id, "Available", None))
                    item.copies = physical_copies[:]
                    self.catalog.add_item(item)
                elif item.prefix == "mu":
                    item.id = self.tdg.add_music(item)
                    keys = self.tdg.get_physical_keys(item.id, item.prefix)
                    physical_copies = []
                    for key in keys:
                        physical_copies.append(PhysicalMusic(key, item.id, "Available", None))
                    item.copies = physical_copies[:]
                    self.catalog.add_item(item)

        # Modify
        if items_to_commit[1] is not None:
            for item in items_to_commit[1]:
                if item.prefix == "bb":
                    modified_books.append(item)
                elif item.prefix == "ma":
                    modified_magazines.append(item)
                elif item.prefix == "mo":
                    modified_movies.append(item)
                elif item.prefix == "mu":
                    modified_music.append(item)
            self.catalog.edit_items(items_to_commit[1])
            if len(modified_books) != 0:
                self.tdg.modify_books(modified_books)
            if len(modified_magazines) != 0:
                self.tdg.modify_magazines(modified_magazines)
            if len(modified_movies) != 0:
                self.tdg.modify_movies(modified_movies)
            if len(modified_music) != 0:
                self.tdg.modify_music(modified_music)

        # Delete
        if items_to_commit[2] is not None:
            for item in items_to_commit[2]:
                if item.prefix == "bb":
                    deleted_books.append(item)
                elif item.prefix == "ma":
                    deleted_magazines.append(item)
                elif item.prefix == "mo":
                    deleted_movies.append(item)
                elif item.prefix == "mu":
                    deleted_music.append(item)
            self.catalog.delete_items(items_to_commit[2])
            if len(deleted_books) != 0:
                self.tdg.delete_books(deleted_books)
            if len(deleted_magazines) != 0:
                self.tdg.delete_magazines(deleted_magazines)
            if len(deleted_movies) != 0:
                self.tdg.delete_movies(deleted_movies)
            if len(deleted_music) != 0:
                self.tdg.delete_music(deleted_music)

    def get_filtered_items(self, prefix, form):
        filter_value = form.filter.data
        search_value = form.search.data
        order_filter = form.order_filter.data
        order_type = form.order_type.data

        filtered_items = self.catalog.get_filtered_items(prefix, filter_value, search_value, order_filter, order_type)
        return filtered_items

