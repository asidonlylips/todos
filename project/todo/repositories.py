from django.db import connection
from .models import Todo, Category


class CategoryRepository():
    @staticmethod
    def get_by_name_or_none(name):
        query = "select id, name from category where name='{0}'".format(name)
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                category = Category(*row)
            else:
                category = None
        return category

    @staticmethod
    def create(category):
        query = "insert into category(name) values('{0}') returning id".format(category.name)
        with connection.cursor() as cursor:
            cursor.execute(query)
            category.id = int(cursor.fetchone()[0])
        return category


class TodoRepository():
    @staticmethod
    def get_list(category_id=None):
        query = ('Select todo.id, todo.text, category.id, '
                 'category.name from todo '
                 'join category on todo.category=category.id')
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            queryset = [Todo(*row) for row in rows]
            print(queryset)
        if category_id:  # filtering
            queryset = [item for item in queryset if item.category.id == int(category_id)]
        return queryset

    @staticmethod
    def get_single(pk):
        query = ('select todo.id, todo.text, category.id, '
                 'category.name from todo '
                 'join category on todo.category=category.id '
                 'where todo.id={}'.format(int(pk)))
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            queryset = Todo(*row)
        return queryset

    @staticmethod
    def update(instance):
        with connection.cursor() as cursor:
            query = ("update todo set text='{0}', category={1}"
                     "where id={2}").format(instance.text, instance.category.id, instance.id)
            cursor.execute(query)
        return instance

    @staticmethod
    def create(instance):
        with connection.cursor() as cursor:
            query = ("Insert into todo(text, category) values('{0}', {1}) "
                     "RETURNING id").format(instance.text,
                                            instance.category.id
                                            )
            cursor.execute(query)
            instance.id = int(cursor.fetchone()[0])
        return instance

    @staticmethod
    def delete(instance):
        query = "delete from todo where id={}".format(instance.id)
        with connection.cursor() as cursor:
            cursor.execute(query)
