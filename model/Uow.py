from model.Item import Item


class Uow():
    def __init__(self):
        self.mapped_items = []  # Identity map

        self.created_items = []
        self.modified_items = []
        self.deleted_items = []

    def get(item_id):
        for pair in self.mapped_items:
            if pair[item_id] is not None:
                return pair[item_id]

    def add(self, i):
        self.mapped_items.append((i.id, i))

    def register_new(self, i):
        self.created_items.append(i.id)

    def register_dirty(self, i):
        item_found = False
        for item in self.created_items:
            if item.id == i.id:
                self.created_items.remove(item)
                item_found = True
                break

        if item_found:
            self.created_items.append(i.id)

        else:
            for item in self.modified_items:
                if item.id == i.id:
                    self.modified_items.remove(item)
                    item_found = True
                    break

            if item_found:
                self.modified_items.append(i.id)
            else:
                raise Exception(f'UoW: Tried to register dirty item(id {i.id})'
                                ',but item was not found.')

    def register_deleted(self, item_id):
        self.deleted_items.append(item_id)
        if item_id in self.created_items:
            self.created_items.remove(item_id)
        if item_id in self.modified_items:
            self.modified_items.remove(item_id)

# Retrieve the lists of updates (create, modify, delete)
    def get_saved_changes(self):
        """Create lists of objects (unlike the similarly named
        instance variables, which contains lists of IDs)"""
        created_items = []
        modified_items = []
        deleted_items = []

        for pair in self.mapped_items:
            for item_id in self.created_items:
                item = pair[item_id]
                if item is not None:
                    created_items.append(item)

            for item_id in self.modified_items:
                item = pair[item_id]
                if item is not None:
                    modified_items.append(item)

            for item_id in self.deleted_items:
                item = pair[item_id]
                if item is not None:
                    deleted_items.append(item)

        # If a list is empty, set it to None (easier checking in mapper.)
        if len(created_items) == 0:
            created_items = None
        if len(modified_items) == 0:
            modified_items = None
        if len(deleted_items) == 0:
            deleted_items = None

        return [created_items, modified_items, deleted_items]
