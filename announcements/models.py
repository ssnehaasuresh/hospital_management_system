from django.db import models
from django.conf import settings
# Create your models here.
class Announcements(models.Model):
    title = models.CharField(max_length=150)
    message = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']