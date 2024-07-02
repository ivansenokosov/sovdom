from rest_framework import serializers
from catalogs.models import Cities
from builds_services.models import BuildServiceContainerTypes, BuildServiceContainerUnits
from citizens.models import Citizens
# from mail.models import GZHIActionTypes, Mail_status

class CitiesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return '{} ({})'.format(obj.name, obj.region.name)  

    class Meta:
        model = Cities
        fields = ['name','id']


class CitiesYMapSerializer(serializers.ModelSerializer):
    qbuilds = serializers.SerializerMethodField()

    def get_qbuilds(self, obj):
        return obj.count_builds() 
        
    class Meta:
        model = Cities
        fields = ['id','name','ymap', 'qbuilds']


class BuildServiceContainerTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildServiceContainerTypes
        fields = '__all__'


class BuildServiceContainerUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildServiceContainerUnits
        fields = ['name','id']

        
class CitizensSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return f'{obj.family_name} {obj.first_name} {obj.second_name}, кв. {obj.flat}'  
    
    class Meta:
        model = Citizens
        fields = ['name','id']

