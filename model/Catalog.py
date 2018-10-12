from model.Item import Item, Book, Magazine, Movie, Music
from model.Form import RegisterForm, BookForm, MagazineForm, MovieForm, MusicForm

class Catalog:

    def __init__(self):
        self.item_catalog = []

    def getItemById(self, id):
        intId = id
        if id is not int:
            intId = int(id)

        for item in self.item_catalog:
            if item.id == intId:
                return item
        return None

    def getFormForItemType(self, type, form):
        if type == 'bb':
            return BookForm(form)
        elif type == 'ma':
            return MagazineForm(form)
        elif type == 'mo':
            return MovieForm(form)
        elif type == "mu":
            return MusicForm(form)
        else:
            return None

    def getFormData(self, itemSelected, request):
        seletedItemType = itemSelected.prefix
        form = None
        if seletedItemType == 'bb':
            form = BookForm(request.form)
            form.title.data = itemSelected.title
            form.author.data = itemSelected.author
            form.format.data = itemSelected.format
            form.pages.data = itemSelected.pages
            form.publisher.data = itemSelected.publisher
            form.language.data = itemSelected.language
            form.isbn10.data = itemSelected.isbn10
            form.isbn13.data = itemSelected.isbn13

        elif seletedItemType == 'ma':
            form = MagazineForm(request.form)
            form.title.data = itemSelected.title
            form.publisher.data = itemSelected.publisher
            form.language.data = itemSelected.language
            form.isbn10.data = itemSelected.isbn10
            form.isbn13.data = itemSelected.isbn13

        elif seletedItemType == 'mo':
            form = MovieForm(request.form)
            form.title.data = itemSelected.title
            form.director.data = itemSelected.director
            form.producers.data = itemSelected.producers
            form.actors.data = itemSelected.actors
            form.language.data = itemSelected.language
            form.subtitles.data = itemSelected.subs
            form.dubbed.data = itemSelected.dubbed
            form.releaseDate.data = itemSelected.release_date
            form.runtime.data = itemSelected.runtime

        elif seletedItemType == 'mu':
            form = MusicForm(request.form)
            form.title.data = itemSelected.title
            form.media_type.data = itemSelected.media_type
            form.artist.data = itemSelected.artist
            form.label.data = itemSelected.label
            form.releaseDate.data = itemSelected.release_date
            form.asin.data = itemSelected.asin

        return form

    def get_all_items(self):
        pass
    
    def add_item(self, type, form):
        if type == "Book":
            title = form.title.data
            prefix = "bb"
            status = "avail"
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
            status = "avail"
            director = form.director.data
            producers = form.producers.data
            actors = form.actors.data
            language = form.language.data
            subtitles = form.subtitles.data
            dubbed = form.dubbed.data
            releaseDate = form.releaseDate.data
            runTime = form.runtime.data
            movie = Movie(title,prefix,7, status, director, producers, actors, language, subtitles, dubbed, releaseDate, runTime)
            self.item_catalog.append(movie)
        elif type == "Music":
            media_type = form.media_type.data
            title = form.title.data
            prefix = "mu"
            status = "avail"
            artist = form.artist.data
            label = form.label.data
            releaseDate = form.releaseDate.data
            asin = form.asin.data
            music = Music(title, prefix, 8, status, media_type, artist, label, releaseDate, asin)
            self.item_catalog.append(music)

    def edit_item(self, id, form):
        item = self.getItemById(id)
        if item is None:
            return None

        selectedItemPrefix = item.prefix

        if selectedItemPrefix == "bb":
            item.title = form.title.data
            item.author = form.author.data
            item.format = form.format.data
            item.pages = form.pages.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data
        elif selectedItemPrefix == "ma":
            item.title = form.title.data
            item.publisher = form.publisher.data
            item.language = form.language.data
            item.isbn10 = form.isbn10.data
            item.isbn13 = form.isbn13.data
        elif selectedItemPrefix == "mo":
            item.title = form.title.data
            item.director = form.director.data
            item.producers = form.producers.data
            item.actors = form.actors.data
            item.language = form.language.data
            item.subs = form.subtitles.data
            item.dubbed = form.dubbed.data
            item.release_date = form.releaseDate.data
            item.runtime = form.runtime.data
        elif selectedItemPrefix == "mu":
            item.title = form.title.data
            item.media_type = form.media_type.data
            item.artist = form.artist.data
            item.label = form.label.data
            item.release_date = form.releaseDate.data
            item.asin = form.asin.data

    def delete_item(self, id):
        item = self.getItemById(id)
        if item is not None:
            self.item_catalog.remove(item)
            return True
        else:
            return False
