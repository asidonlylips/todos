class Category():
    def __init__(self, id, name):
        self.id, self.name = id, name


class Todo():
    def __init__(self, id, text, category):
        self.id, self.text, self.category = id, text, category
