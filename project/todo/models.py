class Category():
    def __init__(self, id, name):
        self.id, self.name = id, name


class Todo():

    def __init__(self, id, text, *category_params):
        self.id, self.text, params = id, text, category_params
        self.category = Category(*category_params)
