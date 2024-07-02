from rest_framework import serializers
from builds.models import Builds

class BuildsSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='street.city.name') 
    addr_str = serializers.ReadOnlyField(source='addr') 
    management_str = serializers.ReadOnlyField(source='management_name')

    total_rub = serializers.SerializerMethodField()
    report_rub = serializers.SerializerMethodField()
    management_rub = serializers.SerializerMethodField()
    repair_rub = serializers.SerializerMethodField()
    report_number = serializers.SerializerMethodField()

    def get_total_rub(self, obj):
        return round(obj.total_rub(),2)

    def get_report_rub(self, obj):
        return round(obj.report_rub(),2)  

    def get_management_rub(self, obj):
        return round(obj.management_rub(),2)

    def get_repair_rub(self, obj):
        return round(obj.repair_rub(),2)

    def get_report_number(self, obj):
        return obj.report_number()  

    class Meta:
        model = Builds
        fields = '__all__'


class BuildsForCatalogSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='addr') 

    class Meta:
        model = Builds
        fields = ['id', 'name', ]