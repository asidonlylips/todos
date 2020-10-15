from rest_framework import viewsets
from .serializers import TodoSerializer
from rest_framework.response import Response
from .models import Todo
from rest_framework import status

class TodoViewSet(viewsets.ViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def list(self, request):
        todos = Todo.objects.all()
        print(todos)
        todos = todo_filter(todos, request.query_params)
        serializer = TodoSerializer(
            instance=todos, many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj2 = Todo.objects.get(pk=int(pk))
        serializer = TodoSerializer(instance=obj2)
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
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

def todo_filter(object, params):
    for x,y in params.items():
        if(x=='category'):
            object = [obj for obj in object if obj.__dict__[x]==y]
    return object
