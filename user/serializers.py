# accounts/serializers.py

from rest_framework import serializers
from .models import User, Customer, Repairer

class UserBaseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password',
                  'pickup_address', 'delivery_address']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')

        pickup_address = validated_data.pop('pickup_address')
        delivery_address = validated_data.pop('delivery_address')

        customer = Customer.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            pickup_address=pickup_address,
            delivery_address=delivery_address
        )
        customer.set_password(password)
        customer.save()
        return customer

class RepairerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    # skill_set = serializers.ListField(child=serializers.CharField(), required=False) # Add this if skillset is a list

    class Meta:
        model = Repairer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password',
                  'nin','rating', 'field', 'wallet_id', 'verification_id', 'work_address']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')

        nin = validated_data.pop('nin')
        rating = validated_data.pop('rating', 0.0)
        field = validated_data.pop('field')
        wallet_id = validated_data.pop('wallet_id')
        verification_id = validated_data.pop('verification_id')
        work_address = validated_data.pop('work_address')

        repairer = Repairer.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            nin=nin,
            rating=rating,
            field=field,
            wallet_id=wallet_id,
            verification_id=verification_id,
            work_address=work_address
        )
        repairer.set_password(password)
        repairer.save()
        return repairer
