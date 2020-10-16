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
        query = ("insert into category(name) values('{0}') "
                 "returning id").format(category.name)
        with connection.cursor() as cursor:
            cursor.execute(query)
            category.id = cursor.fetchone()[0]
        return category


class TodoRepository():
    @staticmethod
    def get_list(category_id=None):
        with connection.cursor() as cursor:
            query = ('Select todo.id, todo.text, category.id, '
                     'category.name from todo '
                     'join category on todo.category=category.id')
            if category_id:
                query += " where category.id={}".format(category_id)
            cursor.execute(query)
            rows = cursor.fetchall()
            todos = [Todo(*row[:2], Category(*row[2:])) for row in rows]
        return todos

    @staticmethod
    def get_single(pk):
        query = ('select todo.id, todo.text, category.id, '
                 'category.name from todo '
                 'join category on todo.category=category.id '
                 'where todo.id={}'.format(pk))
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            todo = Todo(*row[:2], Category(*row[2:]))
        return todo

    @staticmethod
    def update(instance):
        with connection.cursor() as cursor:
            query = ("update todo set text='{0}', category={1}"
                     "where id={2}").format(instance.text,
                                            instance.category.id,
                                            instance.id)
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
            instance.id = cursor.fetchone()[0]
        return instance

    @staticmethod
    def delete(instance):
        query = "delete from todo where id={}".format(instance.id)
        with connection.cursor() as cursor:
            cursor.execute(query)

    @staticmethod
    def is_pk_exist(pk):
        with connection.cursor() as cursor:
            query = ("select todo.id from todo where id={}").format(pk)
            cursor.execute(query)
            row = cursor.fetchone()
        return bool(row)
