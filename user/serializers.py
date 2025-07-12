from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from .models import User, Customer, Repairer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password',
                  'pickup_address', 'delivery_address', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')
        phone = validated_data.get('phone')

        existing_user = User.objects.filter(username=username).first() or User.objects.filter(phone=phone).first()

        if existing_user:
            if not check_password(password, existing_user.password):
                raise serializers.ValidationError({"password": "Password does not match existing user."})
            if hasattr(existing_user, 'customer'):
                raise serializers.ValidationError({"detail": "Customer profile already exists."})

            if existing_user.user_type == 'repairer':
                existing_user.user_type = 'both'
            else:
                existing_user.user_type = 'customer'

            for attr in ['first_name', 'last_name', 'email', 'phone']:
                setattr(existing_user, attr, validated_data.get(attr, getattr(existing_user, attr)))
            existing_user.save()

            customer = Customer.objects.create(
                user_ptr=existing_user,
                pickup_address=validated_data['pickup_address'],
                delivery_address=validated_data['delivery_address'],
            )
            return customer

        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.user_type = 'customer'
        customer.save()
        return customer


class RepairerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.CharField(read_only=True)
    rating = serializers.FloatField(read_only=True)  # rating is read-only

    class Meta:
        model = Repairer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password',
                  'nin', 'rating', 'field', 'wallet_id', 'verification_id', 'work_address', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')
        phone = validated_data.get('phone')

        existing_user = User.objects.filter(username=username).first() or User.objects.filter(phone=phone).first()

        if existing_user:
            if not check_password(password, existing_user.password):
                raise serializers.ValidationError({"password": "Password does not match existing user."})
            if hasattr(existing_user, 'repairer'):
                raise serializers.ValidationError({"detail": "Repairer profile already exists."})

            if existing_user.user_type == 'customer':
                existing_user.user_type = 'both'
            else:
                existing_user.user_type = 'repairer'

            for attr in ['first_name', 'last_name', 'email', 'phone']:
                setattr(existing_user, attr, validated_data.get(attr, getattr(existing_user, attr)))
            existing_user.save()

            repairer = Repairer.objects.create(
                user_ptr=existing_user,
                nin=validated_data['nin'],
                field=validated_data['field'],
                wallet_id=validated_data['wallet_id'],
                verification_id=validated_data['verification_id'],
                work_address=validated_data['work_address'],
            )
            return repairer

        repairer = Repairer(**validated_data)
        repairer.set_password(password)
        repairer.user_type = 'repairer'
        repairer.save()
        return repairer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        data['user'] = user
        return data
