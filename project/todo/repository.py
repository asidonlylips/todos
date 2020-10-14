from .managers import TodoManager


class Category():
    def __init__(self, args):
        print(args)
        self.id, self.name = args


class Todo():
    objects = TodoManager()

    def __init__(self, *args):
        self.id, self.text, *params = args
        self.category = Category(params)

    def delete(self):
        self.objects.delete(self.id)

    def __str__(self):
        return str(self.__dict__)
