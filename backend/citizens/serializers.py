from rest_framework import serializers
from citizens.models import Citizens

class CitizenSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='build.street.city.name') 
    address = serializers.ReadOnlyField(source='build.addr') 

    class Meta:
        model = Citizens
        fields = '__all__'