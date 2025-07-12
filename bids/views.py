from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bid
from .serializers import BidSerializer
from job.models import RepairJob

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign logged-in user as repairer
        serializer.save(repairer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        """
        Custom action to accept a bid.
        Only the customer who owns the job can accept a bid.
        """
        bid = self.get_object()
        job = bid.job

        # Check if the logged-in user is the job owner (customer)
        if job.customer != request.user:
            return Response({'error': 'You are not authorized to accept this bid.'}, status=status.HTTP_403_FORBIDDEN)

        # Mark all other bids for the job as rejected
        Bid.objects.filter(job=job).exclude(id=bid.id).update(status='R')

        # Mark this bid as accepted
        bid.status = 'A'
        bid.save()

        # Update job status to ASSIGNED
        job.status = 'ASSIGNED'
        job.save()

        return Response({'message': f'Bid {bid.id} accepted for job {job.id}.'}, status=status.HTTP_200_OK)
