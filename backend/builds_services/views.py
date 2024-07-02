from builds_services.models import BuildServiceContainer

from rest_framework import viewsets, permissions
from builds_services.serializers import BuildServiceContainerSerializer
from rest_framework.response import Response

class BuildServiceContainerViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = BuildServiceContainer.objects.all()
    serializer_class = BuildServiceContainerSerializer
    
    def list(self, request):
        queryset = BuildServiceContainer.objects.all().order_by('id')[:10]
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)

    def retrieve(self, request, pk=None):
        object = self.queryset.get(pk=pk)
        serializer = self.serializer_class(object)
        return Response(serializer.data)

    def update(self, request, pk=None):
        object = self.queryset.get(pk=pk)
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)        

    def destroy(self, request, pk=None):
        object = self.queryset.get(pk=pk)
        object.delete()
        return Response(status = 204) 


