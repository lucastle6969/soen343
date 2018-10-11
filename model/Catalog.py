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
    
    def add_item(self):
        pass
    
    def edit_item(self, item, id):
        for entry in self.item_catalog:
            if entry.id == id:
                self.item_catalog.remove(entry)
        self.item_catalog.append(item)



    def delete_item(self):
        pass


