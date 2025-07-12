from rest_framework import serializers
from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['id', 'repairer', 'created_at', 'status']
