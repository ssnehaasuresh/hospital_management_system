from django.db import models

# Create your models here.
class Patient(models.Model):
    full_name=models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=13)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name