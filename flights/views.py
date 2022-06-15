from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from knox.models import AuthToken

from .models import User, FlightDetails, Booking_details, Passenger
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": AuthToken.objects.create(user)[1],
            "msg": "Registration successful"
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


from rest_framework import generics, permissions

# Change Password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, FlightDetailsSerializers, PassengerSerializers, BookingSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# @api_view(http_method_names=['GET'])
class FlightViewSet(viewsets.ModelViewSet):
    queryset = FlightDetails.objects.all()
    serializer_class = FlightDetailsSerializers

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class BookingDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthenticated,
    queryset = Booking_details.objects.all()
    serializer_class = BookingSerializers

    def get_queryset(self):
        book = Booking_details.objects.all()
        return book

    def create(self, request, *args, **kwargs):
        data = request.data

        user = User.objects.get(pk=data["u_id"])
        flightdetails = FlightDetails.objects.get(pk=data["f_id"])

        new_book = Booking_details.objects.create(
            trip_date=data["trip_date"],
            no_of_passengers=data["no_of_passengers"],
            price=flightdetails.price * len(data["passenger"]),
            u_id=user,
            f_id=flightdetails,
        )
        new_book.save()
        for passenger in data["passenger"]:
            p = Passenger.objects.create(
                name=passenger["name"],
                age=passenger["age"],
                gender=passenger["gender"],
                contact=passenger["contact"],
                u_id=user,
            )
            new_book.passenger.add(p)

        if flightdetails.avail_seats < len(data["passenger"]):
            return Response({"data": "No seats available", "status": status.HTTP_400_BAD_REQUEST})
        update_seats = flightdetails.avail_seats - data["no_of_passengers"]
        flightdetails.avail_seats = update_seats
        flightdetails.save()
        serializers = BookingSerializers(new_book)
        return Response({"data": serializers.data, "status": status.HTTP_201_CREATED})


class PassengerViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializers
