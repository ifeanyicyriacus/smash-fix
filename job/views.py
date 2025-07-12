from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import RepairJob
from .serializers import RepairJobSerializer

class RepairJobViewSet(viewsets.ModelViewSet):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        bid_deadline = timezone.now() + timedelta(days=3)
        job = serializer.save(customer=self.request.user, status='OPEN', bid_deadline=bid_deadline)
        self.job_response = {
            'jobId': str(job.id),
            'bidDeadline': job.bid_deadline
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if hasattr(self, 'job_response'):
            response.data = self.job_response
        return response
