from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from services.verification.serializers import VerificationSerializer
from services.verification.service import VerificationService


class VerifyNINView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        nin = request.data['nin']
        service = VerificationService()
        record = service.verify_nin(request.user.id, nin)
        return Response(VerificationSerializer(record).data)