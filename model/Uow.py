from model.Item import Item


class Uow():
    def __init__(self):
        self.mapped_book_items = []  # Identity map
        self.mapped_magazine_items = []
        self.mapped_music_items = []
        self.mapped_movie_items = []

        self.created_items = []
        self.modified_items = []
        self.deleted_items = []

        self.temp_id_counter = 0

    def get(self, item_prefix, item_id):
        int_id = int(item_id)
        if item_prefix == "bb":
            for pair in self.mapped_book_items:
                if pair[0] == int_id:
                    return pair[1]

        elif item_prefix == "ma":
            for pair in self.mapped_magazine_items:
                if pair[0] == int_id:
                    return pair[1]

        elif item_prefix == "mo":
            for pair in self.mapped_movie_items:
                if pair[0] == int_id:
                    return pair[1]

        elif item_prefix == "mu":
            for pair in self.mapped_music_items:
                if pair[0] == int_id:
                    return pair[1]

        return None

    def add(self, i):
        if i.id is None:
            self.temp_id_counter -= 1
            i.id = self.temp_id_counter
        if i.prefix == "bb":
            self.mapped_book_items.append((int(i.id), i))
        elif i.prefix == "ma":
            self.mapped_magazine_items.append((int(i.id), i))
        elif i.prefix == "mu":
            self.mapped_music_items.append((int(i.id), i))
        elif i.prefix == "mo":
            self.mapped_movie_items.append((int(i.id), i))

    def register_new(self, i):
        self.created_items.append((i.prefix, int(i.id)))

    def register_dirty(self, i):
        # replace the item in the mapped_items
        if i.prefix == "bb":
            self.mapped_book_items[:] = [tup for tup in self.mapped_book_items if not int(i.id) == tup[0]]
            self.mapped_book_items.append((int(i.id), i))

        elif i.prefix == "ma":
            self.mapped_magazine_items[:] = [tup for tup in self.mapped_magazine_items if not int(i.id) == tup[0]]
            self.mapped_magazine_items.append((int(i.id), i))

        elif i.prefix == "mo":
            self.mapped_movie_items[:] = [tup for tup in self.mapped_movie_items if not int(i.id) == tup[0]]
            self.mapped_movie_items.append((int(i.id), i))

        elif i.prefix == "mu":
            self.mapped_music_items[:] = [tup for tup in self.mapped_music_items if not int(i.id) == tup[0]]
            self.mapped_music_items.append((int(i.id), i))

        # check if it was already registered
        item_found = False
        for item in self.created_items:
            if item[0] == i.prefix and item[1] == int(i.id):
                item_found = True
                break

        if not item_found:
            for item in self.modified_items:
                if item[0] == i.prefix and item[1] == int(i.id):
                    item_found = True
                    break

        if not item_found:
            self.modified_items.append((i.prefix, int(i.id)))

    def register_deleted(self, i):
        item_found = False
        for pair in self.deleted_items:
            if pair[0] == i.prefix and int(i.id) == pair[1]:
                item_found = True

        if not item_found:
            self.deleted_items.append((i.prefix, int(i.id)))

        self.created_items[:] = [tup for tup in self.created_items if not (int(i.id) == tup[1] and i.prefix == tup[0])]
        self.modified_items[:] = [tup for tup in self.modified_items if not (int(i.id) == tup[1] and i.prefix == tup[0])]

    def cancel_deletion(self, item_to_cancel):
        self.deleted_items[:] = [tup for tup in self.deleted_items if not (int(item_to_cancel.id) == tup[1] and item_to_cancel.prefix == tup[0])]

# Retrieve the lists of updates (create, modify, delete)
    def get_saved_changes(self):
        """Create lists of objects (unlike the similarly named
        instance variables, which contains lists of IDs)"""
        created_items = []
        modified_items = []
        deleted_items = []

        print("Get saved changes*********************************")
        for created_pair in self.created_items:
            if created_pair[0] == "bb":
                for mapped_pair in self.mapped_book_items:
                    if created_pair[1] == mapped_pair[0]:
                        created_items.append(mapped_pair[1])
            elif created_pair[0] == "ma":
                for mapped_pair in self.mapped_magazine_items:
                    if created_pair[1] == mapped_pair[0]:
                        created_items.append(mapped_pair[1])

            elif created_pair[0] == "mo":
                for mapped_pair in self.mapped_movie_items:
                    if created_pair[1] == mapped_pair[0]:
                        created_items.append(mapped_pair[1])

            elif created_pair[0] == "mu":
                for mapped_pair in self.mapped_music_items:
                    if created_pair[1] == mapped_pair[0]:
                        created_items.append(mapped_pair[1])

        for modified_pair in self.modified_items:
            if modified_pair[0] == "bb":
                for mapped_pair in self.mapped_book_items:
                    if modified_pair[1] == mapped_pair[0]:
                        modified_items.append(mapped_pair[1])

            elif modified_pair[0] == "ma":
                for mapped_pair in self.mapped_magazine_items:
                    if modified_pair[1] == mapped_pair[0]:
                        modified_items.append(mapped_pair[1])

            elif modified_pair[0] == "mo":
                for mapped_pair in self.mapped_movie_items:
                    if modified_pair[1] == mapped_pair[0]:
                        modified_items.append(mapped_pair[1])

            elif modified_pair[0] == "mu":
                for mapped_pair in self.mapped_music_items:
                    if modified_pair[1] == mapped_pair[0]:
                        modified_items.append(mapped_pair[1])

        for deleted_pair in self.deleted_items:
            if deleted_pair[0] == "bb":
                for mapped_pair in self.mapped_book_items:
                    if deleted_pair[1] == mapped_pair[0]:
                        deleted_items.append(mapped_pair[1])

            elif deleted_pair[0] == "ma":
                for mapped_pair in self.mapped_magazine_items:
                    if deleted_pair[1] == mapped_pair[0]:
                        deleted_items.append(mapped_pair[1])

            elif deleted_pair[0] == "mo":
                for mapped_pair in self.mapped_movie_items:
                    if deleted_pair[1] == mapped_pair[0]:
                        deleted_items.append(mapped_pair[1])

            elif deleted_pair[0] == "mu":
                for mapped_pair in self.mapped_music_items:
                    if deleted_pair[1] == mapped_pair[0]:
                        deleted_items.append(mapped_pair[1])

        return [created_items, modified_items, deleted_items]
