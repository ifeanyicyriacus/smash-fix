from rest_framework import serializers

from bids.models import Bid


class BidSerializer(serializers.ModelSerializer):
    repairer = serializers.ReadOnlyField(source='repairer.username')
    status = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'repairer']