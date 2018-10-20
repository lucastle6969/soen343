from model.Item import Item


class Uow():
    def __init__(self):
        self.mapped_items = []  # Identity map

        self.created_items = []
        self.modified_items = []
        self.deleted_items = []

    def add(self, i):
        self.mapped_items.append((i.id, i))

    def registerNew(self, i):
        self.created_items.append(i.id)

    def registerDirty(self, i):
        for item in self.modified_items:
            if item.id == i.id:
                self.modified_items.remove(item)
        self.modified_items.append(i.id)

    def registerDeleted(self, item_id):
        self.deleted_items.append(item_id)
        if i in self.created_items:
            self.created_items.remove(i)
        if i in self.modified_items:
            self.modified_items.remove(i)

# Retrieve the lists of updates (create, modify, delete) and clear this UoW.
    def commit(self):
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
        if len(self.created_items) == 0:
            self.created_items = None
        if len(self.modified_items) == 0:
            self.modified_items = None
        if len(self.deleted_items) == 0:
            self.deleted_items = None
        return [created_items, modified_items, deleted_items]