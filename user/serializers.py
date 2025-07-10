from rest_framework import serializers
from .models import User, Customer, Repairer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']

class CustomerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Customer
        fields = UserSerializer.Meta.fields + ['pickup_address', 'delivery_address']

class RepairerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Repairer
        fields = UserSerializer.Meta.fields + ['nin', 'skill_set', 'rating', 'field', 'wallet_id', 'verification_id', 'work_address']
