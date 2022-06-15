from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework import serializers

# User Serializer
from flights.models import User, FlightDetails, Passenger, Booking_details


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# # Login Serializer
# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}
from django.utils.translation import gettext_lazy as _


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
    #
    #     return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')


class FlightDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlightDetails
        fields = "__all__"


class PassengerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking_details
        fields = "__all__"
        depth = 1


# Change Password
from rest_framework import serializers
from django.contrib.auth.models import User


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
