class Catalog:

    def __init__(self):
        self.item_catalog = []

    def getItemById(self, id):
        intId = int(id)
        for item in self.item_catalog:
            print(item.id)
            if item.id == intId:
                print("Returning an item")
                return item
        return None

    def get_all_items(self):
        pass
    
    def add_item(self):
        pass
    
    def edit_item(self):
        pass

    def delete_item(self):
        pass


