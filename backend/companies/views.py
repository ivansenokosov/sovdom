from catalogs.models import Cities
from companies import serializers
from companies.models import Companies


from rest_framework import viewsets, permissions
from companies.serializers import CompanySerializer
from rest_framework.response import Response

class CompanyViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Companies.objects.all()
    serializer_class = CompanySerializer
    
    def list(self, request):
        queryset = Companies.objects.all()
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
        company = self.queryset.get(pk=pk)
        serializer = self.serializer_class(company)
        return Response(serializer.data)

    def update(self, request, pk=None):
        company = self.queryset.get(pk=pk)
        serializer = self.serializer_class(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)        

    def destroy(self, request, pk=None):
        company = self.queryset.get(pk=pk)
        company.delete()
        return Response(status = 204)         

