from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from services.logistics.models import LogisticsAssignment
from services.logistics.serializers import LogisticsSerializer


class LogisticsStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        assignment = get_object_or_404(LogisticsAssignment, job_id=job_id)
        return Response(LogisticsSerializer(assignment).data)