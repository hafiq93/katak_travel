# D:\Work\katak_travel\package_kt\views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import System, Package, SubPackage, SubPackage_2

@api_view(['GET'])
def get_packages(request, system_id):
    packages = Package.objects.filter(system_id=system_id)
    package_data = [{"id": package.id, "name": package.name} for package in packages]
    return Response(package_data)

@api_view(['GET'])
def get_subpackages(request, package_id):
    subpackages = SubPackage.objects.filter(package_id=package_id)
    subpackage_data = [{"id": subpackage.id, "name": subpackage.name} for subpackage in subpackages]
    return Response(subpackage_data)

@api_view(['GET'])
def get_subpackage_2(request, subpackage_id):
    subpackage_2 = SubPackage_2.objects.filter(subpackage_id=subpackage_id)
    subpackage_2_data = [{"id": subpkg.id, "name": subpkg.name} for subpkg in subpackage_2]
    return Response(subpackage_2_data)