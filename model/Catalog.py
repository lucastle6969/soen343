from operator import attrgetter


class Catalog:

    def __init__(self):
        self.item_catalog = []

    def get_all_items(self, item_type):
        item_list = []
        for item in self.item_catalog:
            if item.prefix == item_type:
                item_list.append(item)
        return item_list

    def get_item_by_id(self, item_prefix, item_id):
        int_id = int(item_id)

        for item in self.item_catalog:
            if item.id == int_id and item.prefix == item_prefix:
                return item
        return None

    def get_filtered_items(self, prefix, filter_field, search_value):
        search_tokens = search_value.split(" ")
        filtered_items = []
        for item in self.item_catalog:
            if item.prefix != prefix:
                continue

            value = eval("item." + filter_field)
            for token in search_tokens:
                if token.lower() in str(value).lower():
                    if item not in filtered_items:
                        filtered_items.append(item)

        return filtered_items

    @staticmethod
    def order_items(item_list, order_filter, order_type):
        if order_type == "ASC":
            return sorted(item_list, key=attrgetter(order_filter))
        elif order_type == "DESC":
            return sorted(item_list, key=attrgetter(order_filter), reverse=True)
        elif order_type == "NONE":
            return item_list

    def populate(self, books, magazines, movies, music):
        if books is not None:
            for book in books:
                self.item_catalog.append(book)

        if magazines is not None:
            for magazine in magazines:
                self.item_catalog.append(magazine)

        if movies is not None:
            for movie in movies:
                self.item_catalog.append(movie)

        if music is not None:
            for item in music:
                self.item_catalog.append(item)

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

    def mark_as_returned(self, prefix, item_fk, physical_id):
        for item in self.item_catalog:
            if item.prefix is prefix and item.id is item_fk:
                for physical_item in item.copies:
                    if physical_item.id is physical_id:
                        physical_item.status = "Available"
                        physical_item.return_date = None
