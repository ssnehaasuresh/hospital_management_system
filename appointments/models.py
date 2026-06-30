from django.db import models
from django.conf import settings
from patients.models import Patient

MAX_PER_SLOT = 10 

class Appointment(models.Model):
    STATUS = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    SLOT_CHOICES = [
        ('morning', 'Morning (9:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (1:00 PM - 5:00 PM)'),
        ('night', 'Night (6:00 PM - 9:00 PM)'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.CharField(max_length=10, choices=SLOT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS, default='scheduled')

    class Meta:
        ordering = ['date', 'slot']
        unique_together = ('staff', 'date', 'slot')

    def __str__(self):
        return f'{self.patient.full_name} - {self.date} {self.slot}'