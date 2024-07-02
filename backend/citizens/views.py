from django.http import JsonResponse
from django.http import HttpResponse
from citizens.models import Citizens

from rest_framework import viewsets, permissions
from citizens.serializers import CitizenSerializer
from rest_framework.response import Response


class CitizenViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Citizens.objects.all()
    serializer_class = CitizenSerializer
    
    def list(self, request):
        queryset = Citizens.objects.all()
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

