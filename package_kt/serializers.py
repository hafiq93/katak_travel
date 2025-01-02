# package_kt/serializers.py
from rest_framework import serializers
from .models import System, Package, SubPackage, SubPackage_2

class SubPackage2Serializer(serializers.ModelSerializer):
    class Meta:
        model = SubPackage_2
        fields = ['id', 'name', 'description']

class SubPackageSerializer(serializers.ModelSerializer):
    sub_packages_2 = SubPackage2Serializer(many=True, read_only=True)

    class Meta:
        model = SubPackage
        fields = ['id', 'name', 'description', 'sub_packages_2']

class PackageSerializer(serializers.ModelSerializer):
    sub_packages = SubPackageSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ['id', 'name', 'description', 'sub_packages']

class SystemSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = System
        fields = ['id', 'name', 'packages']