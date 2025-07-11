from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Customer, Repairer
from .serializers import CustomerSerializer, RepairerSerializer

class RegisterCustomer(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.create(user=user)
        return Response(
            {'message': f'Dear {user.username}, you have registered successfully.'},
            status=status.HTTP_201_CREATED
        )

class RegisterRepairer(generics.CreateAPIView):
    queryset = Repairer.objects.all()
    serializer_class = RepairerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.create(user=user)
        return Response(
            {'message': f'Dear {user.username}, you have registered successfully.'},
            status=status.HTTP_201_CREATED
        )

class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': f'Dear {user.first_name}, you have logged in successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
