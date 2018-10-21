from model.Item import Item


class Uow():
    def __init__(self):
        self.mapped_items = []  # Identity map

        self.created_items = []
        self.modified_items = []
        self.deleted_items = []

        self.temp_id_counter = 0

    def get(self, item_id):
        for pair in self.mapped_items:
            if pair[0] == int(item_id):
                return pair[1]
        return None

    def add(self, i):
        if i.id is None:
            self.temp_id_counter -= 1
            i.id = self.temp_id_counter
        self.mapped_items.append((int(i.id), i))

    def register_new(self, i):
        self.created_items.append(int(i.id))

    def register_dirty(self, i):
        # replace the item in the mapped_items
        self.mapped_items[:] = [tup for tup in self.mapped_items if not int(i.id) == tup[0]]
        self.mapped_items.append((int(i.id), i))

        # check if it was already registered
        item_found = False
        for item in self.created_items:
            if item == int(i.id):
                self.created_items.remove(item)
                item_found = True
                break

        if item_found:
            self.created_items.append(int(i.id))

        else:
            for item in self.modified_items:
                if item == i.id:
                    self.modified_items.remove(item)
                    item_found = True
                    break

            if item_found:
                self.modified_items.append(int(i.id))
            else:
                self.modified_items.append(int(i.id))

    def register_deleted(self, item_id):
        self.deleted_items.append(int(item_id))
        if item_id in self.created_items:
            self.created_items.remove(int(item_id))
        if item_id in self.modified_items:
            self.modified_items.remove(int(item_id))

# Retrieve the lists of updates (create, modify, delete)
    def get_saved_changes(self):
        """Create lists of objects (unlike the similarly named
        instance variables, which contains lists of IDs)"""
        created_items = []
        modified_items = []
        deleted_items = []

        for item_id in self.created_items:
            for pair in self.mapped_items:
                if item_id == pair[0]:
                    created_items.append(pair[1])

        for item_id in self.modified_items:
            for pair in self.mapped_items:
                if item_id == pair[0]:
                    modified_items.append(pair[1])

        for item_id in self.deleted_items:
            for pair in self.mapped_items:
                if item_id == pair[0]:
                    deleted_items.append(pair[1])

        return [created_items, modified_items, deleted_items]
