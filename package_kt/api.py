from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import System
from .serializers import SystemSerializer

@api_view(['GET'])
def get_system_packages(request, system_id):
    try:
        system = System.objects.get(id=system_id)
        serializer = SystemSerializer(system)
        return Response(serializer.data)
    except System.DoesNotExist:
        return Response({'error': 'System not found'}, status=status.HTTP_404_NOT_FOUND)