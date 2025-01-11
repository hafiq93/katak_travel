from django.http import HttpResponse
from rest_framework import viewsets
from admin_kt.models import (
    HotelType, HotelFacilities, HotelRoom, 
    RoomFacilities, RoomView, RoomBed, MerchantType
)
from .serializers import (
    HotelTypeSerializer, HotelFacilitiesSerializer, HotelRoomSerializer, 
    RoomFacilitiesSerializer, RoomViewSerializer, RoomBedSerializer, MerchantTypeSerializer
)

# Hotel Type ViewSet
class HotelTypeViewSet(viewsets.ModelViewSet):
    queryset = HotelType.objects.all()
    serializer_class = HotelTypeSerializer

# Hotel Facilities ViewSet
class HotelFacilitiesViewSet(viewsets.ModelViewSet):
    queryset = HotelFacilities.objects.all()
    serializer_class = HotelFacilitiesSerializer

# Hotel Room ViewSet
class HotelRoomViewSet(viewsets.ModelViewSet):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer

# Room Facilities ViewSet
class RoomFacilitiesViewSet(viewsets.ModelViewSet):
    queryset = RoomFacilities.objects.all()
    serializer_class = RoomFacilitiesSerializer

# Room View ViewSet
class RoomViewViewSet(viewsets.ModelViewSet):
    queryset = RoomView.objects.all()
    serializer_class = RoomViewSerializer

# Room Bed ViewSet
class RoomBedViewSet(viewsets.ModelViewSet):
    queryset = RoomBed.objects.all()
    serializer_class = RoomBedSerializer

# Merchant Type ViewSet
class MerchantTypeViewSet(viewsets.ModelViewSet):
    queryset = MerchantType.objects.all()
    serializer_class = MerchantTypeSerializer