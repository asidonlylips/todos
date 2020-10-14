from rest_framework import viewsets
from .serializers import TodoSerializer
from rest_framework.response import Response
from .repository import Todo
from django_filters.rest_framework import DjangoFilterBackend


class TodoViewSet(viewsets.ViewSet):
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['category', ]
    queryset = Todo.objects.all()

    def list(self, request):
        todos = Todo.objects.all()
        print(todos)
        serializer = TodoSerializer(
            instance=todos, many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj2 = Todo.objects.get(pk=int(pk))
        serializer = TodoSerializer(
            instance=obj2)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def create(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        if pk:  # Only single delete
            queryset = Todo.objects.get(pk=pk)
            print(type(queryset))
            queryset.delete()
        return Response()

    def filter(self):
        pass
