from rest_framework import serializers

from bids.serializers import BidSerializer
from job.models import RepairJob


class RepairJobSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')
    status = serializers.ReadOnlyField()
    bid_deadline = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = (
            RepairJob)
        fields = [
            'id', 'customer', 'device_brand', 'device_model', 'issue_description',
            'budget', 'status', 'image', 'created_at', 'bid_deadline', 'bids'
        ]
        read_only_fields = ['status', 'created_at', 'bid_deadline', 'customer', 'bids']