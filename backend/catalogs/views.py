

from catalogs.models import Cities
from catalogs.serializers import CitiesSerializer
from rest_framework import viewsets, permissions
from catalogs.serializers import (CitiesSerializer, 
                                 BuildServiceContainerTypesSerializer, 
                                 BuildServiceContainerUnitsSerializer, 
                                 CitizensSerializer,
                                 CitiesYMapSerializer
                                 )

from builds.serializers import BuildsForCatalogSerializer
from builds.models import Builds
from builds_services.models import BuildServiceContainerTypes, BuildServiceContainerUnits
from citizens.models import Citizens
from django.db.models import Q

from rest_framework.response import Response

class CitiesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitiesSerializer

class CitiesYMAPViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Cities.objects.exclude(Q(ymap__isnull=True) | Q(ymap__exact='')).order_by('name')
    serializer_class = CitiesYMapSerializer    
    
class BuildsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Builds.objects.all().order_by('street__name').distinct()
    serializer_class = BuildsForCatalogSerializer
    
    def get_queryset(self):
        qs = Builds.objects.all().order_by('street__name').distinct()
        city = self.request.query_params.get('city')
        if city is not None:
            qs = qs.filter(city=city).order_by('street__name').distinct()
        return qs
    
class CitizensViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Citizens.objects.all().order_by('family_name')
    serializer_class = CitizensSerializer
    
    def get_queryset(self):
        qs = Citizens.objects.all().order_by('family_name')
        build = self.request.query_params.get('build')
        if build is not None:
            qs = qs.filter(build=build).order_by('family_name')
        return qs

class BuildServiceContainerUnitsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = BuildServiceContainerUnits.objects.all().order_by('id')
    serializer_class = BuildServiceContainerUnitsSerializer

class BuildServiceContainerTypesViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = BuildServiceContainerTypes.objects.all().order_by('id')
    serializer_class = BuildServiceContainerTypesSerializer
    
    def list(self, request):
        queryset = BuildServiceContainerTypes.objects.all().order_by('id')
        serializer = self.serializer_class(queryset, many = True)
        return Response(serializer.data)
    