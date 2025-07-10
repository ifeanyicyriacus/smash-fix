from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Customer, Repairer
from .serializers import CustomerSerializer, RepairerSerializer

class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f"Dear {serializer.validated_data['first_name']}, you have registered successfully.", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterRepairer(APIView):
    def post(self, request):
        serializer = RepairerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f"Dear {serializer.validated_data['first_name']}, you have registered successfully.", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response(f"Dear {user.first_name}, you have logged in successfully.", status=status.HTTP_200_OK)
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
