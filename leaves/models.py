from django.db import models
from django.conf import settings
# Create your models here.
class LeaveRequest(models.Model):
    STATUS_CHOICES = [('pending','Pending'),
                      ('approved','Approved'),
                      ('rejected','Rejected'),
                      ]
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    