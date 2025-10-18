from django.urls import path
from .views import QRReceiveView

urlpatterns = [
    path('QR/', QRReceiveView.as_view(), name='receive-qr'),
]
