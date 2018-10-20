from model.Item import Book, Magazine, Movie, Music
from model.UoW import UoW
from model.Catalog import Catalog
from model.Tdg import Tdg


class Mapper:
    def __init__(self, app):
        if self.uow is None:
            self.uow = UoW()
            
        self.catalog = Catalog()
        self.tdg = Tdg(app)
        self.catalog.populate(tdg.getBooks(), tdg.getMagazines(), tdg.getMovies(), tdg.getMusic())

    def add_book(self, form):
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
        book = Book(title, prefix, None, status, author, book_format, pages, publisher, language, isbn10, isbn13)
        if self.uow is None:
            self.uow = UoW()
        self.uow.add(book)
        self.uow.registerNew(book)

    def add_magazine(self, form):
        title = form.title.data
        publisher = form.publisher.data
        prefix = "ma"
        status = "avail"
        language = form.language.data
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        magazine = Magazine(title, prefix, None, status, publisher, language, isbn10, isbn13)
        if self.uow is None:
            self.uow = UoW()
        self.uow.add(magazine)
        self.uow.registerNew(magazine)

    def add_movie(self, form):
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
        movie = Movie(title, prefix, None, status, director, producers, actors, language, subtitles, dubbed,
                        release_date, run_time)
        if self.uow is None:
            self.uow = UoW()
        self.uow.add(movie)
        self.uow.registerNew(movie)

    def add_music(self, form):
        media_type = form.media_type.data
        title = form.title.data
        prefix = "mu"
        status = "avail"
        artist = form.artist.data
        label = form.label.data
        release_date = form.releaseDate.data
        asin = form.asin.data
        music = Music(title, prefix, None, status, media_type, artist, label, release_date, asin)
        if self.uow is None:
            self.uow = UoW()
        self.uow.add(music)
        self.uow.registerNew(music)

    def end(self):
        items_to_commit = self.uow.commit()

        # Add
        if items_to_commit[0] is not None:
            for item in items_to_commit[0]:
                if item.prefix == "bb":
                    item_id = self.tdg.add_book(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                elif item.prefix == "ma":
                    item_id = self.tdg.add_magazine(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                elif item.prefix == "mo":
                    item_id = self.tdg.add_movie(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                elif item.prefix == "mu":
                    item_id = self.tdg.add_music(item)
                    item.id = item_id
                    self.catalog.add_item(item)
                    
        # Modify
        elif items_to_commit[1] is not None:
            for item in items_to_commit[0]:
                if item.prefix == "bb":
                    itemId = self.tdg.modify_book(item)
                    # How is this going to work? there is no form to send..
                    self.catalog.edit_item(itemId, form)
                elif item.prefix == "ma":
                    itemId = self.tdg.modify_magazine(item)
                    self.catalog.edit_item(itemId, form)
                elif item.prefix == "mo":
                    itemId = self.tdg.modify_movie(item)
                    self.catalog.edit_item(itemId, form)
                elif item.prefix == "mu":
                    itemId = self.tdg.modify_music(item)
                    self.catalog.edit_item(itemId, form)

        # Delete
        elif items_to_commit[2] is not None:
            for item in items_to_commit[0]:
                if item.prefix == "bb":
                    item_id = self.tdg.delete_book(item)
                    self.catalog.delete_item(item_id)
                elif item.prefix == "ma":
                    item_id = self.tdg.delete_magazine(item)
                    self.catalog.delete_item(item_id)
                elif item.prefix == "mo":
                    item_id = self.tdg.delete_movie(item)
                    self.catalog.delete_item(item_id)
                elif item.prefix == "mu":
                    item_id = self.tdg.delete_music(item)
                    self.catalog.delete_item(item_id)

        # self.catalog.update(itemsToCommit)
        # self.tdg.update(itemsToCommit)