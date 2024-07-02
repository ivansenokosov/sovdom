from rest_framework import serializers
from builds_services.models import BuildServiceContainer

class BuildServiceContainerSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='build.street.city.name') 
    # city = serializers.ReadOnlyField(source='build.street.city') 
    address = serializers.ReadOnlyField(source='build.addr') 
    type_name = serializers.ReadOnlyField(source='type.name') 


    class Meta:
        model = BuildServiceContainer
        fields = '__all__'