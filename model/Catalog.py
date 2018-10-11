from model.Item import Item, Book, Magazine, Movie, Music

class Catalog:

    def __init__(self):
        self.item_catalog = []

    def getItemById(self, id):
        intId = int(id)
        for item in self.item_catalog:
            if item.id == intId:
                return item
        return None

    def get_all_items(self):
        pass
    
    def add_item(self, type, form):
        if type == "Book":
            title = form.title.data
            prefix = "bb"
            status = "new"
            author = form.author.data
            format = form.format.data
            pages = form.pages.data
            publisher = form.publisher.data
            language = form.language.data
            isbn10 = form.isbn10.data
            isbn13 = form.isbn13.data
            book = Book(title, prefix, 5, status, author, format, pages, publisher, language, isbn10, isbn13)
            self.item_catalog.append(book)
        elif type == "Magazine":
            title = form.title.data
            publisher = form.publisher.data
            prefix = "ma"
            status = "avail"
            language = form.language.data
            isbn10 = form.isbn10.data
            isbn13 = form.isbn13.data
            magazine = Magazine(title, prefix, 6, status, publisher, language, isbn10, isbn13)
            self.item_catalog.append(magazine)
        elif type == "Movie":
            title = form.title.data
            prefix = "mo"
            status = "watched"
            director = form.director.data
            producers = form.producers.data
            actors = form.actors.data
            language = form.language.data
            subtitles = form.subtitles.data
            dubbed = form.dubbed.data
            releaseDate = form.releaseDate.data
            runTime = form.runTime.data
            movie = Movie(title,prefix,7, status, director, producers, actors, language, subtitles, dubbed, releaseDate, runTime)
            self.item_catalog.append(movie)
        elif type == "Music":
            musicType = form.musicType.data
            title = form.title.data
            prefix = "mu"
            status = "loaned"
            artist = form.artist.data
            label = form.label.data
            releaseDate = form.releaseDate.data
            asin = form.asin.data
            music = Music(title, prefix, 8, status, musicType, artist, label, releaseDate, asin)
            self.item_catalog.append(music)

    def edit_item(self, item, id):
        itemToMod = self.getItemById(id)
        for fieldname, value in item.items():
            for x in dir(itemToMod):
                if fieldname == x:
                    setattr(itemToMod, fieldname, value)

    def delete_item(self):
        pass
