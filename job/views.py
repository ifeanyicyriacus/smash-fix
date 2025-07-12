from rest_framework import generics, permissions
from rest_framework.response import Response

from bids.models import Bid
from job.models import RepairJob
from job.serializers import RepairJobSerializer


class JobCreateView(generics.CreateAPIView):
    serializer_class = RepairJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user, status='open')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        job = self.get_queryset().get(id=response.data['id'])
        return Response({
            'jobId': job.id,
            'bidDeadline': job.bid_deadline
        })

class JobListView(generics.ListAPIView):
    serializer_class = RepairJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Customers see their own jobs
        return RepairJob.objects.filter(customer=self.request.user)

class JobDetailView(generics.RetrieveAPIView):
    serializer_class = RepairJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = RepairJob.objects.all()

class AcceptBidView(generics.UpdateAPIView):
    serializer_class = RepairJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = RepairJob.objects.all()

    def patch(self, request, *args, **kwargs):
        job = self.get_object()
        selected_bid_id = request.data.get('selectedBidId')
        status = request.data.get('status')

        if status != 'assigned':
            return Response({'error': 'Invalid status update'}, status=400)

        try:
            bid = job.bids.get(id=selected_bid_id)
        except Bid.DoesNotExist:
            return Response({'error': 'Bid not found'}, status=404)

        # Update all bids statuses
        job.bids.update(status='rejected')
        bid.status = 'accepted'
        bid.save()

        # Update job status
        job.status = 'assigned'
        job.save()

        return Response({'detail': 'Bid accepted and job assigned'})

class PostRatingView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Implement rating logic here (e.g., save rating and comment linked to job and repairer)
        # Placeholder response
        return Response({'detail': 'Rating submitted'})