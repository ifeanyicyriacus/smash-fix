from rest_framework import serializers
from .models import User, Customer, Repairer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'pickup_address', 'delivery_address']

class RepairerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repairer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'nin', 'rating', 'field', 'wallet_id', 'verification_id', 'work_address']
