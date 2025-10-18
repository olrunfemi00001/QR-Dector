from django.contrib import admin
from .models import QRDetection

@admin.register(QRDetection)
class QRDetectionAdmin(admin.ModelAdmin):
    list_display = ('qr_hash', 'created_at')
    search_fields = ('qr_hash',)
