import factory
from todo.services import create_todo
from todo.models import Todo


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    @staticmethod
    def _create(cls, model_class=Todo, *args, **kwargs):
        return create_todo(kwargs)
