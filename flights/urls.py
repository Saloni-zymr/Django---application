from knox import views as knox_views

from . import views
from .views import LoginAPI, RegisterAPI, UserAPI, ChangePasswordView
from django.urls import path, include
from rest_framework import routers
from .views import PassengerViewSet, BookingDetailsViewSet, FlightViewSet, UserAPI


routers = routers.DefaultRouter()
routers.register(r'flight', views.FlightViewSet, basename="flightdetails")
routers.register(r'bookingdetails', BookingDetailsViewSet, basename="booking")
routers.register(r'passenger', PassengerViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('api/', include('knox.urls')),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
