from rest_framework import serializers
from .models import RepairJob, RepairJobImage


class RepairJobImageSerializer:
    class Meta:
        model = RepairJobImage
        fields = ['id', 'issue_image_video_links']


class RepairJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairJob
        fields = [
            'customer',
            'device_brand',
            'device_model',
            'issue_description',
            'budget',
            'status',
            'image',
            'bid_deadline',
        ]
        read_only_fields = ['id', 'customer', 'status', 'created_at', 'bid_deadline']

