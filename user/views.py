from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Customer, Repairer
from .serializers import CustomerSerializer, RepairerSerializer, LoginSerializer

class RegisterCustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        token, _ = Token.objects.get_or_create(user=customer)
        return Response({
            "message": f"Customer {customer.username} registered successfully.",
            "token": token.key,
            "user_type": customer.user_type,
            "dashboard": "customer" if customer.user_type in ['customer', 'both'] else customer.user_type
        }, status=status.HTTP_201_CREATED)

class RegisterRepairerView(generics.CreateAPIView):
    queryset = Repairer.objects.all()
    serializer_class = RepairerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repairer = serializer.save()
        token, _ = Token.objects.get_or_create(user=repairer)
        return Response({
            "message": f"Repairer {repairer.username} registered successfully.",
            "token": token.key,
            "user_type": repairer.user_type,
            "dashboard": "repairer" if repairer.user_type in ['repairer', 'both'] else repairer.user_type
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        dashboard = 'admin' if user.user_type == 'admin' else (
            'both' if user.user_type == 'both' else user.user_type
        )
        return Response({
            "token": token.key,
            "message": f"Welcome back, {user.first_name}!",
            "user_type": user.user_type,
            "dashboard": dashboard
        })
