from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import RepairJob
from .serializers import RepairJobSerializer


class RepairJobViewSet(viewsets.ModelViewSet):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
