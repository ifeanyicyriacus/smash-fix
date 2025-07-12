from rest_framework import permissions, generics, serializers
from rest_framework.response import Response

from bids.models import Bid
from bids.serializers import BidSerializer
from job.models import RepairJob


class BidListView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status == 'open':
            return Bid.objects.filter(job__status__in=['open', 'bidding'])
        return Bid.objects.none()

class BidCreateView(generics.CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job_id = self.request.data.get('job')
        job = RepairJob.objects.get(id=job_id)

        if job.status not in ['open', 'bidding']:
            raise serializers.ValidationError("Bidding is closed for this job.")

        if job.status == 'open':
            job.status = 'bidding'
            job.save()

        serializer.save(repairer=self.request.user, job=job, status='pending')

class MyBidsListView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(repairer=self.request.user)

class BidUpdateView(generics.UpdateAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Bid.objects.all()

    def patch(self, request, *args, **kwargs):
        bid = self.get_object()
        if bid.status != 'pending':
            return Response({'error': 'Cannot update bid unless it is pending'}, status=400)
        return super().patch(request, *args, **kwargs)