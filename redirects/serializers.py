from rest_framework import serializers
from .models import Redirect


class RedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redirect
        # fields = ('key','url','active','created_at','updated_at')
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
