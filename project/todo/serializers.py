from rest_framework import serializers
from .repository import Todo
from .managers import Executor


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256, read_only=True)


class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=256)
    category = CategorySerializer()

    def create(self, validated_data):
        text, category_id = validated_data.values()
        print(category_id['id'])
        query = "Insert into todo({0},{1}) values('{2}', {3}) " \
                "RETURNING id".format(*validated_data.keys(),
                                      text,
                                      category_id['id']
                                      )

        print(query)
        id = Executor.save(query)
        print(*validated_data.values())
        return Todo.objects.get(pk=id)

    def update(self, instance, validated_data):
        category = validated_data.pop('category')['id']
        for field, value in validated_data.items():
            print(field, value)
            setattr(instance, field, value)
        instance.category.id = category
        id = instance.id
        query = "UPDATE todo set {1}='{4}',{2}={5} " \
                "where {0}={3}".format(*self.data.keys(),
                                       id,
                                       instance.text,
                                       category
                                       )
        Executor.update(query)
        return instance
