from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import QRDetection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import QRDetection
from .serializers import QRDetectionSerializer

class QRReceiveView(APIView):
    def post(self, request):
        serializer = QRDetectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        qr_data = serializer.validated_data['qr_hash']

        # Save to database if not already exists
        obj, created = QRDetection.objects.get_or_create(qr_hash=qr_data)

        # Example webhook
        webhook_url = 'https://example.com/webhook'
        contact_info = {"name": "John Doe", "email": "johndoe@example.com"}
        requests.post(webhook_url, json=contact_info)

        return Response({
            'message': 'QR processed',
            'new_entry': created,
            'data_sent': contact_info
        }, status=200)
