from django.urls import path
from .views import QRReceiveView,live_stream_view


urlpatterns = [
    path('QR/', QRReceiveView.as_view(), name='receive-qr'),
      path('live/', live_stream_view, name='live_stream'),
]
