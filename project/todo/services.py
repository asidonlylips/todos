from .repositories import CategoryRepository
from .repositories import TodoRepository
from .models import Category, Todo


def create_todo(todo_data):
    text = todo_data.get('text')
    category_name = todo_data.get('category').get('name')
    category = _get_or_create_category_by_name(category_name)
    todo = Todo(None, text, category.id, category.name)
    todo = TodoRepository.create(todo)
    return todo


def update_todo(instance, todo_data):
    text = todo_data.get('text')
    category_name = todo_data.get('category').get('name')
    category = _get_or_create_category_by_name(category_name)
    instance = Todo(instance.id, text, category.id, category.name)
    todo = TodoRepository.update(instance)
    return todo


def _get_or_create_category_by_name(name) -> Category:
    category = CategoryRepository.get_by_name_or_none(name)
    if not category:
        category = CategoryRepository.create(Category(None, name))
    return category
