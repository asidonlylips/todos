from django.db import connection


class Executor():

    @staticmethod
    def get(query):
        cursor = connection.cursor()
        cursor.execute(query)

        from .repository import Todo
        row = cursor.fetchone()
        return Todo(*row)

    @staticmethod
    def list(query):
        cursor = connection.cursor()
        cursor.execute(query)

        from .repository import Todo
        object = [Todo(*row) for row in cursor.fetchall()]
        object = dict(zip(range(len(object)), object))
        return object.values()

    @staticmethod
    def update(query):
        cursor = connection.cursor()
        cursor.execute(query)

    @staticmethod
    def save(query):
        cursor = connection.cursor()
        cursor.execute(query)
        id = cursor.fetchone()[0]
        return id

    @staticmethod
    def delete(query):
        cursor = connection.cursor()
        cursor.execute(query)


class TodoManager():
    @staticmethod
    def all():
        return Executor.list('Select todo.id, todo.text, category.id, '
                             'category.name from todo '
                             'join category on todo.category=category.id')

    @staticmethod
    def get(*args, pk):
        return Executor.get('select todo.id, todo.text, category.id, '
                            'category.name from todo '
                            'join category on todo.category=category.id '
                            'where todo.id={}'.format(int(pk)))

    def delete(self, pk):
        query = "delete from todo where id={}".format(pk)
        Executor.delete(query)
