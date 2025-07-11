from rest_framework import serializers
from .models import RepairJob

class RepairJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairJob
        fields = '__all__'
