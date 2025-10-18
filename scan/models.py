from django.db import models

class QRDetection(models.Model):
    qr_hash = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qr_hash[:15] + "..."
