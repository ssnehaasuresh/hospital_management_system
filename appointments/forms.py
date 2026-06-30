from django import forms
from .models import Appointment, MAX_PER_SLOT
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    staff = forms.ModelChoiceField(
        queryset=User.objects.filter(role='doctor'),
        label='Doctor'
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'staff', 'date', 'slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        today = timezone.localdate()
        max_date = today + timedelta(days=2)

        if date < today:
            raise forms.ValidationError("You cannot book an appointment in the past.")
        if date > max_date:
            raise forms.ValidationError("You can only book up to 2 days in advance.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        slot = cleaned_data.get('slot')
        staff = cleaned_data.get('staff')

        if date and slot and staff:
            count = Appointment.objects.filter(
                date=date,
                slot=slot,
                staff=staff,
                status='scheduled'
            ).count()

            if count >= MAX_PER_SLOT:
                raise forms.ValidationError(
                    f"The {slot} slot for this doctor on {date} is fully booked ({MAX_PER_SLOT}/{MAX_PER_SLOT}). Please choose a different slot or date."
                )
        return cleaned_data