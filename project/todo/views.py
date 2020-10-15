from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .repository import TodoRepository
from .serializers import TodoSerializer, TodoListQueryParamsSerializer
from .services import create_todo, update_todo


class TodoList(APIView):
    def get(self, request, format=None):
        serializer = TodoListQueryParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            todos = TodoRepository.get_list(serializer.validated_data.get('category_id'))
        else:
            todos = TodoRepository.get_list()
        serializer = TodoSerializer(
            instance=todos, many=True
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = create_todo(serializer.validated_data)
        print(serializer)
        return Response(TodoSerializer(todo).data)


class TodoDetail(APIView):
    def get(self, request, pk, format=None):
        todo = TodoRepository.get_single(pk)
        serializer = TodoSerializer(instance=todo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        todo = TodoRepository.get_single(pk)
        serializer = TodoSerializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = update_todo(todo, serializer.validated_data)
        return Response(TodoSerializer(todo).data)

    def delete(self, request, pk, format=None):
        queryset = TodoRepository.get_single(pk)
        TodoRepository.delete(queryset)
        return Response(status=status.HTTP_204_NO_CONTENT)
