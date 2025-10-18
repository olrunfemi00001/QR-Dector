from rest_framework import serializers

class QRDetectionSerializer(serializers.Serializer):
    qr_hash = serializers.CharField(max_length=256)
