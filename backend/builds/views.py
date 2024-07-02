from builds.models import Builds, Streets, Cities
from citizens.models import Citizens
from rest_framework import viewsets, permissions
from builds.serializers import BuildsSerializer
from rest_framework.response import Response

class BuildsViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Builds.objects.all().filter(city = 1)
    serializer_class = BuildsSerializer
    
    def list(self, request):
        queryset = Builds.objects.all().filter(city = 1)
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
        company = self.queryset.get(pk=pk)
        company.delete()
        return Response(status = 204)     

