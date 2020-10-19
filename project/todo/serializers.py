from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)


class TodoListQueryParamsSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)


class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=256)
    category = CategorySerializer()
