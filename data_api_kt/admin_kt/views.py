from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from admin_kt.models import (
    HotelType, HotelFacilities, HotelRoom, 
    RoomFacilities, RoomView, RoomBed, MerchantType,MainMerchant
)
from .serializers import (
    HotelTypeSerializer, HotelFacilitiesSerializer, HotelRoomSerializer, 
    RoomFacilitiesSerializer, RoomViewSerializer, RoomBedSerializer, MerchantTypeSerializer,
    MainMerchantSerializer
)
from pack_list_kt.models import MerchantPackage

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

# Merchant Type ViewSet
class MainMerchantViewSet(viewsets.ModelViewSet):
    queryset = MainMerchant.objects.all()
    serializer_class = MainMerchantSerializer

class MerchantsByTypeView(APIView):
    def get(self, request, type_id):
        merchants = Merchant.objects.filter(type_id=type_id)
        serializer = MerchantSerializer(merchants, many=True)
        return Response(serializer.data)