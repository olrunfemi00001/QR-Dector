from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import cv2, hashlib, requests
from django.http import StreamingHttpResponse
from .models import QRDetection
from .serializers import QRDetectionSerializer


# ----------------------------
# QR API Endpoint
# ----------------------------
class QRReceiveView(APIView):
    @swagger_auto_schema(
        request_body=QRDetectionSerializer,
        responses={200: 'QR processed successfully'}
    )
    def post(self, request):
        serializer = QRDetectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        qr_data = serializer.validated_data['qr_hash']
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


# ----------------------------
# Live stream with built-in QR detection
# ----------------------------
API_URL = "https://qr-dector4.onrender.com/api/QR/"  # your live API endpoint

def send_qr_to_api(qr_text):
    """Send QR hash to your API"""
    qr_hash = hashlib.sha256(qr_text.encode()).hexdigest()
    data = {'qr_hash': qr_hash}
    try:
        requests.post(API_URL, json=data)
        print("✅ Sent to API:", qr_text)
    except Exception as e:
        print("❌ Error sending to API:", e)


def generate_frames():
    cap = cv2.VideoCapture(0)  # 0 = local webcam; or replace with IP camera URL
    detector = cv2.QRCodeDetector()
    last_qr = None

    while True:
        success, frame = cap.read()
        if not success:
            break

        data, points, _ = detector.detectAndDecode(frame)
        if data:
            if data != last_qr:
                print("Detected QR:", data)
                send_qr_to_api(data)
                last_qr = data

            # Draw green box
            if points is not None:
                points = points[0]
                for i in range(len(points)):
                    pt1 = tuple(map(int, points[i]))
                    pt2 = tuple(map(int, points[(i + 1) % len(points)]))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def live_stream_view(request):
    """Live video feed with automatic QR detection + API sending"""
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
