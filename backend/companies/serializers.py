from rest_framework import serializers
from companies.models import Companies

class CompanySerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.name') 

    class Meta:
        model = Companies
        fields = ['id', 'short_name', 'full_name', 'inn', 'kpp', 'ogrn', 'email', 'web_site', 'addr_jur', 'addr_post', 'city', 'bank', 'account', 'city_name']        