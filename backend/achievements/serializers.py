from rest_framework import serializers
from achievements.models import Achievement

class AchievementSerializer(serializers.ModelSerializer):
    address = serializers.ReadOnlyField(source='build.addr')
    class Meta:
        model = Achievement
        fields = '__all__'