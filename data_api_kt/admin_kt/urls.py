from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HotelTypeViewSet,
    HotelFacilitiesViewSet,
    HotelRoomViewSet,
    RoomFacilitiesViewSet,
    RoomViewViewSet,
    RoomBedViewSet,
    MerchantTypeViewSet
)


# DRF Router
router = DefaultRouter()
router.register(r'hotel-types', HotelTypeViewSet)
router.register(r'hotel-facilities', HotelFacilitiesViewSet)
router.register(r'hotel-rooms', HotelRoomViewSet)
router.register(r'room-facilities', RoomFacilitiesViewSet)
router.register(r'room-views', RoomViewViewSet)
router.register(r'room-beds', RoomBedViewSet)
router.register(r'merchant-types', MerchantTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]