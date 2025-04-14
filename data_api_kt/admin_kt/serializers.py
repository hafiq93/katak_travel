from rest_framework import serializers
from rest_framework import serializers
from admin_kt.models import (
    HotelType, HotelFacilities, HotelRoom, 
    RoomFacilities, RoomView, RoomBed, MerchantType,MainMerchant
)


class HotelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelType
        fields = '__all__'

class HotelFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFacilities
        fields = '__all__'

class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = '__all__'

class RoomFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFacilities
        fields = '__all__'

class RoomViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomView
        fields = '__all__'

class RoomBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBed
        fields = '__all__'

class MerchantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantType
        fields = '__all__'

class MainMerchantSerializer(serializers.ModelSerializer):
    merchant_types = MerchantTypeSerializer(many=True, read_only=True)  # Nested merchant types

    class Meta:
        model = MainMerchant
        fields = '__all__'